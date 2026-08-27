from pathlib import Path
import os, subprocess, tarfile, shutil, sys

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / ".release"
STATE = RELEASE / "state.txt"
ENC = RELEASE / "encrypted"
TOTAL = 60

key = os.environ.get("RELEASE_KEY", "")
if not key:
    raise SystemExit("RELEASE_KEY secret is missing")

current = int(STATE.read_text(encoding="utf-8").strip() or "0")
next_step = current + 1
if next_step > TOTAL:
    print("All 60 releases are already published.")
    sys.exit(0)

enc_file = ENC / f"step_{next_step:03d}.enc"
if not enc_file.exists():
    raise SystemExit(f"Missing encrypted payload: {enc_file.name}")

tmp = Path("/tmp/projedanisman_release")
if tmp.exists(): shutil.rmtree(tmp)
tmp.mkdir(parents=True)
tar_path = tmp / "payload.tar.gz"
subprocess.run([
    "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
    "-in", str(enc_file), "-out", str(tar_path), "-pass", f"pass:{key}"
], check=True)

extract = tmp / "extract"; extract.mkdir()
with tarfile.open(tar_path, "r:gz") as tf:
    tf.extractall(extract)

message = (extract / ".release_message").read_text(encoding="utf-8").strip()
(extract / ".release_message").unlink()

for src in sorted(extract.rglob("*")):
    if src.is_file():
        rel = src.relative_to(extract)
        dst = ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

STATE.write_text(f"{next_step}\n", encoding="utf-8")

# Final release cleans the scheduler/encrypted staging material from the public tree.
if next_step == TOTAL:
    shutil.rmtree(ENC, ignore_errors=True)
    workflow = ROOT / ".github" / "workflows" / "publish-next.yml"
    if workflow.exists(): workflow.unlink()
    # Remove release state and this helper after the final payload is applied.
    try: STATE.unlink()
    except FileNotFoundError: pass
    try: Path(__file__).unlink()
    except FileNotFoundError: pass

out = os.environ.get("GITHUB_OUTPUT")
if out:
    with open(out, "a", encoding="utf-8") as f:
        f.write(f"message={message}\n")
        f.write(f"step={next_step}\n")
else:
    print(message)
