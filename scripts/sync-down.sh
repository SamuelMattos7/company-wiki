#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
if [[ -f .env ]]; then
    source .env
    export AWS_PROFILE
fi
: "${BUCKET:?Set BUCKET in the environment or in .env}"

profile=()
if [[ -n "${PROFILE:-}" ]]; then
    profile=(--profile "$PROFILE")
fi
aws s3 sync "s3://$BUCKET/raw" ./raw "${profile[@]}"
aws s3 sync "s3://$BUCKET/wiki" ./wiki "${profile[@]}"
