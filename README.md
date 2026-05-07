# Reporting API — Technical Documentation
> AuditFlow · Suivi de Recommandation · Python 3.12.3

---

## Definition

The **Reporting API** is a backend service within AuditFlow that generates PDF performance reports destined to directors. It is triggered from the **Suivi de Recommandation** page, consuming audit data filtered by mission or date range, and rendering a KPI summary on recommendation and action implementation.

---

## Role

Receive structured audit data → validate it → compute KPIs → render a director-facing PDF report.

---

## Workflow

```
[Start]

[Input]
  Mandatory : data payload (filtered by mission_id or date_range)
              subtitle : str
  Optional  : comments  : str
              reference : str

[Data Validation]
  - Schema and type checking
  - Required fields presence
  - Status enum consistency
  - Date range logic (from < to)

[KPI Calculation]
  - Recommendation implementation rate
  - Action completion rate
  - Status breakdown (count + %)
  - Priority distribution

[Template Population & PDF Rendering]
  - Inject KPIs and metadata into HTML template
  - Render HTML → PDF via WeasyPrint

[End] → returns application/pdf binary
```

---

## Input Schema

```json
{
  "mission_id"            : 101,
  "recommendation_id"     : 5,
  "recommendation"        : "string",
  "action"                : "string",
  "action_status"         : "in_progress",
  "recommendation_status" : "partially_implemented",
  "subtitle"              : "string",
  "comments"              : "string",
  "reference"             : "string"
}
```

| Field | Type | Required |
|---|---|---|
| `mission_id` | int | ✓ (or `date_range`) |
| `date_range` | object `{ from, to }` | ✓ (or `mission_id`) |
| `subtitle` | str | ✓ |
| `recommendation_id` | int | ✓ |
| `recommendation` | str | ✓ |
| `action` | str | ✓ |
| `action_status` | str (enum) | ✓ |
| `recommendation_status` | str (enum) | ✓ |
| `comments` | str | — |
| `reference` | str | — |

---

## Dependencies

```toml
[project]
requires-python = ">=3.12.3"

dependencies = [
    "fastapi==0.115.12",
    "uvicorn[standard]==0.34.2",
    "pydantic==2.11.4",
    "weasyprint==65.1",
    "jinja2==3.1.6",
    "pandas==2.2.3",
]

[project.optional-dependencies]
dev = [
    "pytest==8.3.5",
    "httpx==0.28.1",
    "ruff==0.11.10",
]
```

---

## Project Structure

```
reporting-api/
│
├── pyproject.toml
│
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Settings
│   │
│   ├── api/
│   │   └── reports.py           # POST /api/v1/reports/generate
│   │
│   ├── schemas/
│   │   ├── request.py           # ReportRequest model
│   │   ├── record.py            # AuditRecord model
│   │   └── enums.py             # ActionStatus, RecommendationStatus
│   │
│   ├── services/
│   │   ├── validator.py         # Validation logic
│   │   ├── calculator.py        # KPI computation
│   │   └── renderer.py          # Template → PDF
│   │
│   └── templates/
│       └── report.html          # Jinja2 HTML template
│
└── tests/
    ├── test_validator.py
    ├── test_calculator.py
    └── test_api.py
```

---

## Error Handling

| HTTP Code | Cause |
|---|---|
| `200` | PDF generated successfully |
| `400` | Conflicting filters / empty dataset |
| `422` | Schema or type validation failure |
| `500` | PDF rendering failure |

```json
{
  "code"      : "REPORT_002",
  "message"   : "No records found for the given filter.",
  "timestamp" : "2025-05-07T10:30:00Z"
}
```

| Code | Trigger |
|---|---|
| `REPORT_001` | Missing or conflicting filter |
| `REPORT_002` | Empty dataset |
| `REPORT_003` | Invalid date range (`from` > `to`) |
| `REPORT_004` | Unknown status enum value |
| `REPORT_005` | PDF rendering failure |
