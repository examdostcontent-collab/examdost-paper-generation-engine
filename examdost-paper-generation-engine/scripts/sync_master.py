# -*- coding: utf-8 -*-
"""sync_master.py -- refresh the chapter/topic taxonomy from the live Google Sheet.

The canonical taxonomy lives in a Google Sheet ("Type List Master Sheet"). This script
downloads its .xlsx export and installs it as assets/chapter_topic_master.xlsx for every
ExamDost skill that uses it -- so the offline master is just a cache of the live sheet.

Run it at the START of any paper-generator / question-metadata / exam-psychometrician job
(SKILL.md Phase 1). It is safe to run every time: if the sheet is unchanged it is a no-op.

Prereq: the sheet must be shared "Anyone with the link -> Viewer" (view-only). Editing access
is NOT needed or wanted. If it is still private the export returns 401/HTML and this script
fails loudly (exit 2) so the caller can fall back to the cached copy.

Usage:
    python sync_master.py                 # download, verify, install to all targets
    python sync_master.py --dry-run       # download + verify only; do not write
    python sync_master.py --config <path> # use a different master_source.json

Exit codes: 0 = synced (or already current) | 2 = download/verify failed (use cache).
"""
from __future__ import annotations
import argparse, hashlib, io, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def expand(p):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(p)))


def load_cfg(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def download(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ExamDost master sync)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def subjects_of(path):
    """Parse an xlsx master and return its ordered list of subject (sheet) names."""
    import load_taxonomy as lt
    return list(lt.parse(path)["subjects"].keys())


def prune_backups(target, keep):
    d, base = os.path.dirname(target), os.path.basename(target)
    stem = base[:-5] if base.endswith(".xlsx") else base
    baks = sorted((f for f in os.listdir(d) if f.startswith(stem + ".PREV-") and f.endswith(".xlsx")),
                  reverse=True)
    for old in baks[keep:]:
        try:
            os.remove(os.path.join(d, old))
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(HERE, "..", "assets", "master_source.json"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    url = cfg["export_url"]
    log = (lambda *a: None) if args.quiet else (lambda *a: print(*a))

    # ---- 1. download ----
    try:
        data, ct = download(url)
    except Exception as e:
        print(f"SYNC FAILED: could not reach the sheet ({type(e).__name__}: {e}).")
        print("  -> If this is a 401/403, share the sheet as 'Anyone with the link -> Viewer'.")
        print("  -> Falling back to the cached local master is the caller's call.")
        return 2

    if data[:2] != b"PK":   # xlsx is a zip; HTML sign-in page is not
        print("SYNC FAILED: the export was not an .xlsx file (got "
              f"{ct or 'unknown'} - the sheet is probably still PRIVATE).")
        print("  -> Open the sheet > Share > General access > 'Anyone with the link' = Viewer.")
        return 2

    # ---- 2. write to a temp file & verify it parses ----
    tmp = os.path.join(HERE, ".master_sync_tmp.xlsx")
    with open(tmp, "wb") as f:
        f.write(data)
    try:
        subs = subjects_of(tmp)
    except Exception as e:
        os.remove(tmp)
        print(f"SYNC FAILED: downloaded file did not parse as a taxonomy ({type(e).__name__}: {e}).")
        return 2

    # ---- 3. sanity checks ----
    problems = []
    if len(subs) < cfg.get("min_subjects", 1):
        problems.append(f"only {len(subs)} subjects (< {cfg['min_subjects']})")
    for s in cfg.get("must_have_subjects", []):
        if s not in subs:
            problems.append(f"missing expected subject '{s}'")
    for s in cfg.get("must_not_have_subjects", []):
        if s in subs:
            problems.append(f"retired subject '{s}' is back in the sheet")
    if problems:
        os.remove(tmp)
        print("SYNC ABORTED: the downloaded sheet failed sanity checks:")
        for p in problems:
            print("   -", p)
        print("  -> Local master left untouched. Check the Google Sheet's tabs.")
        return 2

    new_hash = hashlib.sha256(data).hexdigest()
    log(f"Downloaded OK: {len(data):,} bytes, {len(subs)} subjects.")

    # ---- 4. diff vs the current primary target (show taxonomy changes) ----
    targets = [expand(t) for t in cfg["targets"]]
    primary = targets[0]
    if os.path.exists(primary):
        try:
            old_subs = subjects_of(primary)
            added = [s for s in subs if s not in old_subs]
            removed = [s for s in old_subs if s not in subs]
            if added:
                log("  + subjects added:   " + ", ".join(added))
            if removed:
                log("  - subjects removed: " + ", ".join(removed))
            if not added and not removed:
                log("  (subject list unchanged)")
        except Exception:
            pass

    if args.dry_run:
        os.remove(tmp)
        log("DRY RUN: verified, nothing written.")
        return 0

    # ---- 5. install to every target (backup only when content changed) ----
    keep = cfg.get("keep_backups", 3)
    ts = int(time.time())
    wrote, skipped, missing_dir = 0, 0, 0
    for tgt in targets:
        d = os.path.dirname(tgt)
        if not os.path.isdir(d):
            log(f"  ! skip (no dir): {tgt}")
            missing_dir += 1
            continue
        if os.path.exists(tgt):
            cur = hashlib.sha256(open(tgt, "rb").read()).hexdigest()
            if cur == new_hash:
                skipped += 1
                log(f"  = already current: {tgt}")
                continue
            bak = f"{tgt[:-5]}.PREV-{ts}.xlsx"
            os.replace(tgt, bak)
        with open(tgt, "wb") as f:
            f.write(data)
        prune_backups(tgt, keep)
        wrote += 1
        log(f"  -> installed: {tgt}")

    os.remove(tmp)
    log(f"SYNC OK: {wrote} updated, {skipped} already current"
        + (f", {missing_dir} target dir(s) missing" if missing_dir else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
