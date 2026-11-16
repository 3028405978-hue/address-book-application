import pytest
from models import db, Contact, ContactMethod
from app import create_app

def test_create(post):
    response = post("/contacts/new", {"name": "张三", "phones": ["010-123", "13900000000"]})
    assert response.status_code == 302
    contact = db.session.scalar(db.select(Contact))
    assert contact.name == "张三" and len(contact.values("phones")) == 2

@pytest.mark.parametrize("name", ["", "   ", "A" * 101])
def test_invalid_name(post, name):
    assert post("/contacts/new", {"name": name}).status_code == 400
    assert db.session.scalar(db.select(db.func.count(Contact.id))) == 0

def test_detail(post, client):
    post("/contacts/new", {"name": "详情测试", "notes": "备注内容"})
    response = client.get("/contacts/1")
    assert response.status_code == 200 and "备注内容" in response.text

def test_edit(post):
    post("/contacts/new", {"name": "原名", "phones": ["111", "222"], "favorite": "1"})
    assert post("/contacts/1/edit", {"name": "新名", "phones": ["333"], "emails": ["a@example.com"]}).status_code == 302
    c = db.session.get(Contact, 1)
    assert c.name == "新名" and c.values("phones") == ["333"] and not c.favorite
    assert db.session.scalar(db.select(db.func.count(ContactMethod.id))) == 2

def test_delete(post, client):
    post("/contacts/new", {"name": "删除", "phones": ["123"]})
    assert post("/contacts/1/delete").status_code == 302
    assert client.get("/contacts/1").status_code == 404
    assert db.session.scalar(db.select(db.func.count(ContactMethod.id))) == 0

@pytest.mark.parametrize("query", ["张三", "13912345678", "secondary@example.com"])
def test_search(post, client, query):
    post("/contacts/new", {"name": "张三", "phones": ["010", "13912345678"], "emails": ["a@example.com", "secondary@example.com"]})
    post("/contacts/new", {"name": "李四"})
    response = client.get("/", query_string={"q": query})
    assert "张三" in response.text and "李四" not in response.text

@pytest.mark.parametrize("query", ["%", "_", "\\"])
def test_search_literal_wildcards(post, client, query):
    post("/contacts/new", {"name": "普通联系人"})
    assert "普通联系人" not in client.get("/", query_string={"q": query}).text

def test_multiple_methods(post, client):
    fields = {"name": "多联系方式", "phones": ["001", "002"], "emails": ["a@b.com", "c@d.com"], "socials": ["微信:a", "QQ:b"], "addresses": ["福州", "上海"]}
    post("/contacts/new", fields)
    c = db.session.get(Contact, 1)
    for key in ["phones", "emails", "socials", "addresses"]:
        assert c.values(key) == fields[key]
        for value in fields[key]:
            assert value in client.get("/contacts/1").text

def test_sqlite_persistence(app, post):
    post("/contacts/new", {"name": "持久化", "favorite": "1", "phones": ["0001"]})
    second = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": app.config["SQLALCHEMY_DATABASE_URI"]})
    with second.app_context():
        c = db.session.get(Contact, 1)
        assert c.name == "持久化" and c.favorite and c.values("phones") == ["0001"]

def test_empty_page(client):
    assert "从第一位联系人开始" in client.get("/").text

def test_csrf_rejected(client):
    assert client.post("/contacts/new", data={"name": "非法请求"}).status_code == 400

def test_html_escaped(post, client):
    post("/contacts/new", {"name": "<script>alert(1)</script>"})
    assert "&lt;script&gt;" in client.get("/contacts/1").text

def test_invalid_email(post):
    assert post("/contacts/new", {"name": "邮箱", "emails": ["bad"]}).status_code == 400

def test_invalid_edit_preserves_data(post):
    post("/contacts/new", {"name": "保留", "phones": ["123"]})
    assert post("/contacts/1/edit", {"name": "", "phones": ["456"]}).status_code == 400
    assert db.session.get(Contact, 1).values("phones") == ["123"]

def test_normalize_blank_duplicates(post):
    post("/contacts/new", {"name": " 测试 ", "phones": ["123", " 123 ", ""]})
    assert db.session.get(Contact, 1).values("phones") == ["123"]

def test_oversize_upload(app, post):
    from io import BytesIO
    app.config["MAX_CONTENT_LENGTH"] = 1024
    assert post("/import", {"file": (BytesIO(b"a" * 2048), "big.xlsx")}).status_code == 413

@pytest.mark.parametrize("url", ["/contacts/999", "/contacts/999/edit"])
def test_missing(client, url):
    assert client.get(url).status_code == 404


@pytest.mark.parametrize("data", [
    {"name": "控制字符\x00"},
    {"name": "非法 XML\uffff"},
    {"name": "测试", "phones": [str(i) + "x" * 990 for i in range(50)]},
    {"name": "测试", "notes": "x" * 10001},
    {"name": "测试", "phones": ["x" * 1001]},
    {"name": "测试", "phones": [str(i) for i in range(51)]},
])
def test_reject_unexportable_or_oversized_fields(post, data):
    assert post("/contacts/new", data).status_code == 400
    assert db.session.scalar(db.select(db.func.count(Contact.id))) == 0
