# Diátaxis Framework Content Templates

## Overview

These templates implement the Diátaxis documentation framework for AutoDocs, ensuring each content type serves its specific user needs: learning (tutorials), problem-solving (how-to guides), understanding (explanation), and information-seeking (reference).

## Framework Principles Summary

| Type | Purpose | User Need | Content Focus | Success Metric |
|------|---------|-----------|---------------|----------------|
| **Tutorial** | Learning-oriented | "Teach me" | Guided practice | User completes successfully |
| **How-to Guide** | Problem-oriented | "Show me how" | Practical solutions | User solves specific problem |
| **Explanation** | Understanding-oriented | "Help me understand" | Theoretical knowledge | User gains comprehension |
| **Reference** | Information-oriented | "Tell me facts" | Accurate specifications | User finds needed information |

---

## TUTORIAL TEMPLATES

### Template: Basic Tutorial Structure

```markdown
# [Action] Tutorial: [What Users Will Build/Learn]

> **Learning Goal**: By the end of this tutorial, you'll have [specific, measurable outcome].
> **Time Required**: [X] minutes
> **Difficulty**: Beginner | Intermediate | Advanced

## What You'll Build

[Clear description of the end result with a screenshot or example if applicable]

## Prerequisites

Before starting, make sure you have:
- [Prerequisite 1] - [Link to setup if needed]
- [Prerequisite 2] - [Brief explanation if complex]
- [Basic knowledge requirement] - No link needed for basics

## Overview

In this tutorial, you'll:
1. [High-level step 1]
2. [High-level step 2]
3. [High-level step 3]
4. [Verify everything works]

Let's get started!

---

## Step 1: [Action-Oriented Title]

[Brief explanation of why this step matters and what it accomplishes]

### What to Do
```bash
# Clear, complete commands with comments
command-with-explanation  # What this does
```

### What to Expect
[Describe exactly what users should see after running the command]

```
Expected output:
[Show actual output they should see]
```

### If Something Goes Wrong
**Issue**: [Common problem that might occur]
**Solution**: [Quick fix] or [link to troubleshooting section]

---

## Step 2: [Next Action]

[Continue the pattern...]

---

## Verification: Confirm Everything Works

Let's make sure everything is working correctly:

1. **Test [Function 1]**:
   ```bash
   [verification command]
   ```
   ✅ **Expected**: [What success looks like]

2. **Test [Function 2]**:
   ```bash
   [verification command]
   ```
   ✅ **Expected**: [What success looks like]

## 🎉 Congratulations!

You've successfully [accomplished goal]! You now have:
- [Achievement 1]
- [Achievement 2]
- [Achievement 3]

## What's Next?

**Ready for more?**
- [Related tutorial] - Build on what you've learned
- [How-to guide] - Solve specific problems with what you built
- [Reference documentation] - Look up specific details

**Want to understand more?**
- [Explanation article] - Learn why this works the way it does

## Troubleshooting

### Common Issues

#### Issue: [Specific problem]
**Symptoms**: [What users will see]
**Cause**: [Brief explanation]
**Solution**:
```bash
[Fix commands]
```

#### Issue: [Another problem]
[Same structure...]

## Summary

In this tutorial, you learned how to:
- [Skill 1 with link to relevant how-to guide]
- [Skill 2 with link to reference docs]
- [Skill 3 with link to explanation]

You're now ready to [next logical step in learning journey].
```

### Example Tutorial: "Your First AutoDocs Integration"

