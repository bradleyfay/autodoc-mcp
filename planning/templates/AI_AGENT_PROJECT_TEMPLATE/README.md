# AI Agent Optimized Project Template

**Template Version**: 1.0
**Created**: August 12, 2025
**Purpose**: Standardized project structure optimized for AI agent workflows and handoffs

## Template Overview

This template implements the AI-agent-optimized project structure as specified in the planning-specialist agent specifications. It is designed to eliminate human-collaboration artifacts and optimize for seamless AI agent handoffs and state preservation.

## Template Structure

```
AI_AGENT_PROJECT_TEMPLATE/
├── PROJECT_STATE.md          # Current status, next actions, blocking issues
├── SCOPE_DEFINITION.md       # Project boundaries, what's included/excluded
├── IMPLEMENTATION_LOG.md     # Chronological record of implementations
├── AGENT_CONTEXT.md         # Essential context for any agent working on this
├── assets/                  # Project-specific files, mockups, configs
└── README.md               # This file - template usage instructions
```

## File Purposes

### PROJECT_STATE.md
- **Purpose**: Real-time project status that any agent can understand immediately
- **Key Features**:
  - Current phase and completion status
  - Immediate actionable next steps
  - Blocking issues and dependencies
  - Agent handoff information
- **Update Frequency**: After every significant work session
- **Critical Success Factor**: Must always reflect current reality

### SCOPE_DEFINITION.md
- **Purpose**: Clear project boundaries and objectives
- **Key Features**:
  - Explicit inclusion/exclusion criteria
  - Success metrics and completion definitions
  - Dependencies and constraints
  - Change control processes
- **Update Frequency**: When scope changes are approved
- **Critical Success Factor**: Prevents scope creep and misalignment

### IMPLEMENTATION_LOG.md
- **Purpose**: Chronological record of decisions and learning
- **Key Features**:
  - Major implementation milestones
  - Technical decisions with rationale
  - Failed approaches and lessons learned
  - Agent handoff notes
- **Update Frequency**: After major implementations or decisions
- **Critical Success Factor**: Preserves context and learning across sessions

### AGENT_CONTEXT.md
- **Purpose**: Essential background knowledge for any agent
- **Key Features**:
  - Domain knowledge and terminology
  - Technical architecture decisions
  - Development standards and practices
  - Business context and user needs
- **Update Frequency**: When foundational aspects change
- **Critical Success Factor**: Enables rapid agent onboarding and context switching

## Usage Instructions

### Creating a New Project

1. **Copy Template Directory**:
   ```bash
   cp -r planning/templates/AI_AGENT_PROJECT_TEMPLATE planning/projects/[project-name]
   ```

2. **Customize Core Files**:
   - Replace all `[PROJECT NAME]` placeholders with actual project name
   - Fill in initial project information in each template
   - Remove template-specific content (like this README)

3. **Initialize Project State**:
   - Set initial phase in PROJECT_STATE.md
   - Define scope in SCOPE_DEFINITION.md
   - Create initial entry in IMPLEMENTATION_LOG.md
   - Fill essential context in AGENT_CONTEXT.md

### Maintaining Project State

#### Daily/Session Updates
- **PROJECT_STATE.md**: Update current status, next actions, and handoff info
- **IMPLEMENTATION_LOG.md**: Record major implementations and decisions

#### Weekly Updates
- **PROJECT_STATE.md**: Review and update risk assessment, metrics
- **AGENT_CONTEXT.md**: Update if any foundational aspects changed

#### Milestone Updates
- **SCOPE_DEFINITION.md**: Review scope boundaries and success criteria
- **IMPLEMENTATION_LOG.md**: Record phase completion and major learnings

### Agent Handoff Protocol

#### Before Ending Session
1. Update PROJECT_STATE.md with current status
2. Record session work in IMPLEMENTATION_LOG.md
3. Note any context changes in AGENT_CONTEXT.md
4. Ensure next actions are clearly defined

#### Starting New Session
1. Read PROJECT_STATE.md first for current status
2. Review AGENT_CONTEXT.md for essential background
3. Check IMPLEMENTATION_LOG.md for recent decisions
4. Validate SCOPE_DEFINITION.md for boundaries

## Template Features for AI Agents

### Optimized for Agent Comprehension
- **Structured Format**: Consistent headings and organization across all files
- **Clear Hierarchies**: Information organized by importance and frequency of access
- **Explicit Context**: No assumptions about prior knowledge
- **Actionable Information**: Focus on what needs to be done next

### Minimized Context Switching
- **Self-Contained Files**: Each file provides complete context for its domain
- **Cross-References**: Clear links between related information
- **Status at Glance**: Quick status indicators throughout
- **No Implicit Knowledge**: All important information is explicitly documented

### Handoff Optimization
- **Current State Clarity**: Always clear where project stands
- **Next Action Focus**: Immediate actionable steps for any agent
- **Context Preservation**: Essential information survives session boundaries
- **Decision History**: Rationale for major decisions preserved

## Quality Standards

### Information Currency
- PROJECT_STATE.md must reflect current reality at all times
- No outdated "current" information
- Clear timestamps on all updates
- Consistent update patterns

### Clarity and Completeness
- Any agent should understand project status within 5 minutes
- No ambiguous next actions
- Complete context for decision-making
- Clear success criteria and boundaries

### Agent Workflow Support
- Facilitates rapid project pickup
- Minimizes clarification requests
- Enables consistent decision-making
- Supports parallel agent work

## Template Evolution

### Version Control
- Template versions are tracked and documented
- Changes are propagated to existing projects when beneficial
- Backwards compatibility considerations for existing projects

### Improvement Process
- Template improvements based on agent workflow analysis
- Regular review of template effectiveness
- Community feedback integration for template optimization

---

## Getting Started Checklist

When using this template:

- [ ] Copy template to new project directory
- [ ] Replace all placeholder text with project-specific information
- [ ] Initialize PROJECT_STATE.md with current project phase
- [ ] Complete SCOPE_DEFINITION.md with project boundaries
- [ ] Create first entry in IMPLEMENTATION_LOG.md
- [ ] Fill essential context in AGENT_CONTEXT.md
- [ ] Remove this README.md file (or replace with project-specific README)
- [ ] Test agent handoff by having another agent review the project structure

---

*AI Agent Optimized Project Template*
*Designed for seamless agent handoffs and state preservation*
*Template Version 1.0 - August 12, 2025*
