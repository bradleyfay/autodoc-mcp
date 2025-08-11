# Planning Folder Restructure Proposal

**Date**: August 11, 2025
**Issue**: Current planning structure inadequate for managing multiple ongoing projects
**Priority**: High - Impacts project organization and scalability

## Current State Analysis

### Problems Identified

#### 1. **Mixed Project Scope**
The current structure mixes different projects without clear boundaries:
- Main focus is AutoDocs MCP Server
- TASK_GRAPH_SYSTEM is a completely separate project buried in the structure
- Documentation Site project would add a third project
- No clear separation of concerns

#### 2. **Lack of Project Hierarchy**
Everything exists at the same organizational level:
```
planning/
├── ARCHIVED/           # Mixed project archives
├── CORE_REFERENCE/     # AutoDocs-specific
├── DEVELOPMENT_PHASES/ # AutoDocs-specific
├── EXPANSION/          # AutoDocs-specific
├── IMPLEMENTATION/     # Mixed current work
└── TASK_GRAPH_SYSTEM/  # Completely different project!
```

#### 3. **Scalability Issues**
- Adding new projects creates confusion
- No standard structure for project management
- Hard to find project-specific information
- Cross-project coordination not supported

#### 4. **Inconsistent Organization**
- Some folders are project-specific (DEVELOPMENT_PHASES)
- Some are generic (IMPLEMENTATION)
- No standard project lifecycle management
- Mixed active/archived content

## Proposed New Structure

### Vision: Multi-Project Planning System
Organize around **projects as first-class citizens** with consistent internal structure and cross-project coordination support.

```
planning/
├── projects/                    # All active and planned projects
│   ├── autodocs-mcp/           # Main AutoDocs MCP Server project
│   │   ├── PROJECT_INDEX.md    # Project overview and quick access
│   │   ├── active/             # Current work and priorities
│   │   │   ├── current_priorities.md
│   │   │   ├── technical_debt.md
│   │   │   └── sprint_tracking.md
│   │   ├── phases/             # Completed and planned development phases
│   │   │   ├── phase_3_network_resilience/
│   │   │   ├── phase_4_dependency_context/
│   │   │   └── pre_release_v0.3/
│   │   ├── reference/          # Core specifications and architecture
│   │   │   ├── product_spec.md
│   │   │   ├── system_architecture.md
│   │   │   └── release_validation_status.md
│   │   ├── expansion/          # Future roadmap and expansion plans
│   │   │   ├── roadmap.md
│   │   │   ├── multi_language_support.md
│   │   │   └── documentation_sources_expansion.md
│   │   └── archived/          # Historical documents
│   │
│   ├── documentation-site/     # Documentation revision project
│   │   ├── PROJECT_INDEX.md    # Project overview
│   │   ├── PROJECT_PLAN.md     # Detailed implementation plan
│   │   ├── PROGRESS_TRACKER.md # Real-time tracking
│   │   ├── deliverables/       # Project outputs
│   │   ├── meeting-notes/      # Decisions and discussions
│   │   └── reference/         # Supporting documents
│   │
│   ├── task-graph-system/      # AI agent orchestration project
│   │   ├── PROJECT_INDEX.md    # Project overview and status
│   │   ├── active/             # Current development work
│   │   ├── architecture/       # System design documents
│   │   ├── implementation/     # Implementation plans
│   │   ├── protocols/          # Agent communication specs
│   │   └── documentation/      # User guides and specs
│   │
│   └── [future-projects]/      # Standardized structure for new projects
│
├── cross-project/              # Multi-project coordination
│   ├── PORTFOLIO_OVERVIEW.md   # All projects status and priorities
│   ├── resource_allocation.md  # Team and resource management
│   ├── timeline_coordination.md# Cross-project scheduling
│   ├── shared_standards.md     # Common development practices
│   └── technology_decisions.md # Shared technology choices
│
├── templates/                  # Project management templates
│   ├── PROJECT_TEMPLATE/       # Standard project structure
│   │   ├── PROJECT_INDEX.md
│   │   ├── PROJECT_PLAN.md
│   │   ├── PROGRESS_TRACKER.md
│   │   ├── active/
│   │   ├── reference/
│   │   └── archived/
│   ├── tracking_templates.md   # Progress tracking formats
│   └── meeting_templates.md    # Meeting notes and decision formats
│
├── archived/                   # Completed projects and superseded documents
│   ├── completed_projects/     # Successfully completed projects
│   └── superseded_planning/    # Old planning documents
│
└── PLANNING_INDEX.md           # Master index for entire planning system
```

