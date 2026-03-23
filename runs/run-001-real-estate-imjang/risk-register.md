# Risk Register

| Risk ID | Severity | Description | Mitigation | Owner |
|---|---|---|---|---|
| R-001 | high | attachment upload path introduces the most integration risk | stage upload flow early, limit size, add failure UX | architect / infra |
| R-002 | medium | checklist scope can sprawl and slow implementation | freeze a minimal taxonomy for v1 | planner |
| R-003 | medium | comparison scoring can become arbitrary or misleading | keep score logic simple and transparent in v1 | architect |
| R-004 | medium | mobile session loss can hurt visit workflow | add autosave assumption and revisit offline after MVP | frontend |
| R-005 | high | report generation may depend on too many unfinished fields | keep report as structured web view first, not PDF export | planner / frontend |
