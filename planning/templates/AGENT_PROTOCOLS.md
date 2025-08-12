# AI Agent Protocols for Planning-Specialist

**Version**: 1.0
**Created**: August 12, 2025
**Purpose**: Standardized procedures for AI agent project management and handoffs

---

## Project Creation Protocol

### Phase 1: Scope Assessment (5-10 minutes)

#### Step 1: Project Evaluation
**Questions to Answer**:
- What specific problem does this project solve?
- Who are the primary users/beneficiaries?
- What are the core deliverables?
- How does this relate to existing projects?

**Output**: Clear 2-3 sentence project mission statement

#### Step 2: Boundary Definition
**Scope Boundaries Analysis**:
- **Included**: What specific features/capabilities are in scope
- **Excluded**: What similar/related work is explicitly out of scope
- **Deferred**: What might be future scope but not current priority

**Dependencies Assessment**:
- Cross-project dependencies (what we need from other projects)
- External dependencies (services, APIs, third-party tools)
- Resource dependencies (specific skills, tools, or access required)

**Output**: Clear scope boundaries and dependency map

#### Step 3: Success Criteria Definition
**Success Metrics**:
- Measurable outcomes that define project success
- Quality gates that must be met
- User acceptance criteria

**Completion Definition**:
- Specific conditions for considering project "done"
- Handoff requirements for ongoing maintenance
- Documentation and knowledge transfer requirements

**Output**: Unambiguous completion criteria

### Phase 2: Structure Setup (5 minutes)

#### Step 1: Create Project Directory
```bash
# Create project using AI agent optimized template
cp -r planning/templates/AI_AGENT_PROJECT_TEMPLATE planning/projects/[project-name]
cd planning/projects/[project-name]
```

#### Step 2: Initialize Core Files
**PROJECT_STATE.md**:
- Set initial phase (typically "Planning")
- Define immediate next 3 actions
- Set initial success metrics
- Clear statement of current status

**SCOPE_DEFINITION.md**:
- Transfer scope analysis from Phase 1
- Document all boundary decisions
- List dependencies and constraints
- Define change control process

**AGENT_CONTEXT.md**:
- Essential domain knowledge
- Key terminology and concepts
- Technical constraints or requirements
- User/stakeholder context

**IMPLEMENTATION_LOG.md**:
- Initial entry documenting project creation
- Rationale for key initial decisions
- Project creation context and objectives

#### Step 3: Integration Setup
**Cross-Project Integration**:
- Add project to main PLANNING_INDEX.md
- Update PROJECT_COORDINATION.md if needed
- Identify shared standards that apply
- Note potential resource conflicts

### Phase 3: Context Capture (10-15 minutes)

#### Step 1: Domain Knowledge Capture
**Essential Background Information**:
- Problem domain expertise required
- Industry standards or regulations
- User personas and use cases
- Business rules and constraints

#### Step 2: Technical Context
**Technology Stack Decisions**:
- Programming languages and frameworks
- Infrastructure and deployment requirements
- Integration points and APIs
- Development tools and standards

#### Step 3: Quality and Performance Requirements
**Non-Functional Requirements**:
- Performance benchmarks
- Security requirements
- Reliability and availability needs
- Maintainability standards

### Phase 4: Handoff Preparation (5 minutes)

#### Step 1: First Actions Definition
**Immediate Next Steps**:
- 3-5 specific actionable tasks
- Clear acceptance criteria for each
- Estimated effort and prerequisites
- Priority order for task execution

#### Step 2: Context Validation
**Handoff Readiness Check**:
- Can any agent understand the project goals within 5 minutes?
- Are next actions specific and actionable?
- Is essential context captured in AGENT_CONTEXT.md?
- Are boundaries clear in SCOPE_DEFINITION.md?

#### Step 3: Agent Assignment Ready
**Project State Verification**:
- All template files completed with real project information
- No placeholder text remaining
- Links and cross-references working
- Project added to portfolio tracking

**Total Time Investment**: 25-40 minutes for complete project setup

---

## Project Maintenance Protocol

### Daily Maintenance (2-5 minutes per session)

#### Session Start Checklist
- [ ] Read PROJECT_STATE.md for current status
- [ ] Verify next actions are still relevant and current
- [ ] Check for any new blocking issues
- [ ] Review any changes since last session

