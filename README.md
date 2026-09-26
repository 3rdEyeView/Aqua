# Xtreme Jetski Watersports — Website Workspace

Dedicated workspace for https://xtremestpete.com (WordPress + Elementor).

## MCP server

`.mcp.json` defines `xtreme-jetski-watersports-elementor`, pointing at
`https://xtremestpete.com/wp-json/elementor/mcp/`. The `Authorization` header
is read from the `XTREME_WP_BASIC_AUTH` environment variable at runtime —
no credentials live in this repo.

`XTREME_WP_BASIC_AUTH` = base64 of `<wp-username>:<application-password>`
(without the `Basic ` prefix). Generate locally:

```sh
printf '%s' 'USERNAME:APP_PASSWORD' | base64
```

Set it in the Claude Code environment settings (cloud) or your shell profile
(local). Never commit it. See `.env.example`.
