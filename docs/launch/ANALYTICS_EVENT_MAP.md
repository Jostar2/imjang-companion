# Analytics Event Map

## Core activation events

| Event | Trigger | Why it matters |
| --- | --- | --- |
| `project_created` | first project is created | start of meaningful workspace setup |
| `property_created` | each property is added | indicates evaluation intent |
| `second_property_added` | second property is added | strong signal for comparison use case |
| `visit_started` | visit record is created | start of field workflow |
| `visit_autosave_restored` | local draft is restored after refresh | validates draft recovery behavior |
| `visit_completed` | required sections are complete and visit is marked complete | core activation step |
| `attachment_upload_failed` | upload fails but visit remains saved | measures reliability pain |
| `attachment_retry_succeeded` | failed upload later succeeds | validates recovery UX |
| `comparison_opened` | comparison page is opened | confirms evaluation workflow |
| `report_opened` | report page is opened | confirms summary delivery value |

## Business validation events

| Event | Trigger | Why it matters |
| --- | --- | --- |
| `pricing_viewed` | pricing or offer material is opened | tracks commercial interest |
| `pilot_requested` | pilot form or outbound reply indicates interest | top-of-funnel quality |
| `report_shared` | report is copied, shared, or exported later | strong indicator of operator value |

## Minimum funnel

`project_created -> second_property_added -> visit_completed -> report_opened -> pilot_requested`