#### During Session Updates
**Continuous State Management**:
- Update completion status as work progresses
- Note any new blocking issues immediately
- Document significant decisions as they're made
- Track changes to scope or approach

#### Session End Checklist
- [ ] Update PROJECT_STATE.md with current status
- [ ] Record session work in IMPLEMENTATION_LOG.md
- [ ] Update next actions for future sessions
- [ ] Note any handoff information for next agent

### Weekly Maintenance (10-15 minutes)

#### Status Review
**Progress Assessment**:
- Compare actual progress against planned milestones
- Update completion percentages
- Assess risk levels and mitigation effectiveness
- Review success metrics and trends

#### Context Updates
**Information Currency Check**:
- AGENT_CONTEXT.md still accurate and complete?
- Any new domain knowledge or requirements?
- Technology or architecture changes?
- Updated business rules or constraints?

#### Cross-Project Coordination
**Portfolio Integration**:
- Resource conflicts with other projects?
- Dependencies changes from other projects?
- Opportunities for shared work or learning?
- Updates needed to portfolio documentation?

### Monthly Maintenance (20-30 minutes)

#### Comprehensive Review
**Project Health Assessment**:
- Overall project trajectory and health
- Resource allocation effectiveness
- Quality of agent handoffs and continuity
- Template effectiveness and areas for improvement

#### Process Optimization
**Workflow Analysis**:
- Agent productivity and efficiency patterns
- Common friction points or repeated issues
- Documentation quality and usefulness
- Handoff success rates and quality

#### Strategic Alignment
**Portfolio Coordination**:
- Project priority and resource allocation review
- Cross-project synergies and optimizations
- Long-term strategic alignment
- Portfolio balance and risk management

---

## Agent Handoff Protocol

### Pre-Handoff Preparation (Current Agent - 3-5 minutes)

#### Step 1: State Synchronization
**PROJECT_STATE.md Updates**:
- Current phase and completion status
- All blocking issues and dependencies
- Next 3 immediate actions with clear criteria
- Any recent changes to scope or approach

**Session Context**:
- What was accomplished in current session
- Any discoveries or insights gained
- Problems encountered and solutions attempted
- Specific context for next agent to continue

#### Step 2: Implementation Log Update
**Decision Documentation**:
- Major technical or strategic decisions made
- Rationale for approaches chosen
- Alternative approaches considered and why rejected
- Any failed attempts and lessons learned

#### Step 3: Context Validation
**Information Currency Check**:
- AGENT_CONTEXT.md reflects current understanding
- SCOPE_DEFINITION.md boundaries still accurate
- Any new domain knowledge discovered
- Changes to technical constraints or requirements

### Handoff Execution (5 minutes)

#### Step 1: Complete Current Work
**Clean Handoff State**:
- Finish current atomic task or reach clean stopping point
- Commit any code changes with clear commit messages
- Update documentation for work completed
- Clean up temporary files or states

#### Step 2: Status Documentation
**Final State Update**:
- PROJECT_STATE.md reflects reality at handoff moment
- Clear indication of where work stopped
- Explicit next actions for incoming agent
- Any urgent issues or time-sensitive items

#### Step 3: Handoff Note Creation
**Transition Information**:
- Brief summary of session accomplishments
- Context for continuing work
- Any environmental or setup requirements
- Specific knowledge needed for next tasks

### Post-Handoff Verification (Incoming Agent - 2-3 minutes)

#### Step 1: Context Acquisition
**Information Gathering**:
- Read PROJECT_STATE.md for current status
- Review AGENT_CONTEXT.md for essential background
- Check recent IMPLEMENTATION_LOG.md entries
- Understand immediate next actions

#### Step 2: State Validation
**Reality Check**:
- Verify project state matches documentation
- Confirm development environment status
- Validate next actions are achievable
- Identify any missing context or unclear areas

#### Step 3: Handoff Quality Assessment
**Handoff Success Metrics**:
- Time to understand current state: [Target: <5 minutes]
- Clarity of next actions: [Target: No ambiguity]
- Context completeness: [Target: No clarification requests needed]
- Environmental readiness: [Target: Can begin work immediately]

---

## Cross-Project Coordination Protocol

### Project Creation Coordination

#### Step 1: Portfolio Integration Analysis
**Existing Project Review**:
- Similar or overlapping projects in portfolio
- Potential resource conflicts or synergies
- Shared standards and practices to apply
- Cross-project dependencies to establish

