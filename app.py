"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# These extension instances are shared across the app and models
# so that SQLAlchemy can bind to the application context when the
# factory runs.
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """Application factory used by Flask and the tests.

    The optional ``test_config`` dictionary can override settings such as
    the database URL to keep student tests isolated.
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here so SQLAlchemy is aware of them before migrations
    # or ``create_all`` run. Students will flesh these out in ``models.py``.
    import models  # noqa: F401
    from models import User, Post

    @app.route("/")
    def index():
        """Simple sanity check route."""

        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})

    @app.route("/users", methods=["GET", "POST"])
    def users():
        if request.method == "GET":
            users = User.query.all()
            return jsonify([u.to_dict() for u in users]), 200

        if request.method == "POST":
            data = request.get_json()
            if not data or "username" not in data or "email" not in data:
                return jsonify({"error": "Missing username or email"}), 400

            new_user = User(username=data["username"], email=data["email"])
            db.session.add(new_user)
            db.session.commit()

        """List or create users.

        TODO: Students should query ``User`` objects, serialize them to JSON,
        and handle incoming POST data to create new users.
        """

        return (
            jsonify(new_user.to_dict()),
            501,
        )

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
       if request.method == "GET":
            posts = Post.query.all()
            return jsonify([p.to_dict() for p in posts]), 200

        if request.method == "POST":
            data = request.get_json()
            if not data or "title" not in data or "content" not in data or "user_id" not in data:
                return jsonify({"error": "Missing title, content or user_id"}), 400

            # Vérifier si user existe
            user = User.query.get(data["user_id"])
            if not user:
                return jsonify({"error": "User not found"}), 404

            new_post = Post(
                title=data["title"],
                content=data["content"],
                user_id=data["user_id"]
            )
            db.session.add(new_post)
            db.session.commit()

        """List or create posts.

        TODO: Students should query ``Post`` objects, include user data, and
        allow creating posts tied to a valid ``user_id``.
        """

        return (
            jsonify({new_post.to_dict()),
            501,
        )

    return app


# Expose a module-level application for convenience with certain tools
app = create_app()


if __name__ == "__main__":
    # Running ``python app.py`` starts the development server.
    app.run(debug=True)
