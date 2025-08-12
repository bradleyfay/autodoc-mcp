# MkDocs Linking Patterns Guide

This guide documents the correct linking patterns for this MkDocs site to ensure all internal navigation works properly.

## 🔗 Internal Linking Standards

### Basic Principle
MkDocs converts `.md` files into directories, so use `.md` extensions in your links, not directory paths.

### ✅ Correct Patterns

#### Same Directory Links
```markdown
[Configuration Guide](configuration.md)
[API Reference](api-reference.md)
```

#### Parent Directory Links
```markdown
[Development Process](../development/contributing.md)
[Main Index](../index.md)
```

#### Subdirectory Links
```markdown
[Phase 1](phases/phase-1-core-validation.md)
[Sessions](sessions.md)
```

#### Cross-Section Links
```markdown
<!-- From product/ to development/ -->
[Contributing Guide](../development/contributing.md)

<!-- From journey/phases/ to journey/ -->
[Development Journey](../index.md)

<!-- From docs root to any section -->
[Product Docs](product/index.md)
```

### ❌ Incorrect Patterns (Cause 404s)

```markdown
<!-- Don't use directory paths -->
[Bad Link](../product/)
[Bad Link](product/getting-started/)

<!-- Don't use absolute paths -->
[Bad Link](/product/getting-started.md)

<!-- Don't use relative paths without .md -->
[Bad Link](getting-started)
```

## 📁 Site Structure Understanding

### File System vs Generated URLs

| File Path | Generated URL | Link Format |
|-----------|---------------|-------------|
| `docs/index.md` | `/` | `index.md` |
| `docs/product/index.md` | `/product/` | `product/index.md` |
| `docs/product/getting-started.md` | `/product/getting-started/` | `product/getting-started.md` |
| `docs/journey/phases/phase-1.md` | `/journey/phases/phase-1/` | `journey/phases/phase-1.md` |

### HTML Links in Markdown
When using HTML `<a>` tags, you can use either:
```html
<!-- .md extension (recommended) -->
<a href="product/index.md">Product Docs</a>

<!-- Directory path (works but not preferred) -->
<a href="product/">Product Docs</a>
```

## 🧪 Testing Links

### During Development
```bash
# Build with warnings for broken links
mkdocs build --clean

# Serve locally to test navigation
mkdocs serve
```

### Link Validation
MkDocs will warn about unrecognized relative links during build:
```
INFO - Doc file 'index.md' contains an unrecognized relative link '../product/',
       it was left as is. Did you mean 'product/index.md'?
```

## 🔧 Common Scenarios

### Navigation Cards (HTML)
```html
<div class="doc-card">
  <h3>Getting Started</h3>
  <p>Quick setup guide</p>
  <a href="getting-started.md">Start Here →</a>
</div>
```

### Cross-References in Text
```markdown
For installation instructions, see the [Installation Guide](installation.md).

To contribute to the project, check out our [Contributing Guide](../development/contributing.md).
```

### Breadcrumb Navigation
```markdown
*This documentation is part of the [Development Journey](../index.md).*
```

### "Next/Previous" Links
```markdown
**Next**: [Phase 2](phase-2-documentation-fetching.md) - Building the documentation engine.
```

## ⚡ Quick Reference

### From Root (`docs/index.md`):
- Same level: `filename.md`
- To section: `section/filename.md`

### From Section (`docs/section/index.md`):
- Same section: `filename.md`
- To root: `../index.md`
- To other section: `../other-section/filename.md`

### From Subsection (`docs/section/sub/filename.md`):
- Same sub: `other-file.md`
- Parent section: `../index.md`
- Root: `../../index.md`
- Other section: `../../other-section/filename.md`

## 🐛 Troubleshooting

### "Unrecognized relative link" Warnings
- Check that the target file exists
- Verify the path is correct relative to the source file
- Ensure you're using `.md` extension

### 404 Errors on Generated Site
- Links may be correct in Markdown but broken in generated HTML
- Test with `mkdocs serve` locally
- Check browser developer tools for actual requested URLs

## 📋 Checklist for New Documentation

- [ ] All internal links use `.md` extensions
- [ ] Paths are relative to the current file's location
- [ ] Links tested with `mkdocs build --clean`
- [ ] Navigation tested with `mkdocs serve`
- [ ] No "unrecognized relative link" warnings
- [ ] All referenced files exist in the expected locations

---

*This guide ensures consistent, working navigation throughout the AutoDocs MCP Server documentation site.*
