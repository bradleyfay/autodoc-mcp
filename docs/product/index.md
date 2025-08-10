# Product Documentation

Welcome to the AutoDocs MCP Server product documentation! This section contains everything you need to successfully install, configure, and use AutoDocs with your AI assistants.

## 🎯 What is AutoDocs MCP Server?

AutoDocs MCP Server is an **intelligent documentation context provider** that automatically supplies AI assistants with contextual, version-specific documentation for Python project dependencies. Instead of manually looking up package documentation, your AI assistant gets comprehensive context automatically.

### Key Benefits

- **🧠 Smart Context**: Automatically includes relevant dependencies with intelligent scoring
- **⚡ Fast Performance**: 3-5 second response times with version-based caching
- **🛡️ Production Ready**: Circuit breakers, graceful degradation, health monitoring
- **🔗 Native MCP Integration**: Works seamlessly with Claude, Cursor, and other MCP clients

## 🚀 Quick Start

### 1. Install AutoDocs
```bash
# Using uv (recommended)
uv tool install autodoc-mcp

# Using pip
pip install autodoc-mcp
```

### 2. Start the MCP Server
```bash
autodoc-mcp
```

### 3. Configure Your AI Client
Add AutoDocs to your MCP client configuration (see [Installation Guide](installation.md) for specific clients).

### 4. Test with Your AI Assistant
Ask your AI assistant: *"What packages are available in this project?"*

## 📚 Documentation Sections

<div class="doc-grid">
  <div class="doc-card">
    <h3>🚀 Getting Started</h3>
    <p>Step-by-step guide to get AutoDocs running with your AI assistant in under 5 minutes.</p>
    <a href="getting-started.md">Start Here →</a>
  </div>

  <div class="doc-card">
    <h3>💾 Installation</h3>
    <p>Detailed installation instructions for all supported MCP clients including Claude, Cursor, and more.</p>
    <a href="installation.md">Install Guide →</a>
  </div>

  <div class="doc-card">
    <h3>🛠️ MCP Tools</h3>
    <p>Complete reference for all 8 MCP tools including parameters, examples, and use cases.</p>
    <a href="mcp-tools.md">Tool Reference →</a>
  </div>

  <div class="doc-card">
    <h3>⚙️ Configuration</h3>
    <p>Environment variables, advanced settings, and performance tuning options.</p>
    <a href="configuration.md">Configure →</a>
  </div>

  <div class="doc-card">
    <h3>🔧 Troubleshooting</h3>
    <p>Common issues, error messages, debugging techniques, and performance optimization.</p>
    <a href="troubleshooting.md">Debug Issues →</a>
  </div>

  <div class="doc-card">
    <h3>📖 API Reference</h3>
    <p>Technical API documentation for advanced integrations and custom implementations.</p>
    <a href="api-reference.md">API Docs →</a>
  </div>
</div>

## 🌟 Featured Capabilities

### Phase 4: Dependency Context System
AutoDocs goes beyond single-package documentation by providing **intelligent dependency context**:

- **Smart Relevance Scoring**: Prioritizes major frameworks (FastAPI, Django, Flask)
- **Token-Aware Context**: Respects AI model context limits with automatic truncation
- **Concurrent Processing**: Fetches multiple dependencies simultaneously
- **Framework Intelligence**: Special handling for Python ecosystem patterns

### Example: FastAPI with Context
When you ask about FastAPI, AutoDocs automatically includes:
- **FastAPI** (primary package with full documentation)
- **Pydantic** (required for data validation)
- **Starlette** (underlying ASGI framework)
- **Uvicorn** (production server)

Your AI assistant gets complete context instead of fragmented information!

## 🎯 Use Cases

### For AI-Assisted Development
- **Context-Aware Code Generation**: AI knows about your dependencies and their capabilities
- **Accurate API Usage**: Proper method signatures and parameter types
- **Best Practices**: Framework-specific patterns and conventions
- **Error Resolution**: Understanding of error messages and common fixes

### For Learning & Exploration
- **Dependency Discovery**: Understand what packages your project uses
- **Framework Relationships**: See how packages work together
- **Version Compatibility**: Get documentation for your specific versions
- **Architecture Understanding**: Explore how components interact

## 📊 Performance & Reliability

- **277 Comprehensive Tests**: Full test coverage with pytest ecosystem
- **Network Resilience**: Circuit breakers and exponential backoff
- **Version-Based Caching**: Immutable package versions cached indefinitely
- **Graceful Degradation**: Partial results when some dependencies fail
- **Health Monitoring**: Built-in health checks and performance metrics

## 🤝 Support & Community

- **GitHub Issues**: [Report bugs or request features](https://github.com/bradleyfay/autodoc-mcp/issues)
- **Discussions**: Share use cases and get help
- **Contributing**: See [Development Process](../development/contributing.md) to contribute

---

## Next Steps

1. **New Users**: Start with [Getting Started](getting-started.md)
2. **Quick Setup**: Jump to [Installation](installation.md) for your MCP client
3. **Power Users**: Explore [Configuration](configuration.md) for advanced settings
4. **Issues**: Check [Troubleshooting](troubleshooting.md) for common problems
