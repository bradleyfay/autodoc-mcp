# Agent Context Architecture

**Purpose**: Define how AI agents access and share context across the multi-project ecosystem
**Scope**: Context management for AI development agents working across projects
**Updated**: August 11, 2025

## 🤖 Agent Context Management Philosophy

### Core Principles
- **Project Autonomy**: Each project maintains its own specific context in CLAUDE.md
- **Shared Foundation**: Common knowledge and standards accessible to all agents
- **Context Clarity**: Clear boundaries between project-specific and shared context
- **Documentation as Code**: All context is version-controlled and deployable

### Context Hierarchy
```
Shared Context (All Agents)
├── Development Standards & Conventions
├── Technology Stack Decisions
├── Quality & Testing Standards
├── Architecture Patterns
└── Integration Protocols

Project-Specific Context (Per-Project Agents)
├── Project Goals & Scope
├── Technical Implementation Details
├── Project-Specific Standards
├── Current Status & Priorities
└── Historical Context & Decisions
```

---

## 📁 Shared Context Repository

### What All Agents Need to Know

#### Development Standards (Cross-Project)
- **Code Quality**: Ruff formatting, MyPy type checking, pre-commit hooks
- **Testing Patterns**: pytest ecosystem, >90% coverage, pytest-mock patterns
- **Documentation**: Markdown standards, API documentation requirements
- **Version Control**: Conventional commits, GitFlow branching, semantic versioning

#### Technology Stack (Cross-Project)
- **Python Ecosystem**: Python 3.12+, uv package management, FastAPI/FastMCP
- **Quality Tools**: Ruff, MyPy, pytest ecosystem, pre-commit
- **Deployment**: PyPI packages, GitHub Actions CI/CD
- **Monitoring**: Health checks, structured logging, metrics collection

#### Architecture Patterns (Cross-Project)
- **MCP Protocol**: Standard for AI tool integration
- **Async Design**: Full async/await patterns for scalability
- **Error Handling**: Graceful degradation, structured error responses
- **Security**: Input validation, secure error handling, dependency scanning

---

## 🎯 Project-Specific Context Boundaries

### AutoDocs MCP Server Context
**Unique Knowledge**:
- PyPI API integration patterns
- Documentation caching strategies
- MCP tool implementation specifics
- Production monitoring and reliability patterns

**Shared with Other Projects**:
- MCP protocol expertise
- Python async patterns
- Testing and quality standards

### Documentation Site Context
**Unique Knowledge**:
- Content strategy and information architecture
- Static site generation and deployment
- User experience and content optimization

**Shared with Other Projects**:
- Web development standards
- Documentation writing principles
- Deployment and CI/CD patterns

### Task Graph System Context
**Unique Knowledge**:
- Multi-agent coordination patterns
- AI agent communication protocols
- Research methodology and experimentation

**Shared with Other Projects**:
- AI integration patterns
- Research and prototyping approaches
- Architecture design principles

---

## 🔄 Context Sharing Mechanisms

### CLAUDE.md Integration
Each project's `CLAUDE.md` file contains:
- **Project-Specific Instructions**: Unique to that project's needs
- **Shared Context References**: Links to cross-project standards and patterns
- **Integration Points**: How this project connects with others

### Cross-Project Knowledge Base
Located in `planning/cross-project/`:
- **Standards Documentation**: Accessible to all project agents
- **Technology Decisions**: Shared technology stack and rationale
- **Architecture Patterns**: Reusable design patterns and solutions
- **Best Practices**: Lessons learned and proven approaches

### Documentation Site Context
The planning folder serves as source material for:
- **Public Documentation**: Human-readable project descriptions and architecture
- **Agent Training Data**: Examples and patterns for future AI agent training
- **Community Resource**: Open source community reference and contribution guide

---

## 📊 Context Management Strategies

### Avoiding Context Duplication
- **Single Source of Truth**: Each piece of knowledge has one authoritative location
- **Reference Pattern**: Projects reference shared context rather than duplicating
- **Consistent Updates**: Changes to shared context automatically benefit all projects

### Context Evolution
- **Version Control**: All context changes tracked in Git
- **Change Impact**: Consider how context changes affect all projects
- **Migration Strategy**: Plan for updating project-specific context when shared context evolves

### Agent Onboarding
When agents work on new projects:
1. **Read Shared Context**: Understand cross-project standards and patterns
2. **Read Project Context**: Understand specific project goals and implementation
3. **Identify Integration Points**: Understand how this project connects with others
4. **Apply Consistent Patterns**: Use shared patterns while respecting project uniqueness

---

## 🏗️ Implementation Architecture

### Directory Structure for Agents
```
planning/
├── cross-project/                 # Shared agent context
│   ├── development_standards.md   # How to write code across all projects
│   ├── technology_stack.md        # Shared technology decisions and rationale
│   ├── architecture_patterns.md   # Reusable design patterns
│   └── integration_protocols.md   # How projects connect and share functionality
├── projects/                      # Project-specific agent context
│   ├── autodocs-mcp/CLAUDE.md    # Project-specific agent instructions
│   ├── documentation-site/CLAUDE.md # Project-specific agent instructions
│   └── task-graph-system/CLAUDE.md  # Project-specific agent instructions
└── PUBLIC_DOCUMENTATION/          # Human-readable docs site content
```

### Context Access Pattern
1. **Agent starts on project** → reads project's CLAUDE.md
2. **CLAUDE.md references** → cross-project standards and patterns
3. **Agent applies** → consistent patterns with project-specific adaptation
4. **Agent contributes** → improvements to shared context when applicable

---

## 🌐 Documentation Site Architecture

### Site Content Strategy
The planning folder content is structured for deployment as a documentation site:

**Target Audience**:
- Developers interested in the projects
- AI researchers studying multi-agent systems
- Open source contributors
- Future AI agents learning from examples

**Content Organization**:
- **Project Overviews**: High-level descriptions and current status
- **Architecture Documentation**: Technical system designs and patterns
- **Development Philosophy**: Principles and approaches that guide development
- **Standards and Conventions**: How code is written and projects are managed

### Site Structure
```
docs/
├── index.md                    # Portfolio overview and navigation
├── projects/                   # Individual project documentation
│   ├── autodocs-mcp/          # AutoDocs project docs
│   ├── documentation-site/    # Documentation project docs
│   └── task-graph-system/     # Research project docs
├── architecture/               # Cross-project technical architecture
├── development/               # Standards, practices, and conventions
└── philosophy/                # Principles and approaches
```

---

## 🔮 Future Evolution

### Scaling Context Management
As the project portfolio grows:
- **Context Categorization**: More granular organization of shared vs specific context
- **Agent Specialization**: Different types of agents with different context needs
- **Automated Context**: Tools to automatically maintain context consistency
- **Community Context**: External contributions to shared knowledge base

### Advanced Agent Coordination
Future possibilities:
- **Context APIs**: Programmatic access to context for agent coordination
- **Dynamic Context**: Context that adapts based on current project states
- **Cross-Agent Learning**: Agents learning from each other's experiences
- **Intelligent Context Routing**: Automatically providing relevant context to agents

---

*Agent context architecture established: August 11, 2025*
*Context management approach: Multi-project AI agent coordination*
*Documentation site deployment: Planned for GitHub Pages*