```markdown
# Integration Tutorial: Get AutoDocs Running with Your AI Assistant

> **Learning Goal**: By the end of this tutorial, you'll have AutoDocs providing intelligent documentation context to your AI assistant.
> **Time Required**: 10 minutes
> **Difficulty**: Beginner

## What You'll Build

A working AutoDocs MCP Server integration that:
- Automatically provides package documentation to your AI assistant
- Includes smart dependency context (3-8 related packages)
- Delivers sub-second responses for cached packages

## Prerequisites

Before starting, make sure you have:
- **Python 3.11+** - [Installation guide](https://python.org/downloads/)
- **MCP-compatible AI client** - Claude Desktop, Cursor, or Claude Code
- **5 minutes** - This tutorial is designed for quick success

## Overview

In this tutorial, you'll:
1. Install AutoDocs MCP Server
2. Configure your AI client
3. Test the integration with real queries
4. Verify intelligent context delivery

Let's get started!

---

## Step 1: Install AutoDocs

We'll install AutoDocs globally so it's available to all your AI clients.

### What to Do
```bash
# Install with uv (fastest and most reliable)
uv tool install autodoc-mcp

# Verify installation
autodoc-mcp --version
```

### What to Expect
```
AutoDocs MCP Server v0.5.1
8 MCP tools available
```

### If Something Goes Wrong
**Issue**: `command not found: autodoc-mcp`
**Solution**: Use pip instead: `pip install autodoc-mcp`

---

## Step 2: Configure Your AI Client

Choose your AI client and add the AutoDocs configuration:

### What to Do

=== "Claude Desktop"
    Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
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

=== "Cursor"
    In Cursor settings → Rules for AI → MCP Servers:
    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp"
        }
      }
    }
    ```

### What to Expect
- No immediate visual change
- Your AI client will load AutoDocs tools on next restart

---

## Step 3: Test the Integration

Let's verify AutoDocs is working with some test queries.

### What to Do
1. **Restart your AI client** (important!)
2. **Ask your AI assistant**: "What packages are available in this project?"

### What to Expect
Your AI should:
- Use the `scan_dependencies` tool automatically
- Show you a list of dependencies from pyproject.toml
- Respond within 1-2 seconds

### If Something Goes Wrong
**Issue**: AI says "no tools available" or similar
**Solution**: Double-check your configuration file syntax and restart the AI client

---

## Step 4: Test Smart Context Delivery

Now let's test the main AutoDocs feature - intelligent documentation context.

### What to Do
**Ask your AI assistant**: "Tell me about the FastAPI package with its dependencies"

### What to Expect
Your AI should:
- Use the `get_package_docs_with_context` tool
- Take 3-5 seconds for first request (fetching from PyPI)
- Return comprehensive information about FastAPI AND related packages like:
  - Pydantic (data validation)
  - Starlette (ASGI framework)
  - Uvicorn (ASGI server)
- Show performance metrics at the end

---

## Verification: Confirm Everything Works

Let's make sure everything is working correctly:

1. **Test dependency scanning**:
   Ask: "What dependencies does this project have?"
   ✅ **Expected**: List of project dependencies with versions

2. **Test documentation context**:
   Ask: "Explain the requests library with its key dependencies"
   ✅ **Expected**: Detailed info about requests + urllib3, certifi, etc.

3. **Test cache performance**:
   Ask the same question again immediately
   ✅ **Expected**: Much faster response (< 100ms)

## 🎉 Congratulations!

You've successfully integrated AutoDocs with your AI assistant! You now have:
- Automatic package documentation lookup
- Smart dependency context for better AI responses
- Lightning-fast cached responses for repeated queries

## What's Next?

**Ready for more?**
- [Performance Optimization How-to](../product/configuration.md) - Configure AutoDocs for your workflow
- [MCP Tools Reference](../product/mcp-tools.md) - Learn about all 8 available tools

**Want to understand more?**
- [How AutoDocs Works](../development/architecture.md) - Technical deep dive
- [Smart Context Strategy](../journey/phases/phase-4-dependency-context.md) - Why context selection is intelligent

## Troubleshooting

### Common Issues

#### Issue: "No MCP tools available"
**Symptoms**: AI assistant doesn't recognize AutoDocs tools
**Cause**: Configuration file syntax error or AI client not restarted
**Solution**:
1. Validate JSON syntax in your config file
2. Restart your AI client completely
3. Check logs for specific error messages