## Implementation Plan

### Phase 1: Setup New Structure (1-2 days)
1. **Create new directory structure** (without moving existing content)
2. **Create templates and standards** for project management
3. **Create master PLANNING_INDEX.md** with navigation

### Phase 2: Migrate AutoDocs MCP Project (2-3 days)
1. **Create autodocs-mcp project structure**
2. **Migrate existing content** to appropriate locations:
   - CORE_REFERENCE → reference/
   - DEVELOPMENT_PHASES → phases/
   - IMPLEMENTATION → active/
   - EXPANSION → expansion/
   - ARCHIVED → archived/
3. **Create PROJECT_INDEX.md** for AutoDocs MCP
4. **Update all internal references**

### Phase 3: Migrate Task Graph System (1 day)
1. **Create task-graph-system project structure**
2. **Move TASK_GRAPH_SYSTEM content** to new location
3. **Create PROJECT_INDEX.md** for Task Graph System
4. **Update any cross-references**

### Phase 4: Setup Cross-Project Coordination (1 day)
1. **Create cross-project documentation**
2. **Setup resource allocation tracking**
3. **Create portfolio overview dashboard**
4. **Document new planning processes**

## Benefits of New Structure

### For Individual Projects
✅ **Clear project boundaries** - Each project has dedicated space
✅ **Consistent structure** - Same organization pattern for all projects
✅ **Complete project context** - All project info in one location
✅ **Independent evolution** - Projects can evolve without affecting others

### For Multi-Project Management
✅ **Portfolio visibility** - Easy overview of all active projects
✅ **Resource coordination** - Clear view of competing priorities
✅ **Standardized processes** - Consistent project management across all projects
✅ **Scalable growth** - Easy to add new projects with established patterns

### For Team Productivity
✅ **Faster navigation** - Clear paths to project-specific information
✅ **Reduced confusion** - No mixing of different project contexts
✅ **Better onboarding** - New team members can quickly understand project structure
✅ **Improved maintenance** - Easier to keep documentation current

## Migration Strategy

### Backwards Compatibility
- **Maintain existing URLs** during transition period
- **Create redirect documentation** for moved content
- **Gradual migration** to avoid disruption
- **Clear communication** about structure changes

### Risk Mitigation
- **Backup current structure** before starting migration
- **Test migrations** in development environment first
- **Incremental changes** to minimize disruption
- **Rollback plan** if issues arise

## Success Criteria

### Short-term (Post-migration)
- [ ] All existing content accessible in new structure
- [ ] No broken internal references
- [ ] Clear project boundaries established
- [ ] Team can navigate new structure effectively

### Medium-term (1 month)
- [ ] New project onboarding faster and more consistent
- [ ] Better cross-project coordination and visibility
- [ ] Reduced time finding project-specific information
- [ ] Standardized project management processes adopted

### Long-term (3 months)
- [ ] Planning system scales easily with new projects
- [ ] Portfolio management provides clear strategic visibility
- [ ] Project templates reduce setup time for new initiatives
- [ ] Team productivity improved through better organization

---

## Recommendation

**Proceed with restructure** - The current mixed structure is hindering effective multi-project management. The proposed structure provides:

1. **Clear project separation** with consistent internal organization
2. **Scalable framework** for adding future projects
3. **Portfolio management capabilities** for strategic coordination
4. **Standardized processes** that improve team productivity

**Timeline**: 1 week for complete migration
**Risk**: Low - Primarily organizational with content preservation
**Impact**: High - Significantly improves project management capability

**Next Steps**:
1. Review and approve this proposal
2. Begin Phase 1 implementation (create new structure)
3. Execute migration plan with proper backups
4. Update team processes and documentation

*Proposal created: August 11, 2025*
