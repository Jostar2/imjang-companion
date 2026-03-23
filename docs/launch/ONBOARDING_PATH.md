# Onboarding Path

## Activation target

The user reaches value when they:

1. create one project
2. add at least two properties
3. complete one visit
4. open comparison or report

Time-to-value target: under 20 minutes from first login to first completed visit.

## Current run default persona

Use this persona unless a stronger real lead appears:

- independent buyer agent
- 4 to 8 visits per month
- sends same-day follow-up to a client or partner
- currently uses chat, notes, and photo folders instead of a structured workflow

## Pilot kickoff prerequisites

Before the first live session, confirm:

- the operator already has a real shortlist or visit route
- one project name and target region are known
- at least two candidate properties can be entered during setup
- the user knows V1 is online-first and same-browser autosave only
- the founder has one support channel ready for same-day follow-up
- the pilot offer is stated clearly as `2-week founder-led pilot, KRW 149,000`

## First-session flow

1. Sign in
2. Create project
3. Add first property
4. Add second property
5. Start a visit
6. Fill required sections
7. Save notes and photos
8. Complete the visit
9. Open comparison
10. Open report

## Local demo success definition

The rehearsal counts as successful only if all of these happen in one pass:

1. create one project
2. add two properties
3. complete one visit with required sections
4. confirm draft restore behavior after refresh
5. confirm attachment retry story
6. open comparison
7. open report
8. make the pilot ask at the end of the walkthrough

## Facilitated pilot script

Use this for the first 20-minute onboarding call:

1. Confirm current workflow.
   Ask: "Where do visit notes, photos, and comparison decisions live today?"
2. Set expectation.
   Explain: "Today we will create one project, add two properties, complete one visit, and open the comparison/report surfaces."
3. Enter the first project and two properties together.
4. Let the user drive the first visit form while you only clarify required sections.
5. Pause after completion and ask what they would usually do next.
6. Open comparison and report.
7. Ask what is still missing before they would trust this on a live route.
8. Make the ask:
   "If this replaced part of your current visit-to-report workflow, would you test it in a 2-week guided pilot at KRW 149,000?"

## Instrumentation checkpoints

- project_created
- second_property_added
- visit_started
- visit_autosave_restored
- visit_completed
- attachment_retry_succeeded
- comparison_opened
- report_opened

## Rescue actions if the user stalls

- If the user never creates a second property:
  - remind them that comparison value appears only after at least two candidates.
- If the user starts a visit but does not complete it:
  - point to the required sections and finish one section live with them.
- If draft restore is needed:
  - refresh the page in the same browser and narrate what was restored and what was not.
- If attachment upload fails:
  - confirm visit data was still saved, then walk through retry.

## Rehearsal schedule

- `2026-03-24`: founder runs one solo local rehearsal
- `2026-03-25`: founder runs one timed rehearsal with the scripted pilot ask
- `2026-03-26` onward: only live workflow reviews after both rehearsals are clean

## Friction points to watch

- user adds only one property and stalls
- user starts a visit but never completes required sections
- autosave restore is needed but not obvious
- attachment retry copy is unclear

## Success definition for pilot week

- at least 3 pilot users reach `visit_completed`
- at least 2 pilot users open either comparison or report after completion
- at least 1 pilot user says they would replace part of their current note workflow with this flow
