"""Build only the explicitly authorised PPO teaching files, never the whole repo.

This maintainer utility stays outside the student package. Hashes verify that
the exported original PPO modules and U6 were copied without implementation edits.
"""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "ppo_teaching_handoff_20260924"
SOURCE = ROOT / "ppo_stagec_physx_teammate_training_cp38_20260724"
ORIGINAL = [
    "ppo_framework/actions.py", "ppo_framework/policy.py", "ppo_framework/rollout.py",
    "ppo_framework/state_reward.py", "ppo_framework/v2/action_space.py",
    "ppo_framework/v2/config.py", "ppo_framework/v2/diagnostics.py",
    "ppo_framework/v2/policy.py", "ppo_framework/v2/set_policy.py",
    "ppo_framework/v2/stage_c_trainer.py", "ppo_framework/v2/state_encoder.py",
    "ppo_framework/v2/trainer.py", "ppo_framework/v2/trajectory.py",
    "checkpoints/u6_server_synced_latest.pt",
    "tacticslib/strategy_library.py", "tacticslib/base_library.py", "tacticslib/data/data.json",
]
NEW = [
    "README.md", "requirements.txt", "verify_package.py", "VALIDATION.md",
    "ppo_framework/__init__.py", "ppo_framework/v2/__init__.py",
    "teaching/__init__.py", "teaching/collector.py", "teaching/toy_env.py", "teaching/train.py",
    "tests/__init__.py", "tests/test_training.py",
    "docs/01_training_chain.md", "docs/02_code_guide.md", "docs/03_run_and_adapter.md",
    "docs/04_lesson_plan.md", "docs/05_scope_and_provenance.md",
    "docs/06_reference_tactics.md", "teaching/reference_shot.py", "tests/test_reference_shot.py",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records = []
    for name in ORIGINAL + NEW:
        path = DEST / name
        digest = sha(path)
        if name in ORIGINAL and digest != sha(SOURCE / name):
            raise ValueError(f"Original core modified: {name}")
        records.append({"path": name, "sha256": digest, "bytes": path.stat().st_size,
                        "source": f"{SOURCE.name}/{name}" if name in ORIGINAL else "new_teaching_material",
                        "unchanged_copy": name in ORIGINAL})
    manifest = {"package": DEST.name, "schema": 1, "files": records,
                "excluded": ["search algorithms", "private physics runtime",
                             "deployment clients", "historical match logs", "training outputs"]}
    (DEST / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    archive = ROOT / f"{DEST.name}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ORIGINAL + NEW + ["SOURCE_MANIFEST.json"]:
            z.write(DEST / name, f"{DEST.name}/{name}")
    print(json.dumps({"zip": str(archive), "bytes": archive.stat().st_size,
                      "sha256": sha(archive), "files": len(records) + 1}, ensure_ascii=False))


if __name__ == "__main__":
    main()
