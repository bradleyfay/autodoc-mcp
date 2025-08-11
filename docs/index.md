# AutoDocs MCP Server Documentation

<div class="hero-banner">
  <h1>🤖 Intelligent Documentation Context for AI Assistants</h1>
  <p class="lead">AutoDocs MCP Server automatically provides AI assistants with contextual, version-specific documentation for Python project dependencies. Choose your path below to explore the documentation that's most relevant to you.</p>
</div>

## 🗺️ Choose Your Documentation Path

<div class="path-cards">
  <div class="path-card product">
    <h3>📚 Product Documentation</h3>
    <p><strong>For Users & Integrators</strong></p>
    <p>Learn how to install, configure, and use AutoDocs MCP Server with your AI assistants. Includes API reference, troubleshooting, and integration guides.</p>
    <ul>
      <li>Quick installation and setup</li>
      <li>MCP tools and their usage</li>
      <li>Configuration options</li>
      <li>Troubleshooting guides</li>
    </ul>
    <a href="product/" class="btn-primary">Start Using AutoDocs →</a>
  </div>

  <div class="path-card development">
    <h3>🏗️ Development Process</h3>
    <p><strong>For Contributors & Technical Reviewers</strong></p>
    <p>Understand the system architecture, development standards, and how to contribute to the project. Essential for anyone working on or reviewing the codebase.</p>
    <ul>
      <li>System architecture and design decisions</li>
      <li>Development standards and workflows</li>
      <li>Testing strategies and requirements</li>
      <li>Contribution guidelines</li>
    </ul>
    <a href="development/" class="btn-secondary">Explore the Process →</a>
  </div>

  <div class="path-card journey">
    <h3>📖 Development Journey</h3>
    <p><strong>For AI-Development Enthusiasts</strong></p>
    <p>Follow the complete development story of this project, from initial concept to Phase 4 completion. See how "intention-only programming" works in practice.</p>
    <ul>
      <li>Phase-by-phase evolution</li>
      <li>Technical decisions and learnings</li>
      <li>Development session insights</li>
      <li>AI-assisted development patterns</li>
    </ul>
    <a href="journey/" class="btn-accent">Follow the Journey →</a>
  </div>
</div>

## 🚀 Quick Start

!!! tip "New to AutoDocs?"
    **For immediate usage**: Start with [Product Documentation](product/getting-started/)

    **For contributing**: Check out [Development Process](development/contributing/)

    **For the full story**: Explore the [Development Journey](journey/evolution/)

### Installation (Quick)

=== "PyPI Installation"
    ```bash
    # Install with uv (recommended)
    uv tool install autodoc-mcp

    # Start the MCP server
    autodoc-mcp
    ```

=== "Development Setup"
    ```bash
    # Clone and set up for development
    git clone https://github.com/bradleyfay/autodoc-mcp.git
    cd autodoc-mcp
    uv sync --all-extras

    # Run tests
    uv run pytest
    ```

## 🎯 Project Overview

AutoDocs MCP Server is a **fully implemented** Model Context Protocol (MCP) server that provides AI assistants with intelligent, context-aware documentation for Python dependencies.

### Key Features

- **🧠 Smart Dependency Context**: Automatically includes relevant dependencies with intelligent relevance scoring
- **⚡ High Performance**: Version-based caching with concurrent fetching (3-5 second response times)
- **🛡️ Production Ready**: Circuit breakers, graceful degradation, comprehensive health monitoring
- **🔗 MCP Native**: 8 comprehensive MCP tools for seamless AI integration

### Architecture Highlights

- **Phase 4 Complete**: Full dependency context system with smart scoping
- **277 Tests**: Comprehensive test coverage with pytest ecosystem
- **Layered Architecture**: Clean separation of concerns with 10 core service modules
- **Network Resilience**: Exponential backoff, connection pooling, circuit breakers

## 🏆 Project Status

<div class="status-badges">
  <span class="badge badge-success">Phase 4 Complete ✅</span>
  <span class="badge badge-info">Production Ready 🚀</span>
  <span class="badge badge-primary">Open Source 💚</span>
</div>

**Current Version**: v0.4.2
**Test Coverage**: 277 comprehensive tests
**MCP Tools**: 8 production-ready tools
**Architecture**: Phase 4 layered design complete

## 📊 Navigation Summary

| Section | Best For | Key Content |
|---------|----------|-------------|
| **[📚 Product Docs](product/)** | End users, integrators | Installation, usage, API reference, troubleshooting |
| **[🏗️ Development Process](development/)** | Contributors, reviewers | Architecture, standards, testing, contributing |
| **[📖 Development Journey](journey/)** | Learning enthusiasts | Project evolution, decisions, AI-development insights |

---

<div class="footer-note">
  <p><strong>💡 About This Project</strong></p>
  <p>AutoDocs MCP Server demonstrates "intention-only programming" - describing what you want rather than how to implement it. This documentation site itself was created through this approach, showing how AI assistants can help build comprehensive documentation from existing project materials.</p>
</div>
