# Health MCP Server 🏥

Health and medical data for AI agents — drug information, adverse events, clinical trials, and WHO global health statistics.

## Features

- **Drug Search** — Find drug info, dosage, warnings via OpenFDA
- **Adverse Events** — Check reported side effects from FAERS
- **Clinical Trials** — Search ClinicalTrials.gov for ongoing/completed studies
- **WHO Statistics** — Global health indicators from the WHO Observatory
- **No API Key** — All public APIs, completely free

## Installation

```bash
pip install health-mcp-server
```

## Tools

| Tool | Description |
|------|-------------|
| `search_drugs` | Drug info, dosage, warnings |
| `search_adverse_events` | Reported side effects |
| `search_clinical_trials` | Clinical trials search |
| `get_health_statistics` | WHO health data by indicator |
| `list_health_indicators` | Available WHO indicators |

## Disclaimer

This server provides access to publicly available health data for informational purposes only. It is NOT a substitute for professional medical advice.

## License

MIT
