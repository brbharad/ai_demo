from __future__ import annotations

import json


class TestIndex:
    def test_index_returns_service_info(self, client) -> None:
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["service"] == "Flask + FastMCP Boilerplate"
        assert data["version"] == "0.1.0"
        assert "/health" in data["endpoints"]

    def test_index_lists_all_endpoints(self, client) -> None:
        resp = client.get("/")
        data = resp.get_json()
        assert set(data["endpoints"]) == {"/", "/health", "/hello/<name>", "/items"}


class TestHealth:
    def test_health_returns_healthy(self, client) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json() == {"status": "healthy"}


class TestHello:
    def test_hello_greets_by_name(self, client) -> None:
        resp = client.get("/hello/Alice")
        assert resp.status_code == 200
        assert resp.get_json() == {"message": "Hello, Alice!"}

    def test_hello_special_characters(self, client) -> None:
        resp = client.get("/hello/O'Brien")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "O'Brien" in data["message"]


class TestListItems:
    def test_list_items_returns_seed_data(self, client) -> None:
        resp = client.get("/items")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["count"] == 2
        assert len(data["items"]) == 2

    def test_list_items_seed_ids(self, client) -> None:
        resp = client.get("/items")
        ids = [item["id"] for item in resp.get_json()["items"]]
        assert ids == [1, 2]


class TestCreateItem:
    def test_create_item_happy_path(self, client) -> None:
        resp = client.post(
            "/items",
            data=json.dumps({"name": "baz", "value": 7}),
            content_type="application/json",
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "baz"
        assert data["value"] == 7
        assert data["id"] == 3

    def test_create_item_default_value(self, client) -> None:
        resp = client.post(
            "/items",
            data=json.dumps({"name": "minimal"}),
            content_type="application/json",
        )
        assert resp.status_code == 201
        assert resp.get_json()["value"] == 0

    def test_create_item_missing_name_returns_400(self, client) -> None:
        resp = client.post(
            "/items",
            data=json.dumps({"value": 99}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_create_item_empty_body_returns_400(self, client) -> None:
        resp = client.post("/items", content_type="application/json")
        assert resp.status_code == 400

    def test_create_item_increments_id(self, client) -> None:
        for i in range(3):
            resp = client.post(
                "/items",
                data=json.dumps({"name": f"item-{i}"}),
                content_type="application/json",
            )
            assert resp.get_json()["id"] == 3 + i

    def test_created_item_appears_in_list(self, client) -> None:
        client.post(
            "/items",
            data=json.dumps({"name": "new-entry"}),
            content_type="application/json",
        )
        resp = client.get("/items")
        names = [item["name"] for item in resp.get_json()["items"]]
        assert "new-entry" in names
