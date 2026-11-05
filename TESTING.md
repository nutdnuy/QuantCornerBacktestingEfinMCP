# Verification evidence — 2026-11-05

## v0.2 additions

51 tests pass locally on Python3.9: the previous43 plus8 hand-computable chapter-14 checks covering recovery intervals, unresolved episodes, deepest-versus-longest drawdowns, no drawdown, flat trades, payoff threshold, fee/slippage reconciliation and open-position costs. Synthetic report regenerated; desktop1440/mobile390 checks found no horizontal overflow or missing logo. Guide documents every public CLI and its actual arguments, separates conversational prompts from terminal commands, and identifies the low-level bypass boundary. Live Efin integration evidence below is from v0.1; this update changes metrics/docs, not the provider adapter.


## Deterministic checks

43 tests passed locally with Python3.14 using `python3 -m unittest discover -s tests -v`:

- 12 engine checks: next-open causality, future-price perturbation, fees/slippage/affordability, board lots, zero-volume fills, warmup, drawdown, liquidation, open P&L reconciliation, invalid inputs, undefined ratios.
- 18 workflow checks: provider envelopes/pagination, nonfinite/duplicate/inconsistent bars, repeated cursors, provenance hashes/count/range, explicit audit evidence, price-basis/corporate-action gates, approved assumptions, holdout reuse, failed-run reservation, concurrent lock, private snapshots and reproducible hashes.
- 10 report checks: malformed data, N/A metrics, escaping, synthetic labeling, logo requirement, constant/single-point curves, font weights, responsive structures and research record.
- 3 setup checks: fresh non-destructive onboarding, portable install/refusal to overwrite, exclusion of arbitrary files and symlinks.

The synthetic demo exercises plan → runner → ledger/metrics → report (800 generated rows, 750 evaluation observations, 8 closed trades). Its smooth sine-wave fixture is intentionally artificial. It is not a credible investment opportunity, a market forecast, or an empirical test of a security.

The skill-creator metadata validator passed. Canonical Codex/Claude symlinks resolve to the same source. The broader personal catalog has pre-existing unrelated findings; the new skill has no reported catalog findings. This package does not claim that the entire host catalog passed.

GitHub Actions runs the suite and synthetic demo on Python3.9 and3.12 using Ubuntu22.04 for each push/PR. The first run exposed that ubuntu-latest (26.04) has no Python3.9 build; the workflow now pins a compatible runner; see the repository's Actions history for the actual run status.

## Live Efin integration

An already authenticated host was tested with read-only Efin MCP calls: PTT and SET over2025-01-02..2025-01-10 returned7 rows each. Actual PTT pagination with limit3 returned3+3+1 and was passed in memory through `normalize_efin.py`;7 unique sorted rows, SET source and unknown adjustment basis were preserved. No market responses or cursor tokens were published. This verifies adapter behavior on a small sample, not full historical coverage or investment performance. Clean-account Efin authorization was not tested; onboarding instructions deliberately use the recipient's licensed host connection.

## Visual and instruction review

A real Chromium render was inspected at1440px and390px. No horizontal page/chart/table overflow, no missing assets and no external font/data requests were observed. Dates at both ends of the sample fit, mobile shows both strategy/benchmark metrics, and plotted drawdown/return matched the result file. The HTML embeds fonts and the unchanged QuantCorner mark. Fixed report labels are English; Thai user content is supported by embedded Thai fonts.

An independent agent reviewed three instruction scenarios: no Efin connection, requests to optimize until Sharpe is high, and unknown adjustment basis presented as full validation. This was a proxy review of instructions, not a measured multi-model evaluation or proof that every host agent will comply.

## Limits

Single-asset daily long-only reference engine; no shorting, leverage, order placement, portfolio aggregation, walk-forward fitting, corporate-action accounting, participation/microstructure model or PIT-universe reconstruction. Audit fields and candidate locking are operator attestations with supporting evidence. Workspace locks and append-only events are operational controls, not tamper-proof storage; a separate workspace cannot erase previously inspected information. Historical results remain observations under their stated assumptions.
