"""XLSX interchange. JSON arrays preserve delimiters/newlines losslessly."""
import json
from io import BytesIO
from zipfile import ZipFile, BadZipFile
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from models import db, Contact
from services.contact_methods import KINDS, clean_record, apply_record

HEADERS = ["Name", "Phones", "Emails", "Social Accounts", "Addresses", "Notes", "Favorite"]
FIELDS = ["name", "phones", "emails", "socials", "addresses", "notes", "favorite"]
ALIASES = {
    "name": "name", "姓名": "name", "phones": "phones", "phone": "phones", "电话": "phones", "电话号码": "phones",
    "emails": "emails", "email": "emails", "邮箱": "emails", "电子邮箱": "emails",
    "social accounts": "socials", "socials": "socials", "社交账号": "socials",
    "addresses": "addresses", "address": "addresses", "地址": "addresses", "邮寄地址": "addresses",
    "notes": "notes", "备注": "notes", "favorite": "favorite", "收藏": "favorite", "收藏状态": "favorite",
}

def signature(record):
    return json.dumps(record, ensure_ascii=False, sort_keys=True)

def export_contacts(contacts):
    wb = Workbook()
    ws = wb.active
    ws.title = "Contacts"
    ws.append(HEADERS)
    for contact in contacts:
        record = contact.record()
        values = [record[k] if k not in KINDS else json.dumps(record[k], ensure_ascii=False) for k in FIELDS]
        ws.append(values)
        # Explicit string cells prevent untrusted leading '=' from becoming formulas.
        for cell in ws[ws.max_row]:
            if isinstance(cell.value, str):
                cell.data_type = "s"
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for cell in ws[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = PatternFill("solid", fgColor="247C61")
    for col in "ABCDEFG":
        ws.column_dimensions[col].width = 28 if col != "A" else 18
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream

def parse_list(value):
    text = str(value or "").strip()
    if not text:
        return []
    if text.startswith("["):
        try:
            result = json.loads(text)
        except (ValueError, TypeError) as exc:
            raise ValueError("多值 JSON 数组格式错误") from exc
        if not isinstance(result, list) or any(not isinstance(v, str) for v in result):
            raise ValueError("联系方式必须是字符串数组")
        return result
    return text.replace("；", ";").split(";")

def parse_favorite(value):
    if value is None:
        return False
    text = str(value).strip().lower()
    if text in ("true", "1", "yes", "是", "已收藏", "收藏"):
        return True
    if text in ("false", "0", "no", "否", "未收藏", ""):
        return False
    raise ValueError("收藏状态应为 True/False、1/0 或 是/否")

def import_contacts(stream):
    try:
        with ZipFile(stream) as archive:
            if sum(info.file_size for info in archive.infolist()) > 30 * 1024 * 1024:
                raise ValueError("Excel 解压后超过 30 MB 限制")
        stream.seek(0)
        wb = load_workbook(stream, read_only=True, data_only=False)
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("无法读取 Excel，请使用未损坏且未加密的 .xlsx 文件") from exc
    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}
    try:
        ws = wb.active
        rows = ws.iter_rows()
        header = next(rows, None)
        if not header or all(c.value is None for c in header):
            raise ValueError("文件为空或缺少表头")
        mapped = [ALIASES.get(str(c.value or "").strip().lower()) for c in header]
        known = [k for k in mapped if k]
        if "name" not in known or len(known) != len(set(known)):
            raise ValueError("需要唯一的 Name / 姓名表头，且不能重复映射列")
        seen = {signature(c.record()) for c in db.session.scalars(db.select(Contact))}
        for number, row in enumerate(rows, 2):
            if number > 10001:
                raise ValueError("单次导入最多 10000 行，请拆分文件")
            if all(c.value is None for c in row):
                continue
            try:
                if any(c.data_type == "f" for c in row):
                    raise ValueError("不接受公式单元格，请先粘贴为纯文本")
                raw = {key: c.value for key, c in zip(mapped, row) if key}
                record = clean_record({"name": str(raw.get("name") or ""), "notes": str(raw.get("notes") or ""),
                    "favorite": parse_favorite(raw.get("favorite")), **{k: parse_list(raw.get(k)) for k in KINDS}})
                key = signature(record)
                if key in seen:
                    result["skipped"] += 1
                    continue
                db.session.add(apply_record(Contact(), record))
                seen.add(key)
                result["success"] += 1
            except ValueError as exc:
                result["failed"] += 1
                result["errors"].append(f"第 {number} 行：{exc}")
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        if isinstance(exc, ValueError):
            raise
        raise ValueError("Excel 结构错误，导入已回滚") from exc
    finally:
        wb.close()
    return result
