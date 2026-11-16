"""Verify, package, and publish the existing application; never changes app code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
REPO = "3028405978-hue/address-book-application"
TAG = "v1.0.0"
NAME = "EE308_Address_Book_Submission_Final.zip"
RELEASE_URL = f"https://github.com/{REPO}/releases/tag/{TAG}"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def run(command, cwd, log):
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        print(result.stdout[-12000:])
        raise RuntimeError(f"Verification failed: {command}")
    return result.stdout


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    head = git("rev-parse", "HEAD")
    with tempfile.TemporaryDirectory(prefix="ee308-release-") as directory:
        scratch = Path(directory)
        junit = scratch / "test-results.xml"
        coverage = scratch / "coverage.xml"
        run([sys.executable, "-m", "pytest", "-v", "--cov=app", "--cov=models", "--cov=routes", "--cov=services", "--cov-report=term-missing", f"--cov-report=xml:{coverage}", f"--junitxml={junit}"], ROOT, scratch / "pytest-output.txt")
        run([sys.executable, "-m", "compileall", "."], ROOT, scratch / "compileall-output.txt")
        suite = ET.parse(junit).getroot().find("testsuite")
        counts = {key: int(suite.attrib.get(key, 0)) for key in ("tests", "failures", "errors", "skipped")}
        if counts != {"tests": 49, "failures": 0, "errors": 0, "skipped": 0}:
            raise RuntimeError(f"Unexpected test counts: {counts}")
        coverage_pct = round(float(ET.parse(coverage).getroot().attrib["line-rate"]) * 100)
        runtime = {
            "repository": f"https://github.com/{REPO}", "main_commit_sha": head,
            "commit_count": int(git("rev-list", "--count", "HEAD")),
            "release_url": RELEASE_URL, "pull_requests_url": f"https://github.com/{REPO}/pulls?q=is%3Apr+is%3Amerged",
            "actions_run_url": f"https://github.com/{REPO}/actions/runs/{os.environ['GITHUB_RUN_ID']}" if os.environ.get("GITHUB_RUN_ID") else None,
            "tests": counts, "coverage_percent": coverage_pct,
            "environment": {"system": platform.system(), "python": platform.python_version()},
            "screenshots": len(list((ROOT / "docs/screenshots").glob("*.png"))),
            "video": "docs/video/demo.mp4", "blog": "docs/CSDN_BLOG.md",
            "csdn_publication": "PENDING - owner must publish", "cloud_deployment": "PENDING - optional, no account authorization",
            "psp": "PENDING - owner must fill actual personal hours",
            "note": "Exact release-build snapshot. The release URL is authoritative for public publication status."
        }
        files = {}
        for name in git("ls-files").splitlines():
            path = Path(name)
            if any(part in (".git", ".venv", "__pycache__", ".pytest_cache", "instance") for part in path.parts) or path.suffix in (".db", ".sqlite", ".sqlite3", ".pyc") or path.name == ".env":
                raise RuntimeError(f"Forbidden tracked file: {name}")
            if name.startswith("dist/"):
                raise RuntimeError("Release archives must not be committed into source")
            files[name] = (ROOT / path).read_bytes()
        for name in ("pytest-output.txt", "compileall-output.txt", "test-results.xml", "coverage.xml"):
            files["docs/release-evidence/" + name] = (scratch / name).read_bytes()
        files["docs/FINAL_DELIVERY_RUNTIME.json"] = json.dumps(runtime, ensure_ascii=False, indent=2).encode()
        manifest = "\n".join(hashlib.sha256(data).hexdigest() + "  " + name for name, data in sorted(files.items())) + "\n"
        files["FILE_MANIFEST.sha256"] = manifest.encode()
        archive = output / NAME
        with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
            for name, data in sorted(files.items()):
                bundle.writestr("address-book-application/" + name, data)
        extracted = scratch / "unpacked"
        with ZipFile(archive) as bundle:
            if bundle.testzip() is not None:
                raise RuntimeError("ZIP CRC check failed")
            bundle.extractall(extracted)
        project = extracted / "address-book-application"
        for line in manifest.splitlines():
            expected, name = line.split("  ", 1)
            if hashlib.sha256((project / name).read_bytes()).hexdigest() != expected:
                raise RuntimeError(f"Checksum mismatch: {name}")
        run([sys.executable, "-m", "pytest", "-q"], project, output / "package-pytest-output.txt")
        run([sys.executable, "-m", "compileall", "."], project, output / "package-compileall-output.txt")
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        (output / (NAME + ".sha256")).write_text(digest + "  " + NAME + "\n")
        (output / "FINAL_DELIVERY_RUNTIME.json").write_text(json.dumps(runtime, ensure_ascii=False, indent=2))
        print(json.dumps({"zip": str(archive), "bytes": archive.stat().st_size, "sha256": digest, **runtime}, ensure_ascii=False, indent=2))
        return archive, runtime


def publish(archive, runtime):
    token = os.environ["GITHUB_TOKEN"]
    base = f"https://api.github.com/repos/{REPO}"

    def api(method, endpoint, body=None, binary=False):
        url = endpoint if endpoint.startswith("https://") else base + endpoint
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "EE308-release-workflow"}
        data = body if binary else (json.dumps(body).encode() if body is not None else None)
        if data is not None:
            headers["Content-Type"] = "application/zip" if binary else "application/json"
        with urlopen(Request(url, data=data, headers=headers, method=method), timeout=120) as response:
            content = response.read()
            return json.loads(content) if content else None

    head = runtime["main_commit_sha"]
    try:
        release = api("GET", f"/releases/tags/{TAG}")
    except HTTPError as exc:
        if exc.code != 404:
            raise
        release = None
    if release:
        # Final documentation may advance main after the first publication. Only
        # permit a verified fast-forward of this release's lightweight tag.
        ref = api("GET", f"/git/ref/tags/{TAG}")
        previous = ref["object"]["sha"]
        if ref["object"]["type"] != "commit":
            raise RuntimeError("Refusing to rewrite an annotated or unknown tag")
        if previous != head:
            subprocess.run(["git", "fetch", "origin", previous], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["git", "merge-base", "--is-ancestor", previous, head], cwd=ROOT, check=True)
            changes = git("diff", "--name-only", previous, head).splitlines()
            allowed = ("docs/", "scripts/", ".github/")
            if any(not (name.startswith(allowed) or name in ("README.md", "CODE_STANDARD.md", ".gitignore")) for name in changes):
                raise RuntimeError("New application code requires a new version; refusing to move v1.0.0")
            api("PATCH", f"/git/refs/tags/{TAG}", {"sha": head, "force": False})
    notes = (ROOT / "docs/RELEASE_NOTES.md").read_text(encoding="utf-8")
    body = {"tag_name": TAG, "target_commitish": head, "name": "Address Book Application v1.0.0", "body": notes + f"\n\nVerified commit: `{head}`\nActions: {runtime['actions_run_url']}\n", "draft": True if release is None else release["draft"], "prerelease": False}
    release = api("PATCH", f"/releases/{release['id']}", body) if release else api("POST", "/releases", body)
    wanted = [archive, archive.with_name(archive.name + ".sha256"), archive.parent / "FINAL_DELIVERY_RUNTIME.json"]
    for path in wanted:
        for asset in release.get("assets", []):
            if asset["name"] == path.name:
                api("DELETE", f"/releases/assets/{asset['id']}")
        upload = release["upload_url"].split("{", 1)[0] + "?name=" + path.name
        api("POST", upload, path.read_bytes(), binary=True)
    api("PATCH", f"/releases/{release['id']}", {"draft": False})
    final = api("GET", f"/releases/{release['id']}")
    names = {item["name"] for item in final["assets"]}
    if final["draft"] or not {p.name for p in wanted}.issubset(names):
        raise RuntimeError("Release publication verification failed")
    print("Published:", final["html_url"])
    for asset in final["assets"]:
        print(asset["browser_download_url"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Requires GitHub Actions contents:write token")
    parser.add_argument("--output", default=str(ROOT / "dist"))
    args = parser.parse_args()
    archive, runtime = build(Path(args.output).resolve())
    if args.publish:
        publish(archive, runtime)
