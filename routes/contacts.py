from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from sqlalchemy import or_
from models import db, Contact, ContactMethod
from services.contact_methods import KINDS, apply_record

bp = Blueprint("contacts", __name__)

def form_record():
    return {"name": request.form.get("name", ""), "notes": request.form.get("notes", ""),
            "favorite": request.form.get("favorite") == "1",
            **{k: request.form.getlist(k) for k in KINDS}}

@bp.get("/")
def index():
    q = request.args.get("q", "").strip()
    favorites = request.args.get("favorites") == "1"
    stmt = db.select(Contact)
    if q:
        pattern = "%" + q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        stmt = stmt.where(or_(Contact.name.ilike(pattern, escape="\\"), Contact.methods.any(
            db.and_(ContactMethod.kind.in_(["phones", "emails"]), ContactMethod.value.ilike(pattern, escape="\\")))))
    if favorites:
        stmt = stmt.where(Contact.favorite.is_(True))
    contacts = db.session.scalars(stmt.order_by(Contact.name, Contact.id)).all()
    total = db.session.scalar(db.select(db.func.count(Contact.id)))
    starred = db.session.scalar(db.select(db.func.count(Contact.id)).where(Contact.favorite.is_(True)))
    return render_template("index.html", contacts=contacts, q=q, favorites=favorites, total=total, starred=starred)

@bp.route("/contacts/new", methods=["GET", "POST"])
def create():
    record = {"name": "", "notes": "", "favorite": False, **{k: [] for k in KINDS}}
    if request.method == "POST":
        record = form_record()
        try:
            contact = apply_record(Contact(), record)
            db.session.add(contact)
            db.session.commit()
            flash("联系人已新增", "success")
            return redirect(url_for("contacts.detail", contact_id=contact.id))
        except ValueError as exc:
            flash(str(exc), "error")
            return render_template("form.html", record=record, kinds=KINDS, editing=False), 400
    return render_template("form.html", record=record, kinds=KINDS, editing=False)

@bp.get("/contacts/<int:contact_id>")
def detail(contact_id):
    return render_template("detail.html", contact=db.get_or_404(Contact, contact_id), kinds=KINDS)

@bp.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
def edit(contact_id):
    contact = db.get_or_404(Contact, contact_id)
    record = contact.record()
    if request.method == "POST":
        record = form_record()
        try:
            apply_record(contact, record)
            db.session.commit()
            flash("联系人已更新", "success")
            return redirect(url_for("contacts.detail", contact_id=contact.id))
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")
            return render_template("form.html", record=record, kinds=KINDS, editing=True), 400
    return render_template("form.html", record=record, kinds=KINDS, editing=True)

@bp.post("/contacts/<int:contact_id>/delete")
def delete(contact_id):
    db.session.delete(db.get_or_404(Contact, contact_id))
    db.session.commit()
    flash("联系人已删除", "success")
    return redirect(url_for("contacts.index"))

@bp.get("/export")
def export_excel():
    from services.excel_service import export_contacts
    records = db.session.scalars(db.select(Contact).order_by(Contact.id)).all()
    return send_file(export_contacts(records), download_name="contacts.xlsx", as_attachment=True,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@bp.route("/import", methods=["GET", "POST"])
def import_excel():
    result = None
    if request.method == "POST":
        from services.excel_service import import_contacts
        upload = request.files.get("file")
        if not upload or not upload.filename or not upload.filename.lower().endswith(".xlsx"):
            flash("请选择 .xlsx 格式文件", "error")
            return render_template("import.html", result=None), 400
        try:
            result = import_contacts(upload.stream)
            flash(f"导入完成：成功 {result['success']} 条，失败 {result['failed']} 条，重复跳过 {result['skipped']} 条", "success")
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")
            return render_template("import.html", result=None), 400
    return render_template("import.html", result=result)
