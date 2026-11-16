from models import db, Contact

def test_toggle_preserves_methods(post):
    post("/contacts/new", {"name": "收藏", "phones": ["123", "456"], "notes": "保留"})
    post("/contacts/1/favorite")
    c = db.session.get(Contact, 1)
    assert c.favorite and c.values("phones") == ["123", "456"] and c.notes == "保留"
    post("/contacts/1/favorite")
    assert not c.favorite

def test_filter(post, client):
    post("/contacts/new", {"name": "收藏人", "favorite": "1"})
    post("/contacts/new", {"name": "普通人"})
    response = client.get("/?favorites=1")
    assert "收藏人" in response.text and "普通人" not in response.text

def test_combined_filter(post, client):
    post("/contacts/new", {"name": "Alice", "favorite": "1"})
    post("/contacts/new", {"name": "Bob", "favorite": "1"})
    text = client.get("/?favorites=1&q=Alice").text
    assert "Alice" in text and "Bob" not in text

def test_missing_favorite(post):
    assert post("/contacts/999/favorite").status_code == 404
