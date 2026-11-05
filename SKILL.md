---
name: quantcorner-backtesting-efin-mcp
description: Research and explain long-only strategy behavior using Efin MCP historical data, a grill-me interview, auditable backtests, and portable QuantCorner reports. Includes first-install onboarding and provider coverage checks. No shorting or order execution.
metadata:
  display_name: QuantCornerBacktestingEfinMCP
  version: 0.3.0
---
# QuantCornerBacktestingEfinMCP

Use backtesting to understand strategy behavior, not to promise that a strategy “works”. Follow the user's language; do not assume their identity, machine paths, data entitlements, or risk preferences.

## Suite entry points

This original entry point remains supported and owns the shared engine, metric formulas, assets and research gates. For choosing a stage, use ask-quantcorner; focused entry points are qc-setup, qc-design-strategy, qc-audit-data, qc-backtest, qc-validate, qc-explain-results and qc-report. Read `references/suite.md` before working across stages. Resolve installed siblings by name or checkout members under skills/. If the host has no skill-invocation tool, read the selected SKILL.md and follow it in the same session. Never force an existing result through unrelated setup stages.

## Command help

For help, commands, or first-time usage, read `references/commands.md`. Use the English request names documented there consistently when presenting command help. Reuse an existing authenticated Efin MCP connection; do not ask the user to reinstall it. Preserve the user’s preferred conversation language. Explain conversational requests separately from executable CLI commands; never invent registered slash commands. For metric interpretation, follow `references/metrics.md`, including chapter-14 trade statistics, costs, and drawdown recovery status.

## First use and portability

Resolve this skill's directory at runtime. Read `references/onboarding.md` and run `python3 scripts/onboard.py --workspace <research-folder>`. The helper checks Python and creates private local state and a draft plan; it does **not** install or authenticate Efin. Discover the host's actual Efin tools, inspect their current schemas, and run the read-only smoke test in `references/efin.md`. Record capabilities and missing coverage. Recheck when the client, provider, or schema changes. Never invent a server URL, token variable, login flow, missing bars, or adjustment metadata.

Skill files and synthetic examples are shareable. Efin responses, generated real-data reports, credentials, user plans, and research logs stay private unless their owner explicitly authorizes a specific export and has redistribution rights. Installing this skill is not consent to publish future runs.

## Interview: use grill-me

Invoke the installed `mattpocock-grill-me` or `grill-me` skill when available. If absent, transparently use this package's self-contained `references/grill-me.md` interview protocol; it preserves one question at a time with a recommended answer. Do not silently install an unrelated dependency. Ask only unresolved questions, read supplied artifacts first, and retain answers across turns. Discover available tools before asking users to describe capabilities.

Resolve: research question/economic mechanism; securities and historical universe; time horizon and holdout; signal and next executable price; cash/lot/cost constraints; benchmark; planned sensitivity checks; output language and sharing needs. Short selling and leverage are unsupported. Do not imply all stocks use the same lot size. Record unresolved assumptions; get agreement on material assumptions before running empirical research, rather than repeatedly requesting approval for routine steps already authorized.

## Six-stage research contract

Read `references/framework.md` for details, `references/efin.md` before acquisition, and `references/metrics.md` when interpreting ratios.

1. **Question:** define expected behavior and evidence that would challenge the hypothesis.
2. **Plan:** save the hypothesis, universe, dates/splits, execution/cost assumptions, benchmark, and robustness plan. Keep exploration and confirmation distinct.
3. **Integrity gate:** point-in-time availability, delistings, OHLC/corporate actions, data completeness, signal-before-fill, execution and accounting. Unknown coverage remains visible. Invalid inputs stop performance interpretation.
4. **Development:** simple baseline, parameter/cost/regime sensitivity, full trial history. Use only development data for fitting. Do not cherry-pick trials or search until a desired Sharpe appears.
5. **Held-out evaluation:** freeze the candidate and evaluate the pre-specified unseen period. Record access before reading results. If used to change the model, it is now development data; require new evidence. Historical holdouts are not perfectly independent of prior knowledge.
6. **Behavior report:** explain return, drawdown/recovery, volatility, risk-adjusted ratios, trade outcomes, costs, sample size, uncertainty and benchmark tradeoffs. Choose further research, pause, or forward observation. Never place orders.

## Tools and deterministic helpers

- `scripts/onboard.py`: local environment check and non-destructive workspace setup.
- `scripts/normalize_efin.py`: normalize explicitly saved Efin historical pages; reject malformed, duplicate, nonfinite, incomplete or ambiguous pages. No live connection is embedded in this script.
- `scripts/research.py`: run a plan against audited bars; append trial events, guard held-out reuse and retain hashes, config and provenance. Read the CLI help. Use this wrapper for empirical runs.
- `scripts/engine.py`: transparent **single-asset daily long-only reference engine**, SMA or precomputed target signals with next-open fills. Its low-level `run` function is useful for tests; it does not replace the research gates. No automatic factor portfolio, portfolio aggregation, tick microstructure, dividends, rights, split adjustment, walk-forward fitting, or shorting. For unsupported designs, state the extension required and validate it before use. Never silently approximate a portfolio with independent-stock averages.
- `scripts/report.py`: standalone offline HTML with embedded QuantCorner logo, local fonts, equity/drawdown charts, metric definitions, assumptions and limitations. No CDN, telemetry, fabricated charts, or image generation. For a demo, label synthetic data prominently. Use `references/visual.md` for presentation rules.

## Deliverables and verification

Return the report plus a compact account of the hypothesis, coverage, execution assumptions, findings, contradictory evidence and next question. Keep plan, bars/provenance hashes, code version, all trial events, engine outputs and notes in the private workspace. Mark undefined metrics N/A. MDD is not annualized; ratios must use consistent units/frequencies. Separate closed-trade P&L from still-open mark-to-market P&L. Never label an unknown price basis “adjusted” or price-only return “total return including dividends”.

Before completion run input/accounting checks and inspect the generated report at desktop and mobile width when rendering is available. Tests verify helpers, not the truth of an investment hypothesis. State precisely whether verification was synthetic unit tests, live provider smoke tests, or actual historical research.
