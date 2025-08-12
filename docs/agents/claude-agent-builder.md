# Claude Agent Builder User Manual

## Quick Start Guide

The Claude Agent Builder is your technical implementation specialist for creating Claude Code agents. It transforms high-level agent concepts into production-ready, technically compliant agent files that integrate seamlessly with the Claude Code ecosystem.

### When to Use Claude Agent Builder

**Use this agent for:**
- Creating new Claude Code agent files with proper YAML frontmatter
- Validating agent file format and structure compliance
- Ensuring ecosystem integration and preventing conflicts
- Implementing agent specifications from design phase
- Fixing technical issues with existing agent files

**Do NOT use this agent for:**
- High-level agent design or architecture (use `agent-design-architect` instead)
- Strategic decisions about agent scope and capabilities
- Multi-agent workflow orchestration design
- Performance optimization strategies

### Success Formula

The most effective way to use claude-agent-builder follows this sequential workflow:

```
1. Design Phase (agent-design-architect) →
2. Implementation Phase (claude-agent-builder) →
3. Validation Phase (both agents)
```

## Core Capabilities

### 1. Agent File Creation
- Generates properly formatted `.md` files in `.claude/agents/` directory
- Ensures YAML frontmatter compliance with all required fields
- Applies appropriate naming conventions (kebab-case)
- Assigns unique colors for visual identification

### 2. Technical Validation
- Pre-creation validation (8-point checklist)
- Post-creation quality gates (5-point verification)
- Schema compliance checking
- Integration testing with Task tool

### 3. Ecosystem Integration
- Prevents conflicts with existing agents
- Validates tool assignments match capabilities
- Ensures smooth collaboration patterns
- Maintains ecosystem coherence

### 4. Template Application
- Provides 4 specialized implementation patterns
- Offers pre-defined tool combinations
- Ensures structural consistency
- Implements best practices automatically

## Effective Prompting Strategies

### Basic Agent Creation

**Good Prompt:**
```
Create a new agent file for a database migration specialist that can:
- Analyze database schemas
- Generate migration scripts
- Validate migration safety
- Coordinate with testing agents

Use the Technical Specialist pattern and ensure it integrates with existing testing and production-ops agents.
```

**Why it works:**
- Clearly states the agent's purpose and capabilities
- Specifies the implementation pattern to use
- Identifies integration requirements
- Provides concrete scope boundaries

### Agent File Validation

**Good Prompt:**
```
Validate the agent file at .claude/agents/security-audit.md for:
- YAML frontmatter compliance
- Tool assignment appropriateness
- Integration with existing security-related agents
- Color uniqueness in the ecosystem

Fix any issues found and ensure Task tool compatibility.
```

**Why it works:**
- Specifies exact validation requirements
- Requests specific checks
- Includes remediation instructions
- Ensures end-to-end functionality

### Ecosystem Integration

**Good Prompt:**
```
Review the existing agent ecosystem and create a new performance-monitoring agent that:
- Doesn't overlap with existing monitoring capabilities
- Integrates smoothly with production-ops and testing-specialist
- Uses appropriate analysis pattern tools
- Includes clear handoff protocols

Ensure no color conflicts and validate all integration points.
```

**Why it works:**
- Acknowledges ecosystem context
- Specifies collaboration requirements
- Requests conflict prevention
- Ensures comprehensive integration

## Common Patterns and Templates

### Pattern 1: Technical Specialist
Best for agents focused on core development, testing, or operations.

**Typical Tools:** `Glob, Grep, LS, Read, Edit, MultiEdit, Write, TodoWrite`

**Example Use Cases:**
- API development specialist
- Database optimization expert
- Security scanning agent

### Pattern 2: Content Specialist
Best for documentation, writing, and content strategy agents.

**Typical Tools:** `Read, Edit, MultiEdit, Write, WebFetch, TodoWrite`

**Example Use Cases:**
- API documentation writer
- User guide creator
- Release notes generator

### Pattern 3: Coordination Specialist
Best for workflow orchestration and project management.

**Typical Tools:** `Task, TodoWrite, LS, Read, Edit, Write`

**Example Use Cases:**
- Sprint planning coordinator
- Deployment orchestrator
- Code review manager

### Pattern 4: Analysis Specialist
Best for investigation, monitoring, and reporting.

**Typical Tools:** `Glob, Grep, Read, WebFetch, TodoWrite`

**Example Use Cases:**
- Performance analyzer
- Code quality auditor
- Dependency scanner

## Troubleshooting Guide

### Common Issues and Solutions

| Problem | Solution |
|---------|----------|
| **Agent won't load in Claude Code** | Check YAML frontmatter for missing required fields |
| **Agent can't perform stated capabilities** | Verify tool assignments match required operations |
| **Conflicts with existing agents** | Review scope boundaries and refine agent purpose |
| **Task tool can't invoke agent** | Ensure file location is `.claude/agents/` and name matches |
| **Color already in use** | Check existing agents and select unique color |

### Validation Checklist

Before submitting an agent file, ensure:

**Pre-Creation:**
- [ ] File will be in `.claude/agents/` directory
- [ ] Filename uses kebab-case with `.md` extension
- [ ] All YAML fields are present and valid
- [ ] Agent name matches filename (without .md)
- [ ] Description includes "Use for..." clause
- [ ] Tools appropriate for agent domain
- [ ] Color is unique in ecosystem
- [ ] Content provides sufficient operational detail

