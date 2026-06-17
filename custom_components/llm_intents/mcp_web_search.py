class MCPWebSearchTool(SearchWebTool):
    """Web search tool backed by MCP server."""

    def __init__(self, config, hass):
        super().__init__(config, hass)
        self.base_url = config.get("mcp_url", "http://localhost:8005")

    async def async_search(self, query: str) -> list:
        session = async_get_clientsession(self.hass)

        async with session.post(
            f"{self.base_url}/tools/web_search",
            json={"query": query},
        ) as resp:
            if resp.status != 200:
                raise RuntimeError(await resp.text())

            data = await resp.json()
            return self._normalize(data)

    def _normalize(self, data):
        return [
            {
                "title": r.get("title", ""),
                "content": r.get("content", ""),
            }
            for r in data.get("results", [])
        ]
