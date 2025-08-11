# AutoDocs Documentation Style Guide

## Overview

This style guide ensures consistency, clarity, and user-centeredness across all AutoDocs MCP Server documentation. It follows the **Diátaxis framework** for documentation architecture and establishes editorial standards for content excellence.

## Editorial Standards

### Voice and Tone

**Voice**: Professional yet approachable, technically accurate but not intimidating
**Tone Variations by Content Type**:

- **Tutorials**: Encouraging, step-by-step, confidence-building
- **How-to Guides**: Direct, solution-focused, practical
- **Explanation**: Thoughtful, contextual, illuminating
- **Reference**: Precise, comprehensive, factual

### Writing Style

#### Clarity Principles
- **Active voice preferred**: "AutoDocs fetches documentation" not "Documentation is fetched by AutoDocs"
- **Present tense**: "The system provides..." not "The system will provide..."
- **Second person for instructions**: "You can install..." not "One can install..."
- **Specific over generic**: "3-5 second response time" not "fast response time"

#### Technical Language
- **Define technical terms** on first use with brief explanations
- **Use consistent terminology** throughout (see Glossary section)
- **Avoid unnecessary jargon** - prefer clear, direct language
- **Include context** for technical decisions and choices

### Content Structure

#### Hierarchy Standards
```
# Page Title (H1) - One per page
## Major Section (H2) - Main content divisions
### Subsection (H3) - Detailed breakdowns
#### Minor Section (H4) - Specific details (use sparingly)
```

#### Information Architecture
1. **Lead with value** - Start with what the user gains
2. **Progressive disclosure** - Simple concepts first, complexity later
3. **Logical grouping** - Related information stays together
4. **Clear transitions** - Connect sections with contextual bridges

## Content Type Templates

### Tutorial Template

```markdown
# [Task] Tutorial

[Brief description of what users will learn and build]

## Prerequisites
- Prerequisite 1 (with link if needed)
- Prerequisite 2

## What You'll Build
[Clear description of the end result]

## Step 1: [Action-oriented title]
[Explanation of why this step matters]

[Code example or configuration]

**Expected result**: [What users should see]

## Step 2: [Next action]
[Continue pattern...]

## Verification
[How users can confirm success]

## Next Steps
- Link to related how-to guides
- Link to reference documentation
- Suggestion for further learning
```

### How-to Guide Template

```markdown
# How to [Specific Task]

**Problem**: [Brief description of what this solves]
**Solution time**: [Estimated time to complete]

## Prerequisites
- Brief list of requirements

## Solution
### Quick Version
[For experienced users - direct steps]

### Detailed Steps
1. **[Action]**: [Explanation and code]
2. **[Action]**: [Explanation and code]

## Troubleshooting
**Issue**: [Common problem]
**Solution**: [Fix with explanation]

## Related Tasks
- [Link to related how-to]
- [Link to reference docs]
```

### Explanation Template

```markdown
# Understanding [Concept]

**Why this matters**: [Brief value statement]

## Core Concepts
[High-level explanation of the main ideas]

## How It Works
[Detailed explanation with examples]

## Design Decisions
### Why [Decision X]?
[Rationale with alternatives considered]

## Implications and Benefits
[What this means for users]

## Related Topics
[Links to other explanation articles]
```

### Reference Template

```markdown
# [Feature] Reference

## Overview
[Brief functional description]

## Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| param1 | string | Yes | - | Detailed description |

## Response Format
```json
{
  "example": "response structure"
}
```

## Examples
### Basic Usage
[Simple example with explanation]

### Advanced Usage
[Complex example with explanation]

## Error Handling
| Error Code | Description | Solution |
|------------|-------------|----------|
| ERR001 | Error description | How to fix |

## See Also
- [Related reference pages]
- [How-to guides using this feature]
```

## Visual Communication Standards

