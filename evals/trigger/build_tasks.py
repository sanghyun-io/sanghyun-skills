"""Generate Harbor task folders from cases.json.

usage: python build_tasks.py <out_dir>
Each case becomes <out_dir>/<id>/ with task.toml, instruction.md, environment/ (Dockerfile + fixture app)
and a no-op tests/test.sh. Scoring happens afterwards from trajectories (score.py), so verification
is disabled at run time.
"""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

DOCKERFILE = """FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl git python3 && rm -rf /var/lib/apt/lists/*
# Bake Claude Code into the image: Harbor skips its per-trial install when `claude --version` works,
# and parallel per-trial installs hit the 360 s agent-setup timeout. Identical layers are cached across tasks.
RUN curl -fsSL https://downloads.claude.ai/claude-code-releases/bootstrap.sh | bash -s -- && /root/.local/bin/claude --version
COPY app/ /app/
WORKDIR /app
"""

TASK_TOML = """schema_version = "1.1"

[task]
name = "sanghyun-skills/trigger-{id}"
description = "Trigger eval: expect {expect}"

[metadata]
category = "skill-trigger"
expect = "{expect}"

[verifier]
timeout_sec = 60.0

[agent]
timeout_sec = 600.0

[environment]
build_timeout_sec = 600.0
cpus = 1
memory_mb = 2048
storage_mb = 4096
"""

TEST_SH = "#!/bin/bash\necho 0 > /logs/verifier/reward.txt\n"


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))  # LF only: CRLF breaks shebangs in Linux containers


def main(out: str) -> int:
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]
    root = Path(out)
    if root.exists():
        shutil.rmtree(root)
    for c in cases:
        d = root / c["id"]
        write(d / "task.toml", TASK_TOML.format(id=c["id"], expect=c["expect"] or "none"))
        write(d / "instruction.md", c["prompt"] + "\n")
        write(d / "environment" / "Dockerfile", DOCKERFILE)
        shutil.copytree(HERE / "fixture" / "app", d / "environment" / "app")
        write(d / "tests" / "test.sh", TEST_SH)
        (d / "tests" / "test.sh").chmod(0o755)
    print(f"wrote {len(cases)} tasks to {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]) if len(sys.argv) == 2 else print(__doc__) or 2)
