#!/usr/bin/env bash
set -euo pipefail

# Script seguro para adicionar uma versão do secret GEMINI_API_KEY ao Secret Manager
# Uso:
#   SECRET_VALUE=... ./create_secret_version.sh --project MY_PROJECT --secret GEMINI_API_KEY --service-account SERVICE_ACCOUNT_EMAIL
# Ou execute sem SECRET_VALUE e ele pedirá o valor interativamente (entrada oculta).

PROJECT=""
SECRET_NAME="GEMINI_API_KEY"
SERVICE_ACCOUNT_EMAIL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2;;
    --secret) SECRET_NAME="$2"; shift 2;;
    --service-account) SERVICE_ACCOUNT_EMAIL="$2"; shift 2;;
    -h|--help) echo "Usage: $0 --project PROJECT [--secret NAME] [--service-account EMAIL]"; exit 0;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

if ! command -v gcloud >/dev/null 2>&1; then
  echo "gcloud CLI is required. Install and authenticate before running this script." >&2
  exit 2
fi

if [ -z "$PROJECT" ]; then
  echo "--project is required" >&2
  exit 2
fi

echo "Using project: $PROJECT"
echo "Secret name: $SECRET_NAME"

# Get secret value from env or ask interactively
if [ -z "${SECRET_VALUE:-}" ]; then
  echo -n "Enter the GEMINI secret value (input hidden): "
  read -s SECRET_VALUE
  echo
fi

if [ -z "$SECRET_VALUE" ]; then
  echo "Secret value is empty; aborting." >&2
  exit 3
fi

echo "Ensuring secret resource exists (will create if missing)..."
if ! gcloud secrets describe "$SECRET_NAME" --project "$PROJECT" >/dev/null 2>&1; then
  gcloud secrets create "$SECRET_NAME" --replication-policy="automatic" --project "$PROJECT"
  echo "Created secret resource $SECRET_NAME"
else
  echo "Secret resource $SECRET_NAME already exists"
fi

echo "Adding secret version..."
printf '%s' "$SECRET_VALUE" | gcloud secrets versions add "$SECRET_NAME" --data-file=- --project "$PROJECT"
echo "Secret version added."

if [ -n "$SERVICE_ACCOUNT_EMAIL" ]; then
  echo "Granting access to service account: $SERVICE_ACCOUNT_EMAIL"
  gcloud secrets add-iam-policy-binding "$SECRET_NAME" \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/secretmanager.secretAccessor" \
    --project "$PROJECT"
  echo "IAM binding added."
fi

echo "Done. For safety, unset SECRET_VALUE variable if you exported it: unset SECRET_VALUE"
