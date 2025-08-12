# Claude Code Agents Documentation

Welcome to the Claude Code Agents documentation section. This comprehensive guide provides detailed user manuals and system prompts for all available Claude Code agents.

## What are Claude Code Agents?

Claude Code agents are specialized AI assistants designed to handle specific domains and tasks within the Claude Code ecosystem. Each agent has:

- **Specialized expertise** in a particular domain
- **Defined tool access** for performing operations
- **Clear boundaries** and collaboration patterns
- **Technical specifications** for integration

## Available Agents

### Technical Implementation Agents

#### [Claude Agent Builder](claude-agent-builder.md)
Technical specialist in Claude Code agent implementation, file format validation, and agent ecosystem integration. Use for creating properly formatted agent files, validating YAML frontmatter, and ensuring ecosystem compatibility.

## How to Use This Documentation

Each agent page includes:

1. **User Manual**: Comprehensive guide for developers
   - When to use the agent
   - Effective prompting strategies
   - Common patterns and templates
   - Troubleshooting guide
   - Best practices

2. **System Prompt**: Complete agent specification
   - YAML frontmatter configuration
   - Core expertise areas
   - Integration patterns
   - Quality standards

## Agent Selection Guide

Choose the right agent for your task:

| Task Type | Recommended Agent |
|-----------|------------------|
| Creating new agent files | claude-agent-builder |
| Validating agent compliance | claude-agent-builder |
| Fixing agent integration issues | claude-agent-builder |

## Contributing

To add documentation for a new agent:

1. Create a new markdown file in `/docs/agents/`
2. Include both user manual and system prompt
3. Update this index page with the new agent
4. Add the agent to mkdocs.yml navigation

## Best Practices for Agent Usage

### 1. Understand Agent Boundaries
Each agent has specific expertise. Use the right agent for the right task to get optimal results.

### 2. Follow Sequential Workflows
Many agents work best in combination. For example:
- Design with `agent-design-architect`
- Implement with `claude-agent-builder`
- Validate with both agents

### 3. Use Clear, Specific Prompts
Provide concrete requirements and context to help agents deliver precise results.

### 4. Leverage Templates and Patterns
Most agents provide templates and patterns. Use these as starting points for consistency and quality.

### 5. Validate Early and Often
Run validation checks throughout your workflow to catch issues early.

## Quick Reference

### Common Agent Patterns

- **Technical Specialist**: Core development, testing, operations
- **Content Specialist**: Documentation, writing, content strategy
- **Coordination Specialist**: Workflow orchestration, project management
- **Analysis Specialist**: Investigation, monitoring, reporting

### Tool Categories

- **File Operations**: `Glob`, `Grep`, `LS`, `Read`, `Edit`, `MultiEdit`, `Write`
- **Workflow**: `Task`, `TodoWrite`
- **Web**: `WebFetch`, `WebSearch`
- **Development**: `Bash`, `BashOutput`, `KillBash`
- **Specialized**: `NotebookEdit`, `ListMcpResourcesTool`, `ReadMcpResourceTool`

## Support and Feedback

For questions, issues, or suggestions about agent documentation:
- Create an issue in the [GitHub repository](https://github.com/anthropics/claude-code/issues)
- Refer to the troubleshooting sections in individual agent manuals
- Review best practices and common patterns
