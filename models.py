from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=False, default="")
    favorite = db.Column(db.Boolean, nullable=False, default=False)
    methods = db.relationship("ContactMethod", backref="contact", cascade="all, delete-orphan", order_by="ContactMethod.id")

    def values(self, kind):
        return [m.value for m in self.methods if m.kind == kind]

    def record(self):
        return {"name": self.name, "notes": self.notes, "favorite": self.favorite,
                **{k: self.values(k) for k in ("phones", "emails", "socials", "addresses")}}

class ContactMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False, index=True)
    kind = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Text, nullable=False)
