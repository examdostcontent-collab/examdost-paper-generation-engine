"""Second opinion on doubtful answer keys from ChatGPT's strongest model (see references/Doubtful_Keys_ChatGPT_Process.md).

usage: python chatgpt_key_check.py <items.json> <out.json> [--profile DIR] [--model-labels "Pro,Max,Astra"] [--list-models]

items.json = [{"id": "ese26p1_q60", "text": "<question + (a)..(d) options as plain text>", "image": "optional png path"}]
Never include our key or any explanation in text (blind check). out.json receives, per id:
{"answer": "a-d|NONE|?", "confidence": "HIGH|MED|LOW|?", "model_used": "<label shown in the picker>", "raw": "<reply text>"}.
If the strongest model cannot be selected the item is written with answer "NOT CHECKED" (never answered by a weaker model)."""
import sys, json, re, time, argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
import chatgpt_diagram_pipeline as pipe

PROMPT = ("Solve this exam question independently, as a careful subject expert. Think step by step and verify numerically "
          "where there is a calculation. If the printed data are flawed, say so and name the nearest option. "
          "End your reply with exactly two lines:\nANSWER: (x)   where x is a, b, c or d (or NONE)\nCONFIDENCE: HIGH, MED or LOW\n\n")


def open_picker(page):
    for sel in ('[data-testid="model-switcher-dropdown-button"]', 'button[aria-label*="Model"]', 'button:has-text("ChatGPT")'):
        loc = page.locator(sel).first
        if loc.count():
            loc.click()
            page.wait_for_timeout(800)
            return True
    return False


def pick_model(page, labels, list_only=False):
    """Click the first menu entry whose text contains one of the labels (in the given priority order)."""
    if not open_picker(page):
        return None, []
    items = page.locator('[role="menuitem"], [role="option"], [data-testid^="model-switcher-"]')
    texts = [t.strip().replace("\n", " ") for t in items.all_inner_texts()]
    if list_only:
        page.keyboard.press("Escape")
        return None, texts
    for lab in labels:
        for i, t in enumerate(texts):
            if lab.lower() in t.lower():
                items.nth(i).click()
                page.wait_for_timeout(1000)
                return t, texts
    page.keyboard.press("Escape")
    return None, texts


def wait_reply(page, timeout_s=900):
    t0 = time.time()
    time.sleep(5)
    while time.time() - t0 < timeout_s:
        busy = page.locator('[data-testid="stop-button"]').count() > 0
        if not busy:
            time.sleep(3)
            if page.locator('[data-testid="stop-button"]').count() == 0:
                break
        time.sleep(3)
    msgs = page.locator('[data-message-author-role="assistant"]')
    return msgs.last.inner_text() if msgs.count() else ""


def parse(reply):
    a = re.findall(r"ANSWER:\s*\(?([a-dA-D]|NONE)\)?", reply)
    c = re.findall(r"CONFIDENCE:\s*(HIGH|MED|LOW)", reply, re.I)
    return (a[-1].lower() if a else "?"), (c[-1].upper() if c else "?")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items"); ap.add_argument("out")
    ap.add_argument("--profile", default=r"C:/Users/rahul/.chatgpt_profile")
    ap.add_argument("--model-labels", default="Pro,Max,Astra")
    ap.add_argument("--list-models", action="store_true")
    a = ap.parse_args()
    labels = [x.strip() for x in a.model_labels.split(",") if x.strip()]
    items = json.load(open(a.items, encoding="utf8")) if not a.list_models else []
    out = json.load(open(a.out, encoding="utf8")) if Path(a.out).exists() else {}
    with sync_playwright() as p:
        ctx = pipe.launch_context(p, a.profile)
        page = ctx.new_page()
        page.goto("https://chatgpt.com/", wait_until="domcontentloaded", timeout=60000)
        page.locator(pipe.SEL_COMPOSER).wait_for(state="visible", timeout=120000)
        if a.list_models:
            _, texts = pick_model(page, labels, list_only=True)
            print("MODEL PICKER OPTIONS:", texts)
            ctx.close()
            return
        for it in items:
            if it["id"] in out and out[it["id"]].get("answer") not in (None, "NOT CHECKED"):
                continue
            page.goto("https://chatgpt.com/", wait_until="domcontentloaded", timeout=60000)
            page.locator(pipe.SEL_COMPOSER).wait_for(state="visible", timeout=120000)
            used, texts = pick_model(page, labels)
            if not used:
                out[it["id"]] = {"answer": "NOT CHECKED", "confidence": "?", "model_used": "", "raw": "strongest model not selectable; picker=" + str(texts)}
                print(it["id"], "NOT CHECKED (model)")
                continue
            try:
                if it.get("image"):
                    page.locator('input[type="file"]').first.set_input_files(it["image"])
                    page.wait_for_timeout(2500)
                pipe.send_prompt(page, page.locator(pipe.SEL_COMPOSER), PROMPT + it["text"])
                reply = wait_reply(page)
                if pipe.check_for_quota_message(page):
                    print("QUOTA message: stopping"); break
                ans, conf = parse(reply)
                out[it["id"]] = {"answer": ans, "confidence": conf, "model_used": used, "raw": reply}
                print(it["id"], ans, conf, used)
            except Exception as e:
                out[it["id"]] = {"answer": "NOT CHECKED", "confidence": "?", "model_used": used, "raw": f"{type(e).__name__}: {e}"}
                print(it["id"], "FAILED", e)
            json.dump(out, open(a.out, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        ctx.close()
    json.dump(out, open(a.out, "w", encoding="utf8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
