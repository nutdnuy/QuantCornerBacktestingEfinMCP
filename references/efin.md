# Efin MCP adapter

Observed schemas on 2026-11-05; discover current host tool names and inspect schemas before each new integration. Prefixes differ across clients. Do not hard-code a particular tool namespace or server endpoint.

| Purpose | Tool suffix | Important boundary |
|---|---|---|
| Stock daily OHLC | efin_market_price_history_get | Up to 10 years; excludes current day; max100 rows/page |
| Index daily OHLC | efin_set_index_history_get | Separate endpoint; index is not an executable stock |
| Company status | efin_set_stock_profile_get | Current attributes are not historical facts |
| Universe search | efin_set_stock_search | Latest index review, not point-in-time membership |
| Corporate actions | efin_set_stock_benefit_get | XD/XR/etc; audit events before cash-flow handling |

Read-only probe: request PTT and SET separately over 2025-01-02..2025-01-10. Observed 7 rows each. Do not require that exact count forever: inspect actual returned range/count and calendar. Test stock pagination with limit3 as well as the normal limit. In this session it returned 3+3+1 with no overlap. These observations are a smoke test, not a multi-year backtest.

History payload: use `structuredContent` when provided, otherwise parse the tool's JSON text. Observed envelope has `meta` and `data`; rows at `data.data`. Row fields include `date,open,high,low,close,volume_shares`. Metadata includes `symbol,currency,data_source,as_of,result_count,total_count,has_more,next_cursor`; actual range is in `data.range_from/range_to`. Page summaries are page-local.

Always continue while `has_more` is true with the identical parameters and limit, using the returned opaque cursor. Cursor lifetime is approximately15 minutes; restart on expiry and audit/deduplicate explicitly. Never treat null/absent `has_more` as proven completeness. Save ordered full payload pages in one JSON list for `normalize_efin.py`; a single payload object also works. Detect provider errors and mock data. The normalizer rejects duplicate dates rather than silently choosing a row.

Unknown/missing OHLC is not zero; zero volume means no trading, not a fill opportunity. Compare coverage with the exchange calendar and requested window outside the normalizer; metadata completeness does not prove no missing trading days. Do not append a latest-price snapshot as a historical day.

No price-adjustment declaration or adjustment-factor series was present in the observed schema/response. Do not claim adjusted, raw, or total-return data. Resolve the basis from provider evidence and audit corporate actions before a qualified run; otherwise label a specifically authorized price-only diagnostic with `price_basis=unknown` and clear limitations.

Corporate actions return grouped records per symbol and XD/XR/etc, with pagination `offset_per_group`/`limit_per_group` (not history cursors). Monetary amounts may be formatted strings; `-` and null are unknown, not zero. No announcement timestamp or factor series was observed. The reference engine does not implement corporate-action cash flows. Current membership with status ALL helps find delisted symbols but does not reconstruct historical membership.

Never ship real responses, cursors, credentials or licensed datasets in the public package. Every recipient supplies their own authenticated connection and observes their provider's licensing terms.

## Evidence fields required by the local runner

Audit flags are caller attestations backed by reviewable evidence, not automatic facts established by the helper. Preserve provider documentation and the actual calendar/action checks privately. Never flip audit flags just to make a run pass.

- `calendar_audit="passed"` plus `calendar_audit_evidence`: the checked calendar, requested span and gap resolution.
- `price_basis` plus `price_basis_evidence`: provider-confirmed basis and its source.
- `corporate_actions="audited"`, `corporate_action_policy="no_actions_in_window"` and `corporate_actions_evidence`: evidence that no relevant action affects the complete input window (including warmup).

Because this engine does not process shares/cash flows, only documented raw/unadjusted prices with that no-actions policy qualify for ordinary execution. Split-adjusted, total-return-adjusted, unknown or unsupported price bases, actions within the window, or missing basis/action evidence require explicit `price_only_diagnostic_acknowledged=true`; results remain a limited price-series diagnostic. Adjusted historical OHLC are not claimed to be actual executable prices. No dividend-inclusive investment return is inferred. Supporting other action policies requires a separately implemented and tested accounting engine.

The runner verifies the normalizer's `bars_sha256`, count/range, currency and symbol. Changing bars or adding targets requires a new, documented derived snapshot with recomputed hash and preserved parent provenance; do not silently alter normalized data. All workspaces share one trial registry per research project; starting another workspace does not restore holdout independence.
