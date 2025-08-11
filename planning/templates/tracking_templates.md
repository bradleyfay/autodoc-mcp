# Project Tracking Templates

This document provides standardized templates for consistent project tracking across all projects.

## Sprint Planning Template

### Sprint Goal Template
```markdown
## Sprint [Number] - [Date Range]

### Sprint Goal
[One clear, measurable objective for this sprint]

### Sprint Capacity
- **Team Size**: [Number] developers
- **Available Days**: [Total person-days accounting for PTO, holidays]
- **Commitment**: [Story points or tasks]

### Sprint Backlog
- [ ] **[Task 1]** - [Story points] - [Assigned to]
  - Acceptance Criteria: [Clear definition of done]
  - Dependencies: [Any blockers or prerequisites]
- [ ] **[Task 2]** - [Story points] - [Assigned to]
  - Acceptance Criteria: [Clear definition of done]
  - Dependencies: [Any blockers or prerequisites]
```

## Daily Standup Template

### Standup Format
```markdown
## Daily Standup - [Date]

### [Team Member 1]
- **Yesterday**: [What was accomplished]
- **Today**: [What will be worked on]
- **Blockers**: [Any impediments]

### [Team Member 2]
- **Yesterday**: [What was accomplished]
- **Today**: [What will be worked on]
- **Blockers**: [Any impediments]

### Action Items
- [ ] [Action] - [Owner] - [Due date]

### Decisions Made
- [Decision] - [Impact/rationale]
```

## Weekly Status Template

### Weekly Report Format
```markdown
## Weekly Status - Week of [Date]

### Executive Summary
[High-level status in 2-3 sentences]

### Key Accomplishments
- [Achievement 1] - [Impact]
- [Achievement 2] - [Impact]

### Current Focus
- [Priority 1] - [Expected completion]
- [Priority 2] - [Expected completion]

### Blockers & Risks
- **[Blocker/Risk]**: [Description] - [Mitigation plan]

### Next Week's Goals
- [Goal 1] - [Success criteria]
- [Goal 2] - [Success criteria]

### Metrics
- Velocity: [Current] (Target: [Target])
- Quality: [Bug count] open bugs
- Health: 🟢 On Track / 🟡 At Risk / 🔴 Blocked
```

## Milestone Review Template

### Milestone Assessment Format
```markdown
## Milestone Review: [Milestone Name]

### Milestone Summary
- **Target Date**: [Original date]
- **Actual Date**: [If completed] / [Current estimate]
- **Status**: ✅ Complete / 🔄 In Progress / ❌ Missed

### Success Criteria Assessment
- [ ] [Criterion 1] - [Met/Not Met] - [Notes]
- [ ] [Criterion 2] - [Met/Not Met] - [Notes]

### Key Deliverables
- [Deliverable 1]: [Status] - [Quality assessment]
- [Deliverable 2]: [Status] - [Quality assessment]

### Lessons Learned
- **What Went Well**: [Successes to replicate]
- **What Could Improve**: [Areas for improvement]
- **Process Changes**: [Recommended adjustments]

### Impact on Project
- **Schedule**: [On track/ahead/behind] - [Explanation]
- **Budget**: [Under/on/over budget] - [Explanation]
- **Scope**: [Any scope changes] - [Rationale]
```

## Risk Assessment Template

### Risk Evaluation Format
```markdown
## Risk Assessment: [Risk Name]

### Risk Description
[Clear description of the potential problem]

### Risk Classification
- **Category**: [Technical/Business/Resource/External]
- **Probability**: [High/Medium/Low] ([Percentage if known])
- **Impact**: [High/Medium/Low] ([Cost/schedule impact])
- **Risk Score**: [Probability × Impact]

### Impact Analysis
- **Schedule Impact**: [Effect on timeline]
- **Budget Impact**: [Financial implications]
- **Quality Impact**: [Effect on deliverables]
- **Team Impact**: [Effect on team/morale]

### Mitigation Strategy
- **Prevention**: [How to avoid the risk]
- **Mitigation**: [How to reduce impact if it occurs]
- **Contingency**: [Backup plan if risk materializes]

### Monitoring Plan
- **Indicators**: [Early warning signs]
- **Review Frequency**: [How often to reassess]
- **Owner**: [Who monitors this risk]

### Action Items
- [ ] [Preventive action] - [Owner] - [Due date]
- [ ] [Mitigation prep] - [Owner] - [Due date]
```

## Technical Debt Tracking Template

### Tech Debt Item Format
```markdown
## Technical Debt: [Item Name]

### Classification
- **Category**: [Code Quality/Testing/Performance/Security/Documentation]
- **Priority**: [High/Medium/Low]
- **Effort**: [Story points or time estimate]

### Description
[Clear description of the technical issue]

### Impact
- **Development Speed**: [How it slows development]
- **Maintenance Cost**: [Ongoing burden]
- **Risk**: [Potential problems if not addressed]
- **Business Impact**: [User-facing or business consequences]

### Root Cause
[Why this debt exists - rushed timeline, changing requirements, etc.]

### Proposed Solution
[Recommended approach to address the debt]

### Implementation Plan
- **Phase 1**: [First steps] - [Effort estimate]
- **Phase 2**: [Additional work] - [Effort estimate]

### Success Criteria
- [Measurable improvement 1]
- [Measurable improvement 2]

### Dependencies
- [Dependency 1] - [Why needed]
- [Dependency 2] - [Why needed]
```

## Change Request Template

### Change Request Format
```markdown
## Change Request: [Change Name]

### Change Summary
[Brief description of the requested change]

### Business Justification
[Why this change is needed]

### Impact Analysis
- **Scope**: [What parts of project are affected]
- **Schedule**: [Timeline impact] - [New dates if applicable]
- **Budget**: [Cost impact] - [Additional resources needed]
- **Quality**: [Quality implications]
- **Risk**: [New risks introduced]

### Implementation Options
1. **Option 1**: [Approach] - [Pros/Cons] - [Effort]
2. **Option 2**: [Approach] - [Pros/Cons] - [Effort]

### Recommendation
[Preferred option with rationale]

### Approval Required
- [ ] [Stakeholder 1] - [Role]
- [ ] [Stakeholder 2] - [Role]

### Implementation Plan
[If approved, how will this be executed]
```

---

## Usage Guidelines

### When to Use Each Template
- **Sprint Planning**: Start of each sprint/iteration
- **Daily Standup**: Every workday (keep brief)
- **Weekly Status**: End of each week for stakeholder communication
- **Milestone Review**: Upon reaching major project milestones
- **Risk Assessment**: When new risks are identified or quarterly reviews
- **Technical Debt**: When identifying code quality issues
- **Change Request**: When project scope or requirements changes

### Customization Notes
- Adapt templates to fit your project's specific needs
- Add project-specific metrics or sections as needed
- Maintain consistency across similar projects
- Archive completed templates for reference

### Tools Integration
These templates work well with:
- Markdown files in version control
- Project management tools (Jira, Azure DevOps, etc.)
- Wiki systems (Confluence, Notion, etc.)
- Communication platforms (Slack, Teams, etc.)

---

*Templates created: [Date]*
*Last updated: [Date]*
