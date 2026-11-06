#!/bin/bash
set -euo pipefail

# Vercel's Python is externally managed. Keep build dependencies isolated;
# never bypass its protection or bundle this temporary environment.
BUILD_ENV="$(mktemp -d /tmp/studyhub-build.XXXXXX)"
python3 -m venv "$BUILD_ENV"
"$BUILD_ENV/bin/python" -m pip install -r requirements.txt
"$BUILD_ENV/bin/python" manage.py collectstatic --noinput --clear

# Schema migrations are an explicit operational step, never a page-build side effect.
