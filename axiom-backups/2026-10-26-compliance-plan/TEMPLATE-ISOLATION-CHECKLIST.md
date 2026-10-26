# Checklist: CLIENT TEMPLATE workflows cannot enrol Axiom production leads (read-only, owner in GHL)

For each published "CLIENT TEMPLATE | …" workflow and "| Facebook & Instagram DM Auto Response":
1. Open it (do not edit or save). Note trigger(s), every trigger filter, created date, and "allow re-entry".
2. It is isolated if every trigger is filtered to something production never uses (a client-only tag, form, calendar,
   phone number or pipeline — not "Axiom Sales & Client Acquisition"). It is a risk if a trigger is any of:
   tag added `axiom-new-lead` (or no tag filter), Contact Created, any Form Submitted, Customer Replied (no filter),
   Call Status / inbound call (no number filter), Appointment events on any calendar or an Axiom calendar,
   Opportunity stage/status changes with no pipeline filter or on Axiom Sales & Client Acquisition,
   Facebook/Instagram message on a connected Axiom page.
3. Check "Stop Lead Follow-Ups" actions: if unfiltered, a reply from an Axiom lead could remove tags or end production workflows.
4. Enrolment evidence: open the Axiom test contacts (incl. MWWqo11piJdDiATUmsze) → Workflows/Activity tab: only
   production workflows should be listed. The booked test contact should have exactly one confirmation and one set of reminders.
5. Pipeline evidence: the integration's opportunity check now lists opportunities in other pipelines for each new lead
   (Tools → Axiom CRM Sync → log). "AXIOM | Standard Client Pipeline" should stay empty for Axiom leads.
Record each workflow as Isolated / Risk / Unclear. Any Risk: report before changing anything (change A6 needs approval).