#### Issue: Very slow responses
**Symptoms**: First requests take 10+ seconds
**Cause**: Network connectivity or PyPI API issues
**Solution**:
```bash
# Test network connectivity
curl https://pypi.org/pypi/requests/json
# Should return JSON response quickly
```

## Summary

In this tutorial, you learned how to:
- Install and configure AutoDocs MCP Server
- Test integration with your AI assistant
- Verify intelligent context delivery is working

You're now ready to use AutoDocs to enhance your AI-assisted development workflow!
```

---

## HOW-TO GUIDE TEMPLATES

### Template: How-to Guide Structure

```markdown
# How to [Accomplish Specific Task]

> **Problem Solved**: [Brief description of what this solves]
> **Time Required**: [X] minutes
> **Prerequisites**: [Brief list or "none"]

## Quick Summary

For experienced users, here's the essential steps:
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Need more details?** Continue reading for step-by-step instructions.

---

## The Problem

[Describe the specific problem this solves and when users encounter it]

**You'll know you need this when**:
- [Symptom 1]
- [Symptom 2]
- [Context where this problem occurs]

## The Solution

### Method 1: [Recommended approach]

**Best for**: [When to use this method]

```bash
# Step-by-step commands
command1  # Explanation
command2  # What this achieves
```

**Expected outcome**: [What success looks like]

### Method 2: [Alternative approach]

**Best for**: [Different use case]

[Same structure as Method 1]

---

## Verification

Confirm the solution worked:
```bash
[verification command]
```
✅ **Success**: [What you should see]

## Troubleshooting

**Problem**: [Issue that might occur]
**Solution**: [How to fix it]

**Problem**: [Another issue]
**Solution**: [Another fix]

## Related Tasks

Once you've solved this, you might also need:
- [How to do related thing] - [Brief description]
- [How to optimize this] - [Brief description]

## See Also

- [Reference documentation] for technical details
- [Tutorial] if you're new to this area
```

### Example How-to: "Optimize AutoDocs for Large Projects"

```markdown
# How to Optimize AutoDocs for Large Projects

> **Problem Solved**: Slow AutoDocs performance with projects that have many dependencies
> **Time Required**: 5 minutes
> **Prerequisites**: AutoDocs already installed and working

## Quick Summary

For experienced users:
1. Set `MAX_DEPENDENCY_CONTEXT="5"`
2. Set `MAX_CONCURRENT="15"`
3. Use project-specific cache directory
4. Enable smart scoping

**Need more details?** Continue reading for step-by-step instructions.

---

## The Problem

Large projects with 50+ dependencies can cause AutoDocs to:
- Take 10+ seconds for first requests
- Use excessive memory
- Overwhelm AI assistants with too much context

**You'll know you need this when**:
- Initial requests take longer than 10 seconds
- Your AI assistant mentions "context too large"
- You have projects with 30+ dependencies

## The Solution

### Method 1: Environment Variables (Recommended)

**Best for**: Global optimization across all projects

```bash
# Set optimal concurrency for large projects
export MAX_CONCURRENT="15"

# Limit dependency context to most relevant
export MAX_DEPENDENCY_CONTEXT="5"

# Use smart scoping (default, but explicit)
export CONTEXT_SCOPE="smart"

# Restart AutoDocs to apply settings
autodoc-mcp
```

**Expected outcome**: 2-5x faster responses, more focused context

### Method 2: MCP Configuration

**Best for**: Client-specific optimization

Edit your MCP configuration:
```json
{
  "mcpServers": {
    "autodoc-mcp": {
      "command": "autodoc-mcp",
      "env": {
        "MAX_CONCURRENT": "15",
        "MAX_DEPENDENCY_CONTEXT": "5",
        "CONTEXT_SCOPE": "smart",
        "CACHE_DIR": "~/.cache/autodoc-mcp-large"
      }
    }
  }
}
```

---

## Verification

