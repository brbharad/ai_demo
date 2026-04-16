from __future__ import annotations

from flask import Flask, abort, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)

    # In-memory state — fresh per create_app() call (safe for testing)
    items: list[dict] = [
        {"id": 1, "name": "foo", "value": 42},
        {"id": 2, "name": "bar", "value": 100},
    ]
    next_id = 3

    @app.route("/")
    def index():
        return jsonify(
            {
                "service": "Flask + FastMCP Boilerplate",
                "version": "0.1.0",
                "endpoints": ["/", "/health", "/hello/<name>", "/items"],
            }
        )

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.route("/hello/<name>")
    def hello(name: str):
        return jsonify({"message": f"Hello, {name}!"})

    @app.route("/items", methods=["GET"])
    def list_items():
        return jsonify({"items": items, "count": len(items)})

    @app.route("/items", methods=["POST"])
    def create_item():
        nonlocal next_id
        data = request.get_json(silent=True)
        if not data or "name" not in data:
            abort(400, description="JSON body with 'name' field required")
        item = {
            "id": next_id,
            "name": str(data["name"]),
            "value": data.get("value", 0),
        }
        items.append(item)
        next_id += 1
        return jsonify(item), 201

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
