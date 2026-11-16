from flask import Blueprint, redirect, url_for, flash
from models import db, Contact

bp = Blueprint("favorites", __name__)

@bp.post("/contacts/<int:contact_id>/favorite")
def toggle(contact_id):
    contact = db.get_or_404(Contact, contact_id)
    contact.favorite = not contact.favorite
    db.session.commit()
    flash("已收藏联系人" if contact.favorite else "已取消收藏", "success")
    return redirect(url_for("contacts.detail", contact_id=contact.id))
