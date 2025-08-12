# Agent Execution Protocols

**Purpose**: Executable protocols for AI agents working on this project
**Template Version**: 1.0
**Created**: August 12, 2025

---

## 🤖 Agent Onboarding Protocol (5-Minute Context Acquisition)

### Phase 1: Essential Context (60 seconds)
```yaml
required_reading_order:
  1: "PROJECT_STATE.md - Agent Context Window section"
  2: "SCOPE_DEFINITION.md - Agent Decision-Making Framework"
  3: "AGENT_CONTEXT.md - Essential Background section"

context_validation_checklist:
  - [ ] I understand the project mission and current phase
  - [ ] I know my decision-making authority level for this project
  - [ ] I can identify the next immediate action to take
  - [ ] I understand any cross-project coordination requirements
```

### Phase 2: Work Environment Setup (120 seconds)
```bash
# Agent environment validation script
cd [PROJECT_ROOT]
git status  # Verify correct branch and clean state
[PROJECT_SPECIFIC_SETUP_COMMANDS]

# Validate environment
[PROJECT_SPECIFIC_VALIDATION_COMMANDS]
echo "Environment ready: $(date)"
```

### Phase 3: Integration Verification (120 seconds)
```yaml
integration_checks:
  - cross_project_coordination: "Review active dependencies in PROJECT_STATE.md"
  - resource_conflicts: "Check for concurrent agents in same work area"
  - handoff_quality: "Validate previous agent completed handoff properly"
  - next_actions_clarity: "Confirm next actions are specific and achievable"
```

---

## 🎯 Decision-Making Framework

### Agent Authority Matrix
```yaml
autonomous_decisions:
  implementation_approaches:
    authority: "Full"
    constraint: "Must align with project architecture and standards"
    documentation: "Record key decisions in IMPLEMENTATION_LOG.md"

  testing_strategies:
    authority: "Full"
    constraint: "Must meet project quality requirements"
    documentation: "Update test status in PROJECT_STATE.md"

  refactoring_and_optimization:
    authority: "Full"
    constraint: "Cannot change external interfaces"
    documentation: "Record rationale and impact"

consultation_required:
  scope_modifications:
    consult_with: "planning-specialist or project stakeholder"
    trigger: "Work doesn't clearly fit within defined scope boundaries"
    process: "Document proposed change and seek approval before proceeding"

  cross_project_changes:
    consult_with: "agents working on dependent projects"
    trigger: "Changes affect other projects or shared resources"
    process: "Coordinate through cross-project communication channels"

  architecture_changes:
    consult_with: "architecture specialist or technical lead"
    trigger: "Changes affect system design or technology choices"
    process: "Design review and approval before implementation"

escalation_required:
  resource_conflicts:
    escalate_to: "planning-specialist"
    trigger: "Cannot resolve resource conflicts with other projects"

  scope_boundary_disputes:
    escalate_to: "project stakeholder"
    trigger: "Unclear if work falls within or outside project scope"

  technical_roadblocks:
    escalate_to: "domain specialist or technical lead"
    trigger: "Technical problems beyond current agent expertise"
```

### Decision Process Template
```yaml
decision_framework:
  1_identify_decision: "What needs to be decided?"
  2_check_authority: "Is this within my decision-making authority?"
  3_gather_context: "What information do I need to decide well?"
  4_evaluate_options: "What are the alternatives and their trade-offs?"
  5_assess_impact: "How will this affect the project and other projects?"
  6_make_decision: "Choose best option within my authority"
  7_document_decision: "Record decision and rationale"
  8_communicate_impact: "Inform other agents/projects if needed"
```

---

## 🔄 Agent Handoff Protocol

### Pre-Handoff Checklist (Agent Completing Work)
```yaml
handoff_preparation:
  state_synchronization:
    - [ ] Update PROJECT_STATE.md with current completion percentage
    - [ ] Document all work completed in current session
    - [ ] Record any blocking issues or dependencies discovered
    - [ ] Validate that documented state matches actual project state

  context_preparation:
    - [ ] Update AGENT_CONTEXT.md if new knowledge gained
    - [ ] Record key decisions made and their rationale
    - [ ] Document any technical debt or code quality issues discovered
    - [ ] Note any cross-project coordination needs for next agent

  environment_cleanup:
    - [ ] Commit and push all code changes
    - [ ] Ensure development environment is in clean state
    - [ ] Stop any running services or processes that aren't persistent
    - [ ] Update documentation for any environment changes

  next_actions_preparation:
    - [ ] Define 1-3 specific, actionable next steps
    - [ ] Provide context and rationale for each next action
    - [ ] Identify any prerequisites or dependencies for next actions
    - [ ] Estimate effort required for each next action
```

### Post-Handoff Validation (Agent Starting Work)
```yaml
handoff_validation:
  context_acquisition:
    - [ ] Read and understand current project state (<5 minutes)
    - [ ] Verify understanding of immediate next actions
    - [ ] Confirm development environment is ready
    - [ ] Review any cross-project coordination requirements

  continuity_verification:
    - [ ] Validate that project state matches documented state
    - [ ] Test that development environment works as expected
    - [ ] Confirm understanding of work context and objectives
    - [ ] Identify any gaps or questions before starting work

  quality_assessment:
    rate_handoff_quality: "[1-5 scale]"
    time_to_productive_work: "[minutes]"
    clarification_needs: "[list any unclear areas]"
    improvement_suggestions: "[recommendations for future handoffs]"
```

---