### Code Examples
- **Always complete and executable** - no partial snippets without context
- **Include expected output** when relevant
- **Provide explanations** for non-obvious code
- **Use consistent formatting** with syntax highlighting

#### Code Block Standards
```bash
# Commands include comments for clarity
uv tool install autodoc-mcp  # Install globally with uv

# Show expected output when helpful
autodoc-mcp --version
# Output: AutoDocs MCP Server v0.5.1
```

### Visual Hierarchy

#### Callout Usage
```markdown
!!! tip "Pro Tip"
    Use for helpful suggestions and best practices

!!! warning "Important"
    Use for critical information users must know

!!! note "Context"
    Use for additional background information

!!! example "Example"
    Use for concrete examples and demonstrations
```

#### Status Indicators
- ✅ **Complete/Working**: Green for success states
- ⚠️ **Warning/Caution**: Yellow for important notices
- ❌ **Error/Issue**: Red for problems and failures
- 🚀 **New/Featured**: Blue for highlighting important features
- 📊 **Data/Stats**: For performance and metrics

### Content Organization

#### Section Structure
1. **Value statement** - Why this section matters
2. **Core content** - The main information
3. **Examples** - Concrete demonstrations
4. **Next steps** - Where to go from here

#### Information Density
- **One concept per paragraph** - Keep ideas focused
- **Short paragraphs** - Maximum 4-5 sentences
- **Bulleted lists** for parallel information
- **Numbered lists** for sequential steps

## Terminology and Glossary

### Consistent Terms
- **AutoDocs MCP Server** (full name) or **AutoDocs** (short name)
- **MCP client** not "client application"
- **Package documentation** not "docs"
- **Dependency context** not "dependency information"
- **Cache hit/miss** for performance references
- **Version constraint** not "version specification"

### Technical Accuracy
- Specify exact version numbers when relevant
- Include performance metrics with context
- Reference specific error codes and messages
- Use precise timing estimates (3-5 seconds, not "quickly")

## Cross-Linking Strategy

### Internal Links
- **Contextual links** within content flow
- **Reference hub pages** for comprehensive navigation
- **Related sections** at end of articles
- **Bidirectional linking** between related topics

### Link Patterns
```markdown
- [Tutorial link](tutorial.md) - Learn by doing
- [How-to guide](howto.md) - Solve specific problems
- [Explanation](explanation.md) - Understand the concepts
- [Reference](reference.md) - Look up specifics
```

### Navigation Aids
- **Breadcrumb context** in page headers
- **Progress indicators** for multi-step processes
- **Quick reference** cards for common tasks
- **Search-friendly** headers and content

## Quality Standards

### Content Review Checklist
- [ ] **Audience appropriate**: Matches intended user level
- [ ] **Diátaxis compliant**: Fits framework category correctly
- [ ] **Actionable**: Users can successfully complete described tasks
- [ ] **Current**: All code examples and references work
- [ ] **Complete**: No missing prerequisites or assumptions
- [ ] **Consistent**: Follows style guide standards
- [ ] **Accessible**: Clear language, good contrast, logical flow

### Performance Standards
- **Reading level**: Aim for grade 8-10 level for technical content
- **Scan-ability**: Headers, bullets, and visual breaks every 3-4 paragraphs
- **Mobile-friendly**: Test on mobile devices for readability
- **Load time**: Optimize images and media for fast loading

## Content Maintenance

### Update Procedures
1. **Version alignment**: Update docs with each software release
2. **Link validation**: Regular checks for broken internal/external links
3. **User feedback integration**: Regular review and response to user issues
4. **Performance monitoring**: Track user behavior and content effectiveness

### Ownership and Review
- **Technical accuracy**: Developer review required for API changes
- **Editorial quality**: Style guide compliance review
- **User experience**: Usability testing for new content
- **Accessibility**: Regular accessibility audits

---

This style guide is a living document. Update it as we learn more about user needs and content effectiveness. Quality documentation is not just about following rules—it's about genuinely helping users succeed.
