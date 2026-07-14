set -euo pipefail

source .env

aws s3 sync "s3://$BUCKET/raw" ./raw --profile "$PROFILE"
aws s3 sync "s3://$BUCKET/wiki" ./wiki --profile "$PROFILE"

echo "Sync down from s3://$BUCKET"