# Google Sheets Data Mapping

This document describes the exact column mapping between the FastAPI response and Google Sheets.

## Sheet Structure

**Sheet Name:** `Leads` (or your preferred name)

## Column Definitions

| Column | Type | Description | Source Field |
|--------|------|-------------|--------------|
| `timestamp` | Text/DateTime | ISO8601 timestamp when lead was processed | `timestamp` |
| `name` | Text | Lead's name (normalized) | `name` |
| `email` | Text | Lead's email (normalized, lowercase) | `email` |
| `company` | Text | Company name (normalized) | `company` |
| `message` | Text | Original lead message | `message` |
| `source` | Text | Lead source (e.g., "website_form", "linkedin") | `source` |
| `intent` | Text | AI-analyzed intent | `intent` |
| `urgency` | Text | Urgency level: "low", "medium", or "high" | `urgency` |
| `budget_range` | Text | Budget range if mentioned, empty if null | `budget_range` |
| `summary` | Text | AI-generated summary (max 2 sentences) | `summary` |
| `lead_score` | Number | Lead quality score (0-100) | `lead_score` |
| `next_action` | Text | Recommended next action | `next_action` |
| `dedupe_key` | Text | Deduplication key (email or hash) | `dedupe_key` |
| `raw_payload_json` | Text | Original request payload as JSON string | `raw_payload_json` |

## Make.com Google Sheets Module Configuration

### For "Add a row" operation:

**Spreadsheet:** Select your Google Sheets spreadsheet
**Sheet:** Select the "Leads" sheet
**Map the following fields:**

```
timestamp → timestamp
name → name
email → email
company → company
message → message
source → source
intent → intent
urgency → urgency
budget_range → budget_range
summary → summary
lead_score → lead_score
next_action → next_action
dedupe_key → dedupe_key
raw_payload_json → raw_payload_json
```

### For "Update a row" operation:

**Search criteria:**
- **Column:** `dedupe_key`
- **Value:** `{{dedupe_key}}` (from FastAPI response)

**Update fields:** Map all fields same as "Add a row" above

## Example Row Data

```
timestamp: 2024-01-15T10:30:00Z
name: John Doe
email: john@example.com
company: Acme Inc
message: We need an AI lead system. Budget 5k. ASAP
source: website_form
intent: seeking AI automation services
urgency: high
budget_range: 5k
summary: Lead is interested in AI lead system with budget of 5k. Requires ASAP implementation.
lead_score: 75
next_action: schedule discovery call to discuss requirements
dedupe_key: john@example.com
raw_payload_json: {"name":"John Doe","email":"JOHN@EXAMPLE.COM","company":"Acme Inc","message":"We need an AI lead system. Budget 5k. ASAP","source":"website_form"}
```

## Notes

- **Deduplication:** Use `dedupe_key` column to search for existing leads before adding
- **Empty values:** Google Sheets will show empty cells for null values (e.g., budget_range)
- **Data types:** Ensure `lead_score` is formatted as a number in Google Sheets
- **Timestamp format:** ISO8601 format is human-readable and sortable in Google Sheets

