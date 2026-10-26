<?php
/**
 * Axiom CRM Sync (GoHighLevel)
 * Sends saved, non-spam Get Started form entries (Jetpack form 1096) to the
 * Axiom GoHighLevel sub-account: contact upsert (email/phone), one note per
 * entry, then the axiom-new-lead tag that starts the existing workflow.
 *
 * - The submission hook only saves a field snapshot and queues a background
 *   job (Action Scheduler); no API call happens in the visitor's request.
 * - The Jetpack entry, the Gmail notification and Google Ads tracking are not
 *   touched. If the CRM is unreachable, the job retries, then emails an alert.
 * - Token: AXIOM_GHL_PRIVATE_TOKEN (site configuration file). Only placed in the
 *   Authorization header of server-side requests; never stored, shown or logged.
 * - Modes (Tools > Axiom CRM Sync): off, dry-run (default: builds the payload,
 *   no GoHighLevel requests), test (writes only for listed test emails, with a
 *   test tag), live. Verification makes GET requests only. Write requests are
 *   refused unless the mode is test or live.
 * Rollback: unpublish this snippet. Entries keep their sync status meta.
 */
namespace AngieSnippets\AxiomCrmSync_1398;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const FORM_ID          = 1096;
const DEFAULT_LOCATION = 'WSbB7bUher6I1M2VNlZz';
const API_BASE         = 'https://services.leadconnectorhq.com';
const API_VERSION      = '2021-07-28';
const LEAD_TAG         = 'axiom-new-lead';
const TEST_TAG         = 'axiom-integration-test';
// Production pipeline the Instant New Lead Response workflow writes to. Verification
// resolves it to an ID; only the read-only opportunity check uses it.
const PIPELINE_NAME    = 'Axiom Sales & Client Acquisition';
const STAGE_NAME       = 'New Lead';
const ALERT_TO         = 'axiom.systems.co@gmail.com';
const SOURCE           = 'Website: Get Started form';
const OPT              = 'axiom_ghl_sync_settings';
const META_STATE       = '_axiom_ghl_state';
const META_SNAPSHOT    = '_axiom_ghl_snapshot';
const META_LOCK        = '_axiom_ghl_lock';
const JOB              = 'axiom_ghl_sync_entry';
const CHECK_JOB        = 'axiom_ghl_check_opportunity';
const GROUP            = 'axiom-ghl';
const RETRY_DELAYS     = array( 60, 300, 1800, 7200, 43200 );

require_once __DIR__ . '/capture.php';
require_once __DIR__ . '/delivery.php';
require_once __DIR__ . '/verify.php';
require_once __DIR__ . '/admin.php';
