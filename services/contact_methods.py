from models import ContactMethod

KINDS = {"phones": "电话号码", "emails": "电子邮箱", "socials": "社交账号", "addresses": "邮寄地址"}

def clean_record(record):
    name = str(record.get("name", "")).strip()
    if not name or len(name) > 100:
        raise ValueError("姓名不能为空，且不能超过 100 个字符")
    notes = str(record.get("notes", "")).strip()
    if len(notes) > 10000:
        raise ValueError("备注不能超过 10000 个字符")
    result = {"name": name, "notes": notes, "favorite": bool(record.get("favorite", False))}
    for kind in KINDS:
        values = list(dict.fromkeys(str(v).strip() for v in record.get(kind, []) if str(v).strip()))
        if len(values) > 50 or any(len(v) > 1000 for v in values):
            raise ValueError("每类联系方式最多 50 条，每条最多 1000 字符")
        if kind == "emails" and any("@" not in v or any(c.isspace() for c in v) or not all(v.rsplit("@", 1)) for v in values):
            raise ValueError("请输入有效的邮箱地址")
        result[kind] = values
    return result

def apply_record(contact, record):
    record = clean_record(record)
    contact.name, contact.notes, contact.favorite = record["name"], record["notes"], record["favorite"]
    contact.methods = [ContactMethod(kind=k, value=v) for k in KINDS for v in record[k]]
    return contact
