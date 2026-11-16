from io import BytesIO
import pytest
from openpyxl import Workbook, load_workbook
from models import db, Contact
from services.excel_service import HEADERS

def workbook(rows):
    w = Workbook()
    for row in rows:
        w.active.append(row)
    b = BytesIO(); w.save(b); b.seek(0)
    return b

def upload(post, data, filename="data.xlsx"):
    return post("/import", {"file": (data, filename)})

def test_export(post, client):
    post("/contacts/new", {"name": "导出", "phones": ["001"]})
    r = client.get("/export")
    assert r.status_code == 200 and "attachment" in r.headers["Content-Disposition"]
    w = load_workbook(BytesIO(r.data))
    assert list(next(w.active.values)) == HEADERS
    assert w.active["B2"].value == '["001"]'

def test_chinese_headers_partial_import(post):
    r = upload(post, workbook([["姓名", "电话", "邮箱", "收藏"], ["中文", "001;002", "a@b.com；c@d.com", "是"], [None, "123", None, "否"]]))
    assert r.status_code == 200 and "成功 1 条，失败 1 条" in r.text
    c = db.session.scalar(db.select(Contact))
    assert c.favorite and c.values("phones") == ["001", "002"] and len(c.values("emails")) == 2

def test_lossless_roundtrip(post, client):
    data = {"name": "=SUM(1,2)", "phones": ["00123", "+86 123"], "emails": ["a@example.com", "b@example.com"], "socials": ["微信;含分号", "QQ|包含竖线"], "addresses": ["楼一\n二层", "地址；含分隔符"], "notes": "=hello\n中文备注", "favorite": "1"}
    post("/contacts/new", data)
    original = db.session.get(Contact, 1).record()
    exported = client.get("/export").data
    w = load_workbook(BytesIO(exported))
    assert w.active["A2"].data_type == "s" and w.active["F2"].data_type == "s"
    post("/contacts/1/delete")
    assert upload(post, BytesIO(exported)).status_code == 200
    assert db.session.scalar(db.select(Contact)).record() == original

def test_exact_duplicates_skip_same_name_new_record(post):
    rows = [["Name", "Phones"], ["同名", "123"], ["同名", "123"], ["同名", "456"]]
    r = upload(post, workbook(rows))
    assert "成功 2 条，失败 0 条，重复跳过 1 条" in r.text
    r = upload(post, workbook(rows))
    assert "成功 0 条，失败 0 条，重复跳过 3 条" in r.text

@pytest.mark.parametrize("content,filename", [(b"bad", "bad.xlsx"), (b"", "empty.xlsx"), (b"text", "file.csv")])
def test_invalid_file(post, content, filename):
    assert upload(post, BytesIO(content), filename).status_code == 400
    assert db.session.scalar(db.select(db.func.count(Contact.id))) == 0

@pytest.mark.parametrize("rows", [[], [["Phones"], ["123"]], [["Name", "姓名"], ["a", "b"]]])
def test_invalid_headers(post, rows):
    assert upload(post, workbook(rows)).status_code == 400

def test_header_only(post):
    r = upload(post, workbook([HEADERS]))
    assert r.status_code == 200 and "成功 0 条" in r.text

def test_reject_formula_and_bad_values(post):
    r = upload(post, workbook([["Name", "Phones", "Favorite"], ["=1+1", "123", True], ["错误数组", "[invalid", False], ["错误收藏", "123", "maybe"], ["正确", "123", False]]))
    assert "成功 1 条，失败 3 条" in r.text

def test_no_upload(post):
    assert post("/import").status_code == 400

def test_blank_rows(post):
    r = upload(post, workbook([["Name"], [None], ["正常"]]))
    assert "成功 1 条，失败 0 条" in r.text

def test_empty_export(client):
    w = load_workbook(BytesIO(client.get("/export").data))
    assert w.active.max_row == 1