**Post-Creation:**
- [ ] YAML parses without errors
- [ ] Agent loads via Task tool
- [ ] No conflicts with existing agents
- [ ] Documentation follows conventions
- [ ] Clear scope and handoff criteria

## Best Practices

### 1. Always Start with Design
Never use claude-agent-builder directly for conceptual work. First use agent-design-architect to create a clear specification, then implement with claude-agent-builder.

### 2. Use Established Patterns
Don't reinvent the wheel. Use one of the four established patterns (Technical, Content, Coordination, Analysis) as your starting point.

### 3. Validate Early and Often
Run validation checks at each stage of development. It's easier to fix issues early than after full implementation.

### 4. Consider the Ecosystem
Always review existing agents before creating new ones. Look for:
- Potential overlaps in functionality
- Collaboration opportunities
- Tool assignment precedents
- Color availability

### 5. Document Integration Points
Clearly specify how your agent works with others:
- Input requirements from other agents
- Output formats for downstream agents
- Handoff criteria and protocols
- Communication standards

## Advanced Usage

### Custom Implementation Patterns
While the four standard patterns cover most use cases, you can create hybrid patterns:

```yaml
# Hybrid Analysis-Coordination Pattern
tools: [Task, TodoWrite, Glob, Grep, Read, WebFetch]
```

### Multi-Agent Workflow Integration
When creating agents that participate in complex workflows:

1. Define clear input/output contracts
2. Specify synchronous vs asynchronous operations
3. Document error handling and fallback behaviors
4. Include performance expectations

### Dynamic Tool Assignment
For agents with varying operational modes:

```markdown
## Operational Modes
### Investigation Mode
Tools: Glob, Grep, Read

### Implementation Mode
Tools: Edit, MultiEdit, Write

### Validation Mode
Tools: Task, TodoWrite
```

## Performance Optimization

### Tool Selection Efficiency
- Include only necessary tools (each tool adds overhead)
- Group related tools for common operations
- Consider tool initialization costs
- Balance capability with performance

### Description Optimization
- Keep descriptions concise but complete
- Include specific trigger keywords for Task tool selection
- Avoid ambiguous scope statements
- Use clear action verbs ("analyzes", "creates", "validates")

### Integration Streamlining
- Minimize handoff complexity
- Use standard communication formats
- Avoid circular dependencies
- Implement clear termination conditions

## Working with Agent Design Architect

The claude-agent-builder works best in partnership with agent-design-architect:

### Division of Labor

| agent-design-architect | claude-agent-builder |
|------------------------|----------------------|
| Strategic design | Technical implementation |
| Scope definition | File creation |
| Capability planning | Tool assignment |
| Workflow architecture | Integration testing |
| Performance metrics | Validation compliance |

### Handoff Protocol

When receiving specifications from agent-design-architect:

1. **Review completeness** of specification
2. **Map capabilities** to tool requirements
3. **Identify integration** points with existing agents
4. **Implement** using appropriate pattern
5. **Validate** all technical requirements
6. **Report** implementation status back

## Metrics for Success

### Technical Metrics
- **Zero YAML errors** in created files
- **100% Task tool compatibility**
- **No ecosystem conflicts**
- **Complete validation checklist**

### User Experience Metrics
- **Time to working agent:** < 30 minutes
- **First-attempt success rate:** > 95%
- **Integration success:** 100%
- **Documentation clarity:** Self-sufficient

### Business Impact Metrics
- **Development velocity:** 3-5x faster
- **Quality consistency:** 100% compliance
- **Reduced technical debt:** Standardized implementation
- **Team productivity:** Focus on logic, not plumbing

## Appendix: System Prompt

Below is the complete system prompt for the claude-agent-builder agent:

---

```yaml
---
name: claude-agent-builder
description: Technical specialist in Claude Code agent implementation, file format validation, and agent ecosystem integration. Use for creating properly formatted agent files, validating YAML frontmatter, implementing agent specifications, ensuring directory structure compliance, and integrating new agents into the existing ecosystem.
tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, TodoWrite
model: sonnet
color: cyan
---
```

# Claude Agent Builder

You are a **Claude Agent Builder** - a technical specialist focused on the practical implementation of Claude Code agents. You transform high-level agent designs into properly formatted, technically compliant agent files that integrate seamlessly with the Claude Code ecosystem.

## Core Technical Expertise

### Claude Code Agent File Format Mastery
- **YAML Frontmatter Validation**: Ensure all required fields are present and correctly formatted
- **File Structure Compliance**: Validate proper directory placement and naming conventions
- **Integration Testing**: Verify agents work correctly with Claude Code's Task tool
- **Ecosystem Compatibility**: Ensure new agents integrate smoothly with existing agent patterns

### Specialized Technical Knowledge
- **Required File Location**: `.claude/agents/` directory (absolute requirement)
- **File Naming Convention**: kebab-case `.md` files (e.g., `my-specialist-agent.md`)
- **YAML Schema Validation**: Strict adherence to Claude Code agent specification
- **Tool Assignment Optimization**: Matching tools to agent capabilities and workflows

[System prompt continues with full technical specification...]

---

*Note: The complete system prompt is available in `.claude/agents/claude-agent-builder.md`*
