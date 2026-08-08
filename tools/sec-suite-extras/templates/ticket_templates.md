# Ticket templates (GitHub issue & Jira)

Use these templates to create a reproducible remediation ticket from a finding.

---

## GitHub Issue Template

Title: [SEC][<Severity>] <Short title> — <Target>

Labels: security, triage, <severity>

Body:

**Finding ID:** {{id}}

**Title:** {{title}}

**Severity:** {{severity}}

**Target:** {{target}}

**Description:**
{{description}}

**Evidence:**
```
{{evidence}}
```

**Recommendation:**
{{recommendation}}

**References:**
- {{references}}

**Reported by:** {{reporter}}
**Date:** {{date}}

---

## Jira Ticket Template (copy into new issue)

Summary: [SEC][{{severity}}] {{title}} — {{target}}

Description:
h3. Finding
*ID:* {{id}}
*Tool:* {{tool}}
*Target:* {{target}}

{{description}}

h3. Evidence
{{evidence}}

h3. Recommendation
{{recommendation}}

h3. References
{{references}}

h3. Reporter
{{reporter}} — {{date}}

Priority: {{priority}}
Labels: security, triage
