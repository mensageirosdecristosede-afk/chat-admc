#!/usr/bin/env bash
set -euo pipefail

# Script de deploy Terraform para ENV-GCP
# Uso mínimo:
#   ./deploy_terraform.sh --project MY_PROJECT --bucket MY_BUCKET
# Para rodar sem prompt de confirmação, adicione `--auto-approve`.

PROJECT=""
BUCKET=""
AUTO_APPROVE=0
CREATE_SECRET=0

print_usage(){
  cat <<EOF
Usage: $0 --project PROJECT --bucket BUCKET [--auto-approve] [--create-secret]

--project       GCP project id
--bucket        Cloud Storage bucket name (var.bucket_name)
--auto-approve  Skip confirmation and pass --auto-approve to terraform apply
--create-secret After apply, run the create_secret_version.sh helper to add secret version
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2;;
    --bucket) BUCKET="$2"; shift 2;;
    --auto-approve) AUTO_APPROVE=1; shift;;
    --create-secret) CREATE_SECRET=1; shift;;
    -h|--help) print_usage; exit 0;;
    *) echo "Unknown arg: $1"; print_usage; exit 1;;
  esac
done

if ! command -v terraform >/dev/null 2>&1; then
  echo "terraform CLI not found. Install Terraform before running this script." >&2
  exit 2
fi
if ! command -v gcloud >/dev/null 2>&1; then
  echo "gcloud CLI not found. Install and authenticate gcloud before running." >&2
  exit 2
fi

if [ -z "$PROJECT" ]; then
  read -rp "GCP project id: " PROJECT
fi
if [ -z "$BUCKET" ]; then
  read -rp "Cloud Storage bucket name: " BUCKET
fi

echo "Using project=$PROJECT bucket=$BUCKET"

cd "$(dirname "$0")/.."

echo "Initializing Terraform..."
terraform init -input=false

echo "Running terraform plan (no changes will be applied yet)..."
terraform plan -input=false -var="project_id=$PROJECT" -var="bucket_name=$BUCKET" -out=tfplan

if [ "$AUTO_APPROVE" -eq 0 ]; then
  read -rp "Apply plan to project $PROJECT and bucket $BUCKET? (y/N) " CONF
  case "$CONF" in
    [yY]|[yY][eE][sS]) ;;
    *) echo "Aborted by user."; exit 0;;
  esac
fi

echo "Applying Terraform..."
if [ "$AUTO_APPROVE" -eq 1 ]; then
  terraform apply -input=false -auto-approve -var="project_id=$PROJECT" -var="bucket_name=$BUCKET"
else
  terraform apply -input=false tfplan
fi

echo "Terraform apply finished."

if [ "$CREATE_SECRET" -eq 1 ]; then
  echo "Running secret creation helper..."
  if [ -x ./scripts/create_secret_version.sh ]; then
    ./scripts/create_secret_version.sh --project "$PROJECT" --secret GEMINI_API_KEY --service-account chat-bot-admc@${PROJECT}.iam.gserviceaccount.com
  else
    echo "Helper script ./scripts/create_secret_version.sh not found or not executable." >&2
  fi
fi

echo "Done. Check Cloud Console or run 'gcloud secrets describe GEMINI_API_KEY --project $PROJECT' to verify." 