#### Step 2: Resource Allocation Assessment
**Capacity Analysis**:
- Current portfolio resource utilization
- Available capacity for new project
- Skill requirements vs available expertise
- Timeline coordination with existing projects

#### Step 3: Integration Planning
**Coordination Setup**:
- Update portfolio documentation
- Establish cross-project communication needs
- Identify shared resources or standards
- Plan for coordinated deliveries if needed

### Ongoing Coordination Maintenance

#### Daily Coordination Checks
**Quick Portfolio Scan**:
- Any blocking dependencies from other projects?
- Resource conflicts requiring resolution?
- Opportunities for knowledge sharing?
- Urgent cross-project issues?

#### Weekly Coordination Review
**Portfolio Health Assessment**:
- Overall portfolio balance and risk
- Resource allocation effectiveness
- Cross-project dependency status
- Coordination overhead and optimization opportunities

#### Monthly Strategic Coordination
**Portfolio Strategy Review**:
- Long-term strategic alignment across projects
- Portfolio priorities and resource reallocation
- Cross-project synergies and optimization
- Strategic initiatives requiring coordination

---

## Error Recovery and Problem Resolution

### Common Handoff Issues

#### Issue: Unclear Next Actions
**Symptoms**: Next agent spends >10 minutes figuring out what to do
**Resolution Protocol**:
1. Review PROJECT_STATE.md and identify vague actions
2. Break down unclear actions into specific, measurable tasks
3. Add acceptance criteria and prerequisites for each action
4. Update with clear time estimates and priorities

#### Issue: Missing Context
**Symptoms**: Agent needs to research domain or technical context
**Resolution Protocol**:
1. Identify what context was missing
2. Update AGENT_CONTEXT.md with essential missing information
3. Add domain knowledge, technical decisions, or business context
4. Verify context sufficiency with quick test read-through

#### Issue: Outdated Project State
**Symptoms**: Documentation doesn't match actual project reality
**Resolution Protocol**:
1. Audit all core files for accuracy
2. Update PROJECT_STATE.md to reflect current reality
3. Add recent decisions to IMPLEMENTATION_LOG.md
4. Verify all cross-references and dependencies

#### Issue: Scope Confusion
**Symptoms**: Uncertainty about what's in/out of scope
**Resolution Protocol**:
1. Review and clarify SCOPE_DEFINITION.md
2. Add explicit exclusions for areas of confusion
3. Update success criteria and completion definition
4. Document any scope changes in IMPLEMENTATION_LOG.md

### Escalation Procedures

#### When to Escalate
- Repeated handoff failures (>3 attempts)
- Fundamental scope or technical architecture questions
- Cross-project conflicts that can't be resolved locally
- Resource allocation issues affecting multiple projects

#### Escalation Process
1. Document the issue clearly in IMPLEMENTATION_LOG.md
2. Identify stakeholders who need to be involved
3. Prepare recommendations and alternatives
4. Update PROJECT_STATE.md to reflect escalated status
5. Use appropriate cross-project coordination channels

---

## Quality Assurance for Agent Workflows

### Handoff Quality Metrics

#### Quantitative Metrics
- **Context Acquisition Time**: Time for new agent to understand project (<5 min target)
- **Clarification Requests**: Number of questions needed to begin work (0 target)
- **State Accuracy**: Percentage of documentation that matches reality (100% target)
- **Action Clarity**: Percentage of next actions that are immediately actionable (100% target)

#### Qualitative Metrics
- **Agent Confidence**: New agent feels confident to begin work
- **Continuity Quality**: Work continues smoothly from previous session
- **Decision Consistency**: Decisions align with previous context and rationale
- **Progress Efficiency**: Time spent on productive work vs context gathering

### Continuous Improvement

#### Weekly Process Review
- Handoff success rates and common issues
- Template effectiveness and areas for improvement
- Agent workflow friction points
- Cross-project coordination effectiveness

#### Monthly Template Evolution
- Update templates based on usage patterns
- Incorporate lessons learned from multiple projects
- Optimize for most common agent workflows
- Balance comprehensiveness with usability

#### Quarterly Strategic Assessment
- Overall planning-specialist effectiveness
- Portfolio management success metrics
- AI agent workflow optimization opportunities
- Integration with broader development practices

---

*AI Agent Protocols for Planning-Specialist*
*Version 1.0 - August 12, 2025*
*Optimized for seamless agent handoffs and state preservation*
