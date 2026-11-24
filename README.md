# Extended Brand Story (800-character master, Chinese) — Member Space Platform

Deliverable for ticket S1-BRAND-008: an ~800-character extended brand story
(Chinese master + companion English version) telling why a membership space
serving ~100 member companies upgrades from venue operator to industry
resource connection platform.

## Files

| File | What it is |
|---|---|
| `brand_story.md` | Markdown master: Chinese story (three sections 问题·Problem / 方案·Solution / 愿景·Vision, six-beat budget), companion English version, fictional character-and-scenario table, per-beat count audit |
| `brand_story.docx` | Word version generated from the same Markdown (`docx-formal-report` pipeline: build → precheck → output QA, all PASS) |
| `verification_log.md` | Machine-generated gate log (real checks, verbatim output) |
| `verify_gates.py` | The gate script itself; re-runnable |

## Structure (six-beat budget, sum ≈ 800 characters)

opening scene ~120 / conflict tension ~160 / insight ~120 / turning point ~160 / mechanism-promise ~140 / vision invitation ~100. The three required sections map onto the beats: Problem = beats 1-3, Solution = beats 4-5, Vision = beat 6. Two fictional scenarios are included and explicitly labeled （虚构场景）/ (Fictional scenario).

## Gates (all PASS; see verification_log.md)

- G1 word count: master Chinese story 700-900 chars required (the brief's unit is 「约 800 字」 — the gate scope is the Chinese story section only, not the bilingual document total); the authoritative number is whatever `verification_log.md` records from the last script run. The companion English version is a faithful translation, not an independent 700-900-word deliverable.
- G2 sections: exactly 3 headings containing Problem / Solution / Vision, checked in both the Markdown and the docx
- G3 banned-list scan (最好/第一/最强/保证/绝对/翻倍/行业领先/遥遥领先 + best/#1/guarantee/amazing/world-class/revolutionary): 0 hits in md and docx
- G4 fictional: character-table flags all true; no client name in any file
- G5 fictional-scenario labels present in both languages

Re-run the gates:

```
python verify_gates.py
```

Requires only Python 3.11+ standard library. Regenerating the Word file:
`brand_story.docx` is produced from `brand_story.md` by the build script;
the Markdown file is the single source (edit md, rebuild docx).
