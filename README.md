# outbound-email-guardrails

Pre-send **guardrails for AI sales agents** (AI SDRs): lint every machine-written email before it leaves, then apply a
per-domain daily cap so a bad prompt cannot burn a sending domain.

## Checks
`unresolved_token` (`{{first_name}}` shipped to a prospect), `no_unsubscribe`, `spam_words`, `ungrounded_claim`
(numeric claims must exist in an approved fact sheet, so the agent cannot invent "5000 customers"), `too_long`,
`suppressed_recipient`, plus `daily_cap` per sending domain.

## Run
```bash
pip install pytest
python -m pytest -q
PYTHONPATH=src python -m guard.cli data/emails.json
```
Sample: 8 drafts, 2 sent, 6 held, each with the reason.

## Extend
Feed real drafts and the real fact sheet; add reply-rate feedback; add an LLM check only for tone, keep compliance checks deterministic.