Confirm the optimization worked:
```bash
# Test with a complex package
echo "Testing with Django (many dependencies):"
```

Ask your AI: "Tell me about Django with its dependencies"

✅ **Success**: Response in under 5 seconds with 3-5 key dependencies

## Troubleshooting

**Problem**: Still slow despite optimization
**Solution**: Check network connectivity and PyPI API status

**Problem**: Missing important dependencies in context
**Solution**: Increase `MAX_DEPENDENCY_CONTEXT` to 8 or use "runtime" scope

## Related Tasks

Once you've optimized performance, you might also need:
- [Monitor AutoDocs Performance](monitor-performance.md) - Track metrics over time
- [Configure Corporate Firewalls](corporate-setup.md) - Network optimization

## See Also

- [Configuration Reference](../product/configuration.md) for all available options
- [Architecture Explanation](../development/architecture.md) for how caching works
```

---

## EXPLANATION TEMPLATES

### Template: Explanation Structure

```markdown
# Understanding [Concept/System/Decision]

> **Purpose**: This article explains [concept] and why it matters for AutoDocs users.

## Why This Matters

[Brief explanation of why users should understand this concept]

**You'll benefit from understanding this if**:
- [Use case 1]
- [Use case 2]
- [Context where this knowledge helps]

---

## Core Concepts

### [Concept 1]
[Clear explanation with examples]

### [Concept 2]
[Continue pattern...]

## How It Works

[Detailed explanation of the mechanism/process]

### [Aspect 1]: [Subheading]
[Explanation with examples]

### [Aspect 2]: [Subheading]
[Continue pattern...]

## Design Decisions

### Why [Decision X]?

**The choice**: [What was decided]
**The alternatives**: [What else was considered]
**The reasoning**: [Why this choice was made]
**The trade-offs**: [What was gained and lost]

### Why [Decision Y]?
[Same structure...]

## Implications and Benefits

**For users, this means**:
- [Benefit 1] - [Concrete example]
- [Benefit 2] - [Concrete example]

**For developers, this enables**:
- [Technical benefit 1]
- [Technical benefit 2]

## Common Misconceptions

**Misconception**: [What people often think]
**Reality**: [What actually happens]
**Why the confusion**: [Source of misunderstanding]

## Related Concepts

This concept connects to:
- [Related explanation] - [How they relate]
- [Related tutorial] - [Learning application]
- [Related reference] - [Technical details]

## Further Reading

**To learn more about the technical implementation**:
- [Technical reference] - Deep technical details
- [Architecture documentation] - System context

**To see this in action**:
- [Tutorial] - Hands-on learning
- [How-to guide] - Practical application
```

### Example Explanation: "Understanding AutoDocs Smart Context System"

```markdown
# Understanding AutoDocs Smart Context System

> **Purpose**: This article explains how AutoDocs intelligently selects which dependencies to include in documentation context and why this matters for AI assistance quality.

## Why This Matters

AutoDocs doesn't just dump all available documentation at your AI assistant. It carefully curates which packages to include based on relevance, usage patterns, and AI model limitations.

**You'll benefit from understanding this if**:
- You want to understand why certain packages appear in responses
- You're optimizing AutoDocs performance for your workflow
- You're curious about the "intelligence" behind dependency selection

---

## Core Concepts

### Smart Scoping
AutoDocs analyzes dependency relationships and selects 3-8 most relevant packages rather than including everything.

**Example**: When you ask about FastAPI, you get:
- FastAPI (primary package)
- Pydantic (core dependency for data validation)
- Starlette (underlying ASGI framework)
- Uvicorn (common deployment server)

But NOT less relevant packages like:
- typing-extensions (internal utility)
- click (CLI tool, not web development)

### Context Relevance Scoring
Each potential dependency gets a relevance score based on:
- **Direct dependency weight**: Runtime deps score higher than dev deps
- **Popularity influence**: More downloaded packages get slight preference
- **Framework relationships**: Known framework patterns (FastAPI→Pydantic)
- **User patterns**: Commonly requested together packages

