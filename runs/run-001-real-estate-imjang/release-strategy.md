# Release Strategy

## Staging target

The first release candidate must prove:

- project creation
- property creation
- visit checklist completion
- note/score persistence
- comparison view
- report view

## Sequencing

1. project/property CRUD
2. visit session and checklist responses
3. score aggregation and comparison shell
4. attachment upload path
5. summary report
6. staging smoke and release checklist

## Manual gates

- production deploy
- attachment storage policy change
- permission model expansion
- any schema migration beyond additive changes

## Rollback posture

- if upload path is unstable, disable upload and keep visit flow alive
- if comparison/report regresses, preserve visit capture and hide summary route
- if checklist completion fails, block release candidate
