# Analytics Event Map

## Core activation events

| Event | Trigger | Why it matters | Required properties |
| --- | --- | --- | --- |
| `project_created` | first project is created | start of meaningful workspace setup | `project_id`, `region`, `budget_present` |
| `property_created` | each property is added | indicates evaluation intent | `project_id`, `property_id`, `property_type`, `listing_price_present` |
| `second_property_added` | second property is added | strong signal for comparison use case | `project_id`, `property_count` |
| `visit_started` | visit record is created | start of field workflow | `project_id`, `property_id`, `visit_id`, `visit_date` |
| `visit_autosave_restored` | local draft is restored after refresh | validates draft recovery behavior | `project_id`, `property_id`, `visit_id`, `restored_sections`, `restored_attachment_names_count` |
| `visit_completed` | required sections are complete and visit is marked complete | core activation step | `project_id`, `property_id`, `visit_id`, `total_score`, `red_flag_count`, `attachment_count` |
| `attachment_upload_failed` | upload fails but visit remains saved | measures reliability pain | `project_id`, `visit_id`, `category`, `error_code` |
| `attachment_retry_succeeded` | failed upload later succeeds | validates recovery UX | `project_id`, `visit_id`, `category`, `retry_count` |
| `comparison_opened` | comparison page is opened | confirms evaluation workflow | `project_id`, `property_count`, `completed_visit_count` |
| `report_opened` | report page is opened | confirms summary delivery value | `project_id`, `visit_id`, `property_id` |

## Business validation events

| Event | Trigger | Why it matters | Required properties |
| --- | --- | --- | --- |
| `pricing_viewed` | pricing or offer material is opened | tracks commercial interest | `persona_hint`, `channel` |
| `pilot_requested` | pilot form or outbound reply indicates interest | top-of-funnel quality | `persona_hint`, `channel`, `source_campaign` |
| `report_shared` | report is copied, shared, or exported later | strong indicator of operator value | `project_id`, `visit_id`, `share_target` |

## Minimum funnel

`project_created -> second_property_added -> visit_completed -> report_opened -> pilot_requested`

## Dashboard views to maintain

- Activation dashboard:
  - users who created a project
  - users who added a second property
  - users who completed a visit
  - users who opened comparison or report
- Reliability dashboard:
  - attachment upload failure rate
  - autosave restore rate
  - visits started vs visits completed
- Commercial dashboard:
  - pilot requests by persona
  - pricing views by channel
  - report sharing rate among pilot accounts

## Weekly review questions

- Where do users drop before `visit_completed`?
- Do buyer agents and investor teams activate differently?
- Are users opening comparison and report in the same session or later?
- Is attachment failure materially blocking pilot trust?
