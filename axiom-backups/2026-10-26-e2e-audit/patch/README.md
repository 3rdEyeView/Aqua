# Snippet 1398 patch: opportunity check → production pipeline (NOT DEPLOYED, awaiting approval)

`backup-live/` = the five live files, fetched 2026-10-26 and byte-identical to `../../2026-10-23-ghl-integration/split/`.
`split/` = patched files. `snippet-1398.patch` = unified diff. `harness.php` = offline tests (52 pass on `split/`).

## What changes (read-only verification and logging only)
| File | Change |
|---|---|
| main.php | `PIPELINE_NAME` "AXIOM Standard Client Pipeline" → "Axiom Sales & Client Acquisition" |
| verify.php | Verification lists every pipeline's ID + stages (`pipeline_ids`) and stores the production pipeline's ID even if no stage is called "New Lead"; new admin-only REST action `check` re-runs the opportunity check for one entry |
| delivery.php | The check makes one GET `/opportunities/search?location_id&contact_id` (no pipeline filter) and logs "X open / Y total in Axiom Sales & Client Acquisition", plus any opportunities in other pipelines by ID (template-isolation evidence) |

Unchanged: contact upsert, source, note, tag, retries, alerts, modes, field map, form, workflows, tracking. The check
still uses `api()` without write permission, so it can only send GET requests.

## Deploy steps (after approval)
1. Save `split/main.php`, `split/verify.php`, `split/delivery.php` into snippet 1398 (capture.php/admin.php unchanged); diff live vs `split/`; publish.
2. Run verification (GET only). Confirm `axiom_pipeline.pipeline_id` and `pipeline_ids` show "Axiom Sales & Client Acquisition (New Lead, Appointment Booked, …)". Settings then store that ID.
3. Prove the ID empirically: POST `axiom/v1/crm-sync` `{"action":"check","entry":1402}` (one GET). Expected: "1 open / 1 total in Axiom Sales & Client Acquisition", matching the Opportunities dashboard.
Rollback: save `backup-live/` files back and publish; run verification again only if the old pipeline ID is wanted.
