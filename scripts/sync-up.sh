set -euo pipefail

source .env

aws s3 sync ./raw "s3://$BUCKET/raw" --profile "$PROFILE"
aws s3 sync ./wiki "s3://$BUCKET/wiki" --profile "$PROFILE"

echo "Sync up to s3://$BUCKET"