# Command guide / คู่มือคำสั่ง

## คุยกับ Agent

เรียก `$quantcorner-backtesting-efin-mcp` แล้วบอกงานเป็นภาษาปกติ ตัวอย่างด้านล่างเป็นข้อความที่พิมพ์คุย ไม่ใช่ slash commands ที่ลงทะเบียนใหม่:

| ข้อความที่พิมพ์ต่อท้ายชื่อสกิล | Agent ทำอะไร |
|---|---|
| `ช่วยตั้งค่าครั้งแรก` | ตรวจ Python/ไฟล์ประกอบ สร้างพื้นที่ส่วนตัว ตรวจ Efin ที่เชื่อมไว้ และบอกสิ่งที่ยังขาด |
| `ถามผมแบบ grill-me ก่อนเริ่ม` | ถามทีละข้อเรื่องสมมติฐาน หุ้น ช่วงเวลา กฎซื้อขาย ต้นทุน และสิ่งที่ต้องการเรียนรู้ |
| `ช่วยตรวจข้อมูล Efin ของ PTT` | ตรวจ schema, pagination, ช่วงข้อมูล, ปฏิทิน และสถานะการปรับสิทธิ โดยยังไม่ถือว่าข้อมูลผ่านอัตโนมัติ |
| `ทำ Backtest ตามแผนที่ตกลง` | ตรวจ plan และข้อมูลก่อนรัน บันทึกทุกการทดลอง พร้อมต้นทุนและข้อจำกัด |
| `อธิบาย Ratio ตามบทที่ 14` | อ่านผลตอบแทน ความถี่/ขนาดกำไรขาดทุน ต้นทุน และ Drawdown ร่วมกัน |
| `สร้างรายงาน QuantCorner` | สร้าง HTML ออฟไลน์พร้อมโลโก้ กราฟ ตาราง และหลักฐานของรอบทดสอบ |
| `ลองตัวอย่างโดยไม่ต่อ Efin` | รันข้อมูลสังเคราะห์เพื่อทดลองระบบ ไม่ใช่ผลลงทุนจริง |

## Terminal commands

Run from the cloned skill directory. Replace example paths with your own. Research files must stay outside the public checkout. Every script supports `--help`. Efin tool calls happen through the AI host, not a hidden downloader in these Python scripts.

| Command | Purpose and result |
|---|---|
| `python3 scripts/install.py --target codex` | Copy public skill resources into the Codex skills directory. Use `--target claude` for Claude, or `--destination /path/to/skills` for another host. Existing installation is refused; no MCP credentials/config are changed. |
| `python3 scripts/onboard.py --workspace "$HOME/quantcorner-research"` | Create private `onboarding.json`, draft `plan.json`, and workspace `.gitignore`. Preserve existing files. Local readiness does not prove Efin authentication. |
| `python3 scripts/demo.py --output "$HOME/quantcorner-demo"` | Produce synthetic `result.json`, `report.html`, and private research records. Use a fresh output folder for another demo; existing trial IDs are preserved. |
| `python3 scripts/normalize_efin.py --input /private-work/pages.json --symbol PTT --output /private-work/data.json` | Validate saved, fully paginated Efin MCP responses and normalize bars/provenance. Refuse existing output. Does not establish calendar completeness or adjusted prices. |
| `python3 scripts/research.py --data /private-work/data.json --plan /private-work/plan.json --workspace /private-work/runs --trial-id baseline-001` | Execute an agreed audited plan; save `baseline-001/plan.json`, `dataset.json`, `result.json` and append `trials.jsonl`. Reused trial IDs and previously accessed holdout windows are rejected. |
| `python3 scripts/report.py --input /private-work/runs/baseline-001/result.json --output /private-work/report.html --title "พฤติกรรมกลยุทธ์"` | Render the result as standalone HTML. Existing HTML at the output path is overwritten; choose a new filename to preserve earlier reports. |
| `python3 -m unittest discover -s tests -v` | Run offline deterministic tests. No licensed data or credentials are required. |

`/private-work` is a placeholder, not a required operating-system directory. Use your actual absolute workspace path. Never change audit/approval flags merely to bypass a failed gate; record the evidence and user-agreed assumptions first.

## Advanced helper

`python3 scripts/engine.py --input /private-work/bars.json --config /private-work/config.json --output /private-work/raw-result.json`

This low-level simulator expects a **bare bars array** and an **engine config object**, unlike `research.py`, which expects a dataset object (`bars` plus `provenance`) and a full plan (including `engine`). It refuses existing output. Use it for mechanic tests; empirical work uses `research.py` because the engine alone does not enforce research gates. `analytics.py` is an imported calculation module, not a CLI command.

## Reading results

Read the source/data basis and assumptions first, then compare strategy with benchmark over the same dates. Read Win Rate together with Average Win/Loss, Payoff and Expectancy. Separate filled orders from closed trades and open marks from realized P&L. Costs are already deducted. An unrecovered drawdown has unknown completed recovery/underwater duration, displayed N/A, plus its elapsed age. Report observations and remaining questions, not a binary works/does-not-work verdict.

For an update, `git pull --ff-only` updates a clean clone. The installer deliberately does not overwrite another installation; use the updated clone directly or select a new destination. Owner-managed canonical symlinks already follow canonical updates.
