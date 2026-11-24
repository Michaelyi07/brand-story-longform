#!/usr/bin/env python3
"""Per-gate machine verification for the brand-story deliverable (#2291).

Runs the four promised gates against the actual deliverable files and writes
verification_log.md with verbatim status=PASS/FAIL lines. Real checks only -
no hardcoded results.

Gates:
  G1 word count    : 700 <= CJK chars (master Chinese story) <= 900
  G2 section count : exactly 3 sections Problem / Solution / Vision (zh + en)
  G3 banned list   : exaggeration words -> 0 hits (story + docx text)
  G4 fictional     : character-table fictional flags all true; no client/
                     platform-internal identifiers anywhere
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent
MD = ROOT / "brand_story.md"
DOCX = ROOT / "brand_story.docx"

text = MD.read_text(encoding="utf-8")

# ---- section extraction -------------------------------------------------
zh = text.split("## 品牌故事", 1)[1].split("## 英文版本", 1)[0]
en = text.split("## 英文版本", 1)[1].split("## 虚构角色与场景表", 1)[0]

# ---- G1 word count ------------------------------------------------------
def cjk_count(s: str) -> str:
    chars = [c for c in s if "\u4e00" <= c <= "\u9fff" or c in "，。：；！？「」『』（）、——…"]
    return len(chars)

zh_chars = cjk_count(zh)
en_words = len(re.findall(r"[A-Za-z]+(?:'[a-z]+)?", en))

# ---- G2 sections --------------------------------------------------------
def sections(s: str) -> list[str]:
    return [h.strip() for h in re.findall(r"^### (.+)$", s, re.M)]

zh_heads = sections(zh)
en_heads = sections(en)

def head_ok(heads: list[str]) -> bool:
    joined = " ".join(heads)
    return (len(heads) == 3
            and "Problem" in joined and "Solution" in joined and "Vision" in joined)

# ---- G3 banned list -----------------------------------------------------
BANNED_ZH = ["最好", "第一", "最强", "保证", "绝对", "翻倍", "行业领先", "遥遥领先"]
BANNED_EN = ["best", "#1", "guarantee", "amazing", "world-class", "revolutionary"]

def banned_hits(s: str) -> list[str]:
    hits = []
    low = s.lower()
    for w in BANNED_ZH:
        if w in s:
            hits.append(w)
    for w in BANNED_EN:
        if re.search(r"(?<![a-z])" + re.escape(w).lower() + r"(?![a-z])", low):
            hits.append(w)
    return hits

story_hits = banned_hits(zh + en)

# docx text (if built yet)
docx_text = ""
if DOCX.exists():
    with zipfile.ZipFile(DOCX) as z:
        docx_text = z.read("word/document.xml").decode("utf-8", "replace")
    # strip tags
    docx_text = re.sub(r"<[^>]+>", "", docx_text)
docx_hits = banned_hits(docx_text) if docx_text else []

# ---- G4 fictional / no internal identifiers -----------------------------
table = text.split("## 虚构角色与场景表", 1)[1]
flags = re.findall(r"\| true \||\| false \|", table)
all_true = ("| false |" not in flags) and len(flags) >= 5

INTERNAL = ["bobo", "clawhunt", "daoye-data-agent", "S1-BRAND", "2291"]
internal_hits = [w for w in INTERNAL if w.lower() in text.lower()]
if docx_text:
    internal_hits += [w for w in INTERNAL if w.lower() in docx_text.lower()]

# ---- scenario labels ----------------------------------------------------
labels_zh = zh.count("（虚构场景）")
labels_en = en.count("(Fictional scenario)")

# ---- write log ----------------------------------------------------------
lines = []
add = lines.append
add("# Verification Log — brand story gates")
add("")
add("Every line below is produced by `verify_gates.py` running against the")
add("actual deliverable files (brand_story.md / brand_story.docx). No")
add("hand-written results.")
add("")
add(f"- G1 word count: master Chinese story = {zh_chars} chars (companion English = {en_words} words) "
    f"-> status={'PASS' if 700 <= zh_chars <= 900 else 'FAIL'}")
add(f"  assert: 700 <= zh_chars <= 900 (the brief's unit is 「约 800 字」)")
add(f"- G2 section count: zh headings = {zh_heads}; en headings = {en_heads} "
    f"-> status={'PASS' if head_ok(zh_heads) and head_ok(en_heads) else 'FAIL'}")
add(f"- G3 banned list (zh: {'/'.join(BANNED_ZH)}; en: {'/'.join(BANNED_EN)}): "
    f"story hits = {story_hits or 0}, docx hits = {docx_hits or 0} "
    f"-> status={'PASS' if not story_hits and not docx_hits else 'FAIL'}")
add(f"- G4 fictional: character-table flags true = {len(flags)}, false flags = {len(flags) - sum(1 for f in flags if 'true' in f)} "
    f"-> status={'PASS' if all_true else 'FAIL'}")
add(f"- G4b internal identifiers (client/platform names): hits = {internal_hits or 0} "
    f"-> status={'PASS' if not internal_hits else 'FAIL'}")
add(f"- G5 fictional-scenario labels: zh = {labels_zh}, en = {labels_en} "
    f"-> status={'PASS' if labels_zh >= 1 and labels_en >= 1 else 'FAIL'}")
add("")
add("Gate summary: " + ("ALL PASS" if (
    700 <= zh_chars <= 900 and head_ok(zh_heads) and head_ok(en_heads)
    and not story_hits and not docx_hits and all_true and not internal_hits
    and labels_zh >= 1 and labels_en >= 1) else "FAILURES PRESENT"))

print("\n".join(lines))
(ROOT / "verification_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
sys.exit(0 if "ALL PASS" in lines[-1] else 1)
