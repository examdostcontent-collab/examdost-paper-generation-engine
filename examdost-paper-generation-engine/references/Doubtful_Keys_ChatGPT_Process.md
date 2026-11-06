# Doubtful keys: second opinion from ChatGPT's strongest model (STANDING PROCESS)

Applies to EVERY job that derives or checks answer keys (GATE, ESE, SSC JE, RRB JE, UPSSSC, crash/PYQ books, test series). Use it whenever a key is not confidently settled: any `UNSURE` log line, any blind-solver or proofreader disagreement, any difference from a printed/publisher key, any question where two options are defensible, any `*` key, any current-affairs or recall fact keyed from memory.

## Rule
Never ship a doubtful key on Claude's judgement alone. Ask ChatGPT's strongest available model (the Max/Pro-tier model of the user's plan, selected in the model picker; the user calls it the "Astra max plan" model) the question blind, compare, and decide by the rules below. Record the result.

## Steps
1. **Collect** the doubtful list per paper: `UNSURE` lines in `out/log_*.txt`, `PROOF_*.md` notes that mention a disagreement, `ADJ_KEYS.md` rows, blind-solver differences (`cmp_blind.py`), printed-key differences (`cmp_printed.py`), review flags. Each item = question number, our key, rival option(s).
2. **Ask ChatGPT blind** with `scripts/chatgpt_key_check.py` (uses the logged-in ChatGPT profile via Playwright; same engine as the diagram redraw scripts). It sends ONLY the question text + options (+ figure image if any), never our key, with the instruction: "Solve independently. Think step by step, verify numerically. Give the final answer as `ANSWER: (n)` and a confidence HIGH/MED/LOW. If the printed data are flawed, say which option is nearest." The model picker is set to the strongest model before sending; the script logs which model label it actually used. If the Max model is unavailable (quota or picker not found) the item is marked `NOT CHECKED`, never silently answered by a weaker model.
3. **Compare** (`out/chatgpt_check.json` per paper):
   - ChatGPT-max agrees with our key -> keep, mark `confirmed by ChatGPT-max` in the notes workbook.
   - Disagrees -> show ChatGPT's reasoning to a Claude agent which must re-derive fully (numericals from scratch, facts via WebSearch where possible), then decide. Change the key only when the re-derivation supports ChatGPT with a concrete reason; otherwise keep ours and list the question under "Doubtful - human check" with both reasonings.
   - Both models LOW or the question is flawed -> key the nearest option, state the flaw plainly in the solution, flag for human check.
   - Facts/current affairs: ChatGPT answers are not accepted without an independent source (WebSearch/official page); an agreement of two unsourced answers is still `Facts to verify`.
4. **Update** the part file (key + header + final `Hence the correct option is (n).` + solution wording), lint, rebuild, Mode-7.
5. **Record** in `Final\Supporting\*_Answer_Key_Notes.xlsx` (sheet `Key changes` / `Doubtful - human check` gets a column `ChatGPT-max`) and the Review_Flags file.

## Gotchas
- Blind means blind: never include our key, the printed key or the publisher explanation in the prompt (it anchors the model).
- One question per fresh chat; paste LaTeX as plain text. Large numericals: ask for the final number and which option it is nearest to.
- ChatGPT-max can also be wrong on current affairs and on flawed printed questions; it is a second opinion, not the authority.
- Respect ChatGPT quota messages (`check_for_quota_message`): stop and report, do not loop.
- Credentials are the user's logged-in profile only; never type passwords.
