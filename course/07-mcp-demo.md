# MCP demo (7 minutes, facilitator)

## Message

An MCP server gives the agent new tools and new data. Trust it like a dependency: it comes from an official source, it
gets the fewest permissions possible, and it is read-only whenever you can manage it.

## Setup (before the session)

- The organisation policy "MCP servers in Copilot" must be enabled for the facilitator's seat (it is disabled by default for Copilot Business and Enterprise).
- A **fine-grained personal access token** limited to `CAprogs/coding-dojo-devx`, with read-only access to Contents and Pull requests.
- The configuration below, copied from [examples/mcp.json](examples/mcp.json) to `.vscode/mcp.json` on the facilitator's machine only.

```json
{
  "inputs": [
    { "id": "github_pat", "type": "promptString", "description": "Read-only fine-grained token", "password": true }
  ],
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/readonly",
      "headers": {
        "Authorization": "Bearer ${input:github_pat}",
        "X-MCP-Toolsets": "repos,pull_requests"
      }
    }
  }
}
```

The `/readonly` endpoint exposes read tools only. The token adds a second limit: even a write tool would be refused.
Signing in with OAuth instead would grant the scopes of the app across every repository your account can access.

## Script

1. Show the server in the tools picker, and the tools it exposes (names, read-only).
2. In Agent mode: "List the open pull requests on the lab-2 branch of CAprogs/coding-dojo-devx and which ones have failing checks."
3. Ask it to add a comment on one pull request. It cannot: no write tool is available.
4. Point out that the pull request titles and descriptions it just read were written by learners, so they are **untrusted input**.
   An MCP server makes that text part of the agent's context.

## Fallback

Show the recording or screenshots from the rehearsal.

## Why not build our own GitHub MCP server?

The official server already offers read-only mode and toolsets. A custom server would add code, token handling and a trust
boundary to maintain, without teaching anything more about harness design.
