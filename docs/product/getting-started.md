# Getting Started

Get AutoDocs MCP Server running with your AI assistant in under 5 minutes!

## 🚀 Quick Setup

### Step 1: Install AutoDocs

=== "uv (Recommended)"
    ```bash
    uv tool install autodoc-mcp
    ```

=== "pip"
    ```bash
    pip install autodoc-mcp
    ```

=== "Development Setup"
    ```bash
    git clone https://github.com/bradleyfay/autodoc-mcp.git
    cd autodoc-mcp
    uv sync --all-extras
    ```

### Step 2: Test the Installation

```bash
# Verify installation
autodoc-mcp --version

# Test the server (should show FastMCP startup screen)
autodoc-mcp
```

You should see output like:
```
🚀 FastMCP Server Starting...
📊 Available MCP Tools: 8
✅ Server ready on stdio transport
```

Press `Ctrl+C` to stop the test server.

### Step 3: Configure Your MCP Client

Choose your AI assistant and follow the configuration:

=== "Claude Code Sessions"
    ```bash
    # AutoDocs is already globally available after installation
    # Start it in your session:
    autodoc-mcp
    ```

=== "Cursor Desktop"
    Add to Cursor settings (`Cmd+,` → Extensions → Rules for AI → MCP Servers):
    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",
          "env": {
            "CACHE_DIR": "~/.cache/autodoc-mcp"
          }
        }
      }
    }
    ```

=== "Claude Desktop"
    Add to `claude_desktop_config.json`:
    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",
          "env": {
            "CACHE_DIR": "~/.cache/autodoc-mcp"
          }
        }
      }
    }
    ```

### Step 4: Test with Your AI Assistant

Start a conversation with your AI assistant and try these test prompts:

!!! example "Test Commands"
    1. **"What packages are available in this project?"**
       *(Uses `scan_dependencies` tool)*

    2. **"Tell me about the FastAPI package with its dependencies"**
       *(Uses `get_package_docs_with_context` tool)*

    3. **"What's in the AutoDocs cache?"**
       *(Uses `get_cache_stats` tool)*

## 🎯 What to Expect

### First Request (Cache Miss)
- **Response Time**: 3-5 seconds (fetching from PyPI)
- **Context**: Primary package + 3-8 relevant dependencies
- **Caching**: All responses cached for future use

### Subsequent Requests (Cache Hit)
- **Response Time**: < 100ms (instant from cache)
- **Context**: Same comprehensive context as before
- **Performance**: Lightning fast with preserved quality

## 📊 Success Indicators

### ✅ Working Correctly
- AI assistant acknowledges AutoDocs tools are available
- Package queries return structured documentation
- Dependencies are automatically included in context
- Cache builds up over time (check with "cache stats" query)

### ❌ Common Issues
- **"Tool not found" errors**: MCP configuration problem
- **Network timeouts**: Check PyPI connectivity
- **Empty responses**: Verify package names are correct

See [Troubleshooting](troubleshooting.md) for detailed solutions.

## 🧠 Understanding the Context System

AutoDocs provides **three levels of context**:

### Level 1: Primary Package
```json
{
  "name": "fastapi",
  "version": "0.104.1",
  "summary": "FastAPI framework, high performance...",
  "key_features": ["Automatic API docs", "Type hints", "Async support"],
  "main_classes": ["FastAPI", "APIRouter", "Depends"]
}
```

### Level 2: Runtime Dependencies
```json
{
  "runtime_dependencies": [
    {
      "name": "pydantic",
      "why_included": "Required by fastapi",
      "summary": "Data validation using Python type hints"
    }
  ]
}
```

### Level 3: Context Metadata
```json
{
  "context_scope": "smart (3 deps)",
  "total_packages": 4,
  "token_estimate": 15420,
  "performance": {
    "total_time": 0.89,
    "cache_hits": 1,
    "cache_misses": 3
  }
}
```

## 🎨 Usage Patterns

### For Development Work
Ask your AI assistant:
- *"How do I create a FastAPI app with database models?"*
- *"What are the key differences between FastAPI and Django?"*
- *"Show me how to set up authentication with these packages"*

### For Learning & Exploration
Ask your AI assistant:
- *"What does this project depend on and why?"*
- *"Explain the relationship between these frameworks"*
- *"What are the main features of package X?"*

### For Debugging & Troubleshooting
Ask your AI assistant:
- *"This error mentions Pydantic - what might be wrong?"*
- *"How do I fix version conflicts with these dependencies?"*
- *"What's the proper way to configure package X?"*

## ⚡ Performance Tips

### Maximize Cache Efficiency
- **Ask about common packages first** (FastAPI, Django, requests)
- **Use consistent package names** (avoid typos that miss cache)
- **Let AutoDocs choose dependencies** (smart scoping is optimized)

### Optimize for Your Workflow
- **Set environment variables** for your preferred settings
- **Use project-specific cache directories** for isolation
- **Monitor cache stats** to understand performance patterns

## 📈 What's Next?

Now that AutoDocs is working:

1. **Explore MCP Tools**: Learn about all [8 available tools](mcp-tools.md)
2. **Customize Configuration**: Tune performance with [configuration options](configuration.md)
3. **Advanced Usage**: Discover power-user features in the [API Reference](api-reference.md)

---

## 🆘 Need Help?

- **Quick Issues**: Check [Troubleshooting](troubleshooting.md)
- **Configuration Problems**: See detailed [Installation Guide](installation.md)
- **Bug Reports**: [GitHub Issues](https://github.com/bradleyfay/autodoc-mcp/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/bradleyfay/autodoc-mcp/discussions)