## How It Works

### Selection Process

1. **Parse Dependencies**: Extract all dependencies from package metadata
2. **Filter by Category**: Prioritize runtime over development dependencies
3. **Apply Framework Rules**: Include known important relationships
4. **Score Relevance**: Calculate importance score for each package
5. **Respect Token Budgets**: Select top packages within AI model limits
6. **Cache Results**: Store selections for consistent responses

### Context Scoping Levels

**"primary_only"**: Just the requested package
```json
{
  "packages": ["fastapi"],
  "total_packages": 1,
  "context_scope": "primary_only"
}
```

**"runtime"**: All runtime dependencies (can be 10-20 packages)
```json
{
  "packages": ["fastapi", "pydantic", "starlette", "anyio", ...],
  "total_packages": 15,
  "context_scope": "runtime"
}
```

**"smart"**: Intelligently selected subset (3-8 packages)
```json
{
  "packages": ["fastapi", "pydantic", "starlette", "uvicorn"],
  "total_packages": 4,
  "context_scope": "smart"
}
```

## Design Decisions

### Why Smart Scoping by Default?

**The choice**: Default to "smart" rather than "all dependencies"
**The alternatives**: Include all dependencies or just the primary package
**The reasoning**:
- AI models have context limits (typically 128K-200K tokens)
- Too much information can reduce response quality
- Most relevant dependencies provide 80% of the value
**The trade-offs**:
- Gained: Fast, focused responses that stay within model limits
- Lost: Occasional edge case dependencies might be missing

### Why Version-Specific Caching?

**The choice**: Cache documentation by exact version (e.g., "fastapi-0.104.1")
**The alternatives**: Cache by package name only or version ranges
**The reasoning**:
- Package versions are immutable - v0.104.1 never changes
- Enables permanent caching without expiration logic
- Ensures documentation matches exact installed versions
**The trade-offs**:
- Gained: Perfect cache reliability, no stale documentation
- Lost: Slightly larger cache sizes for multiple versions

## Implications and Benefits

**For users, this means**:
- **Faster responses**: 3-5 seconds instead of 10+ seconds for comprehensive context
- **Better AI answers**: Focused context leads to more accurate responses
- **Consistent experience**: Same packages selected each time for same query

**For developers, this enables**:
- **Scalable architecture**: System works well with large dependency trees
- **Configurable behavior**: Can adjust context scope based on needs
- **Performance optimization**: Parallel fetching of selected subset

## Common Misconceptions

**Misconception**: "AutoDocs should include ALL dependencies for completeness"
**Reality**: AI models perform better with curated, relevant context than exhaustive information
**Why the confusion**: More information seems better, but AI context windows and attention mechanisms work differently

**Misconception**: "Smart scoping might miss important dependencies"
**Reality**: The algorithm specifically targets framework relationships and common usage patterns
**Why the confusion**: Users worry about edge cases but the system optimizes for common scenarios

## Related Concepts

