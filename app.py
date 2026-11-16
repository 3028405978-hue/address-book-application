from pathlib import Path
import hmac
import secrets
from flask import Flask, session, request, abort, render_template
from config import Config
from models import db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    from routes.contacts import bp
    from routes.favorites import bp as favorites_bp
    app.register_blueprint(bp)
    app.register_blueprint(favorites_bp)

    def csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)
        return session["csrf_token"]
    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.before_request
    def csrf_protect():
        if request.method == "POST":
            expected = session.get("csrf_token", "")
            actual = request.form.get("csrf_token", "")
            if not expected or not hmac.compare_digest(expected, actual):
                abort(400, description="表单已过期，请刷新页面后重试")

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(413)
    def error(err):
        message = "文件过大，最大允许 5 MB" if err.code == 413 else err.description
        return render_template("error.html", code=err.code, message=message), err.code

    with app.app_context():
        db.create_all()
    return app

if __name__ == "__main__":
    from waitress import serve
    serve(create_app(), host="127.0.0.1", port=5000)
