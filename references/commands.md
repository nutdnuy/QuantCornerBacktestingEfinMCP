# Command reference

## Agent requests

Invoke `$quantcorner-backtesting-efin-mcp`, followed by one of the requests below. These are natural-language instructions to the agent, not registered slash commands or shell subcommands. You can add a symbol, dates, or an existing plan to make a request more specific.

| Request | What the agent does |
|---|---|
| `Show available commands` | Explain the available requests, terminal commands, required inputs, and outputs. |
| `Set up my workspace` | Check Python and bundled assets, initialize private research files, and verify the existing Efin MCP connection. Reuse an authenticated connection; only guide connection setup when it is missing. |
| `Define my strategy with grill-me` | Ask one question at a time to clarify the hypothesis, instruments, dates, trading rules, costs, and intended learning. |
| `Audit Efin data for PTT` | Retrieve data through the connected Efin MCP and inspect schemas, pagination, coverage, calendar gaps, and corporate-action metadata. Report unresolved issues. |
| `Run the approved backtest` | Validate the agreed plan and audited data, run the experiment, and preserve its assumptions, costs, results, and trial history. |
| `Explain the performance metrics` | Interpret returns, trade statistics, costs, risk ratios, and drawdown recovery together using the chapter-14 definitions. |
| `Generate a QuantCorner report` | Create an offline HTML report with the QuantCorner logo, charts, metric explanations, provenance, and limitations. |
| `Run the synthetic demo` | Exercise the complete pipeline with generated data, without an Efin connection or claims about actual investment performance. |

Examples:

```text
$quantcorner-backtesting-efin-mcp Set up my workspace. Efin MCP is already connected.
$quantcorner-backtesting-efin-mcp Define my strategy with grill-me. Long-only Thai equities, daily bars.
$quantcorner-backtesting-efin-mcp Audit Efin data for PTT from 2023-01-01 to 2025-12-31.
$quantcorner-backtesting-efin-mcp Generate a QuantCorner report from my latest completed experiment.
```

The agent calls the existing Efin MCP directly when connected; users do not need to download provider responses manually. The terminal helpers below process the private snapshots saved by the agent. English command examples do not change the conversation language: respond in the user's preferred language.

## Terminal commands

Run from the cloned skill directory. Replace example paths with your own. Research files must stay outside the public checkout. Every script supports `--help`. Efin tool calls happen through the AI host, not a hidden downloader in these Python scripts.

| Command | Purpose and result |
|---|---|
| `python3 scripts/install.py --target codex` | Copy public skill resources into the Codex skills directory. Use `--target claude` for Claude, or `--destination /path/to/skills` for another host. Existing installation is refused; no MCP credentials/config are changed. |
| `python3 scripts/onboard.py --workspace "$HOME/quantcorner-research"` | Create private `onboarding.json`, draft `plan.json`, and workspace `.gitignore`. Preserve existing files. Local readiness does not prove Efin authentication. |
| `python3 scripts/demo.py --output "$HOME/quantcorner-demo"` | Produce synthetic `result.json`, `report.html`, and private research records. Use a fresh output folder for another demo; existing trial IDs are preserved. |
| `python3 scripts/normalize_efin.py --input /private-work/pages.json --symbol PTT --output /private-work/data.json` | Validate saved, fully paginated Efin MCP responses and normalize bars/provenance. Refuse existing output. Does not establish calendar completeness or adjusted prices. |
| `python3 scripts/research.py --data /private-work/data.json --plan /private-work/plan.json --workspace /private-work/runs --trial-id baseline-001` | Execute an agreed audited plan; save `baseline-001/plan.json`, `dataset.json`, `result.json` and append `trials.jsonl`. Reused trial IDs and previously accessed holdout windows are rejected. |
| `python3 scripts/report.py --input /private-work/runs/baseline-001/result.json --output /private-work/report.html --title "Strategy Behavior Report"` | Render the result as standalone HTML. Existing HTML at the output path is overwritten; choose a new filename to preserve earlier reports. |
| `python3 -m unittest discover -s tests -v` | Run offline deterministic tests. No licensed data or credentials are required. |

`/private-work` is a placeholder, not a required operating-system directory. Use your actual absolute workspace path. Never change audit/approval flags merely to bypass a failed gate; record the evidence and user-agreed assumptions first.

## Advanced helper

`python3 scripts/engine.py --input /private-work/bars.json --config /private-work/config.json --output /private-work/raw-result.json`

This low-level simulator expects a **bare bars array** and an **engine config object**, unlike `research.py`, which expects a dataset object (`bars` plus `provenance`) and a full plan (including `engine`). It refuses existing output. Use it for mechanic tests; empirical work uses `research.py` because the engine alone does not enforce research gates. `analytics.py` is an imported calculation module, not a CLI command.

## Reading results

Read the source/data basis and assumptions first, then compare strategy with benchmark over the same dates. Read Win Rate together with Average Win/Loss, Payoff and Expectancy. Separate filled orders from closed trades and open marks from realized P&L. Costs are already deducted. An unrecovered drawdown has unknown completed recovery/underwater duration, displayed N/A, plus its elapsed age. Report observations and remaining questions, not a binary works/does-not-work verdict.

For an update, `git pull --ff-only` updates a clean clone. The installer deliberately does not overwrite another installation; use the updated clone directly or select a new destination. Owner-managed canonical symlinks already follow canonical updates.