## 🤝 Cross-Project Coordination Protocol

### Communication Triggers
```yaml
required_coordination:
  scope_boundary_changes:
    trigger: "Work approaches or crosses project scope boundaries"
    action: "Consult with planning-specialist before proceeding"
    documentation: "Record coordination discussion and outcomes"

  shared_resource_conflicts:
    trigger: "Need for resources currently used by other projects"
    action: "Coordinate directly with agents on affected projects"
    documentation: "Update PROJECT_STATE.md with coordination status"

  cross_project_dependencies:
    trigger: "Changes that affect what this project provides to others"
    action: "Notify dependent projects before making changes"
    documentation: "Record impact assessment and communication"

  integration_point_modifications:
    trigger: "Changes to APIs, interfaces, or integration contracts"
    action: "Review changes with agents working on connected projects"
    documentation: "Update integration specifications"
```

### Coordination Communication Template
```markdown
## Cross-Project Coordination Notice

**From Project**: [Current Project Name]
**To Project**: [Affected Project Name]
**Agent**: [Agent ID/Type]
**Date**: [ISO Date]

### Change Summary
[Brief description of what's changing and why]

### Impact Assessment
[How this affects the other project]

### Timeline
**Change Implementation**: [When]
**Other Project Action Needed**: [When and what]

### Coordination Required
[Specific coordination or communication needed]

### Contact Information
[How to coordinate - project channels, documentation locations]
```

---

## 📊 Performance and Quality Protocols

### Work Session Quality Metrics
```yaml
session_effectiveness:
  context_acquisition_time:
    target: "< 5 minutes"
    measurement: "Time from starting to productive work"

  handoff_preparation_time:
    target: "< 10 minutes"
    measurement: "Time to prepare state for next agent"

  work_continuity:
    target: "No context gaps"
    measurement: "Next agent clarification requests"

  cross_project_coordination:
    target: "No coordination conflicts"
    measurement: "Successful coordination with dependent projects"
```

### Quality Assurance Checkpoints
```yaml
work_quality_gates:
  code_quality:
    frequency: "Every commit"
    criteria: "Passes linting, typing, and style checks"
    action: "Fix issues before proceeding"

  test_coverage:
    frequency: "Before major state updates"
    criteria: "Maintains or improves test coverage"
    action: "Add tests for new functionality"

  documentation_currency:
    frequency: "End of each work session"
    criteria: "Documentation matches implementation reality"
    action: "Update docs to reflect current state"

  integration_validation:
    frequency: "Before cross-project coordination"
    criteria: "Changes don't break integration contracts"
    action: "Test integration points before communicating changes"
```

---

## 🚨 Error Handling and Recovery Protocol

### Common Issue Resolution
```yaml
issue_categories:
  context_insufficient:
    symptoms: "Unclear about project goals or current state"
    resolution: "Review AGENT_CONTEXT.md and consult planning-specialist"
    prevention: "Request context improvement for future agents"

  environment_issues:
    symptoms: "Development environment not working as expected"
    resolution: "Follow environment setup procedures, escalate if needed"
    prevention: "Update environment documentation"

  cross_project_conflicts:
    symptoms: "Work conflicts with other projects or agents"
    resolution: "Pause work, coordinate with affected projects"
    prevention: "Better cross-project communication"

  scope_uncertainty:
    symptoms: "Unclear if work falls within project scope"
    resolution: "Consult SCOPE_DEFINITION.md and escalate if needed"
    prevention: "Improve scope documentation clarity"
```

### Escalation Protocol
```yaml
escalation_framework:
  technical_issues:
    level_1: "Consult project technical documentation"
    level_2: "Coordinate with other agents working on project"
    level_3: "Escalate to domain specialist or technical lead"

  coordination_issues:
    level_1: "Direct coordination with affected agents/projects"
    level_2: "Consult planning-specialist for portfolio coordination"
    level_3: "Escalate to project stakeholder for decision"

  scope_issues:
    level_1: "Review SCOPE_DEFINITION.md for clarification"
    level_2: "Consult with planning-specialist"
    level_3: "Escalate to project stakeholder for scope decision"
```

---

## 🔧 Template Customization Guide

### Project-Specific Protocol Extensions
```yaml
customization_areas:
  technology_specific_protocols:
    location: "Add to AGENT_CONTEXT.md"
    content: "Technology-specific setup, validation, and workflow steps"

  domain_specific_procedures:
    location: "Add to this file under custom section"
    content: "Domain expertise requirements and specialized procedures"

  integration_specific_protocols:
    location: "Add to SCOPE_DEFINITION.md dependencies section"
    content: "Specific coordination procedures for project integrations"

  quality_specific_requirements:
    location: "Add to this file under quality protocols"
    content: "Project-specific quality gates and validation procedures"
```

### Protocol Evolution Process
```yaml
protocol_improvement:
  feedback_collection:
    method: "Agent experience reports in IMPLEMENTATION_LOG.md"
    frequency: "After each significant work session"

  pattern_identification:
    method: "Review session reports for common issues and successes"
    frequency: "Monthly protocol review"

  protocol_updates:
    method: "Update protocols based on agent experience patterns"
    approval: "planning-specialist review and validation"

  effectiveness_measurement:
    metrics: "Context acquisition time, handoff quality, coordination success"
    reporting: "Include in project state updates"
```

---

*Agent Execution Protocols Template v1.0*
*Optimized for <5 minute context acquisition and seamless agent handoffs*
*Created: August 12, 2025*
