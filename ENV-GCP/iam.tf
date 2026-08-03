// IAM bindings required for Cloud Function service account to operate
resource "google_project_iam_member" "fn_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${var.function_service_account_email}"
}

resource "google_project_iam_member" "fn_datastore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${var.function_service_account_email}"
}

resource "google_project_iam_member" "fn_storage_object_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${var.function_service_account_email}"
}
