from __future__ import annotations

from mcp_server import add, greeting_resource, healthcheck, hello, hello_prompt, server_info


class TestHelloTool:
    def test_hello_default(self) -> None:
        result = hello()
        assert result == "Hello, World! Greetings from FastMCP."

    def test_hello_custom_name(self) -> None:
        result = hello(name="Alice")
        assert "Alice" in result

    def test_hello_empty_string(self) -> None:
        result = hello(name="")
        assert "Hello, !" in result


class TestAddTool:
    def test_add_positive(self) -> None:
        assert add(2, 3) == 5.0

    def test_add_negative(self) -> None:
        assert add(-1, -2) == -3.0

    def test_add_floats(self) -> None:
        assert add(1.5, 2.5) == 4.0

    def test_add_zero(self) -> None:
        assert add(0, 0) == 0.0


class TestServerInfo:
    def test_server_info_keys(self) -> None:
        info = server_info()
        assert "name" in info
        assert "version" in info
        assert "tools" in info
        assert "resources" in info
        assert "prompts" in info

    def test_server_info_tool_list(self) -> None:
        info = server_info()
        assert "hello" in info["tools"]
        assert "add" in info["tools"]
        assert "server_info" in info["tools"]


class TestGreetingResource:
    def test_greeting_resource(self) -> None:
        result = greeting_resource(name="Bob")
        assert "Bob" in result
        assert "FastMCP resource" in result


class TestHelloPrompt:
    def test_hello_prompt_default(self) -> None:
        result = hello_prompt()
        assert "World" in result


class TestHealthcheck:
    def test_healthcheck_status(self) -> None:
        result = healthcheck()
        assert result["status"] == "healthy"

    def test_healthcheck_server_name(self) -> None:
        result = healthcheck()
        assert "server" in result

    def test_hello_prompt_custom(self) -> None:
        result = hello_prompt(name="Cisco")
        assert "Cisco" in result
