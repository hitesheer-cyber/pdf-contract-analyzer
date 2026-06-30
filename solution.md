# Solution

This document summarizes the work done on the **pdf-contract-analyzer** backend.

## Summary

The existing pytest suite passed but never exercised the real PDF-extraction path,
so two bugs went undetected: uploads of valid PDFs failed during NLP extraction, and
the CORS configuration silently ignored its environment variable. Both are fixed below.

## Changes

### 1. Fixed missing imports in `nlp_service.py` (critical)

`backend/app/services/nlp_service.py` referenced `torch`, `AutoTokenizer`,
`AutoModelForTokenClassification`, and `pipeline` without importing them. As a
result, **every valid-PDF upload failed extraction** and the contract was marked
`failed`.

Added the imports at the top of the module:

```python
import torch
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    pipeline,
)
```

Note: imports are kept at module top (not lazy-imported inside `_initialize_model`).
This means the app hard-depends on `torch` loading at import time, so the
environment must have the VC++ redistributable installed for `torch` to load.

### 2. Fixed ignored CORS environment variable in `config.py` (minor)

`backend/app/config.py` mapped the `cors_origins_str` field to the env var
`CORS_ORIGINS_STR`, but the `.env` file sets `CORS_ORIGINS`. The configured origins
were therefore silently ignored and the defaults always won.

Added an explicit validation alias so the documented `CORS_ORIGINS` variable is honored:

```python
from pydantic import Field

cors_origins_str: str = Field(
    default="http://localhost:3000,http://localhost:8000",
    validation_alias="CORS_ORIGINS",
)
```

## Known open issues (not yet addressed)

These were surfaced by a live upload but are out of scope for the fixes above:

- **DATE / MONEY never extracted.** The `dslim/bert-base-NER` model only emits
  PER/ORG/LOC/MISC, while the analytics layer treats `{PERSON, ORG, DATE, MONEY}` as
  key types. Every contract is therefore permanently flagged as "missing DATE, MONEY".
  Addressing this needs regex/heuristic extraction or a different model.
- **Subword tokens not merged.** Token-classification output is not aggregated
  cleanly — e.g. a single "Acme Corporation" can yield garbage entities like `"A"`
  and `"##cme Corporation"` alongside the correct one. This inflates entity counts
  and pollutes `most_frequent_entities`. Likely needs `aggregation_strategy="simple"`
  or a corrected merge of `##` continuation tokens.