This concept connects to:
- [Caching Strategy](caching-strategy.md) - How selected context gets stored
- [Performance Tutorial](../product/getting-started.md#performance-tips) - Optimizing context selection
- [Configuration Reference](../product/configuration.md) - Controlling context scope settings

## Further Reading

**To learn more about the technical implementation**:
- [Context Fetcher Architecture](../development/architecture.md#context-fetcher) - Code-level details
- [Phase 4 Development Story](../journey/phases/phase-4-dependency-context.md) - How this was built

**To see this in action**:
- [Getting Started Tutorial](../product/getting-started.md) - Experience smart context
- [Optimize Performance How-to](optimize-performance.md) - Configure context settings
```

---

## REFERENCE TEMPLATES

### Template: Reference Documentation Structure

```markdown
# [Feature/Tool/API] Reference

> **Quick Reference**: [One-line description of what this documents]

## Overview

[Brief functional description - what it does, not how to use it]

**Key Information**:
- **Type**: [Tool/API/Configuration/etc.]
- **Availability**: [When/where available]
- **Related**: [Links to main related items]

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `param1` | string | ✅ | - | [Detailed description] |
| `param2` | integer | ❌ | 10 | [Detailed description with constraints] |
| `param3` | boolean | ❌ | false | [Detailed description] |

### Parameter Details

#### `param1` (string, required)
[Extended description if needed]
- **Valid values**: [constraints]
- **Example**: `"example-value"`

#### `param2` (integer, optional, default: 10)
[Extended description]
- **Range**: [min-max values]
- **Performance impact**: [if relevant]

---

## Response Format

```json
{
  "field1": "string",
  "field2": 123,
  "nested_object": {
    "sub_field": "value"
  },
  "array_field": ["item1", "item2"]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `field1` | string | [Description] |
| `field2` | integer | [Description] |
| `nested_object` | object | [Description] |
| `nested_object.sub_field` | string | [Description] |

---

## Examples

### Basic Usage
```json
{
  "param1": "simple-example",
  "param2": 5
}
```

**Response**:
```json
{
  "field1": "result",
  "field2": 200
}
```

### Advanced Usage
```json
{
  "param1": "complex-example",
  "param2": 20,
  "param3": true
}
```

**Response**:
```json
{
  "field1": "advanced-result",
  "field2": 500,
  "nested_object": {
    "sub_field": "additional-data"
  }
}
```

---

## Error Handling

| Error Code | HTTP Status | Description | Solution |
|------------|-------------|-------------|----------|
| `ERR_001` | 400 | Invalid parameter value | [How to fix] |
| `ERR_002` | 500 | Internal processing error | [How to fix] |

### Error Response Format
```json
{
  "error": {
    "code": "ERR_001",
    "message": "Human readable error",
    "details": "Additional context"
  }
}
```

---

## Performance Notes

- **Response time**: [typical performance]
- **Rate limits**: [if applicable]
- **Resource usage**: [memory/CPU considerations]

## Version History

| Version | Changes |
|---------|---------|
| v0.5.0 | Initial release |
| v0.5.1 | Added `param3` option |

## See Also

- **Tutorials**: [How to learn this]
- **How-to Guides**: [How to solve problems with this]
- **Explanations**: [How to understand this better]
- **Related References**: [Related technical docs]
```

---

## CONTENT TYPE DECISION MATRIX

Use this matrix to determine which template to use:

| User Says... | User Needs... | Content Type | Template |
|--------------|---------------|--------------|----------|
| "How do I..." | Step-by-step guidance | Tutorial | Tutorial Template |
| "I want to solve..." | Problem solution | How-to Guide | How-to Template |
| "Why does..." | Understanding | Explanation | Explanation Template |
| "What are the parameters for..." | Factual information | Reference | Reference Template |

## Template Usage Guidelines

### Before Writing Any Content

1. **Identify user intent**: What is the user trying to accomplish?
2. **Choose appropriate type**: Use the decision matrix above
3. **Check existing content**: Avoid duplication, build on existing material
4. **Plan cross-links**: How does this connect to other content?

### Quality Checklist

- [ ] **Type appropriate**: Content serves the right user need
- [ ] **Complete**: All necessary information is present
- [ ] **Tested**: All code examples work correctly
- [ ] **Linked**: Connected to related content appropriately
- [ ] **Accessible**: Clear language, good structure, mobile-friendly
- [ ] **Current**: Information is up-to-date and accurate

### Maintenance Process

1. **Regular review**: Check accuracy every quarter
2. **User feedback integration**: Update based on user reports
3. **Version alignment**: Update with software releases
4. **Link validation**: Verify internal/external links work

---

These templates ensure consistent, user-centered documentation that follows Diátaxis principles while serving the specific needs of AutoDocs users across different contexts and skill levels.
