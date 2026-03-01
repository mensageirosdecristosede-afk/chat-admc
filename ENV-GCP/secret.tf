resource "google_secret_manager_secret" "gemini_api_key" {
  secret_id = var.gemini_secret_name
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "gemini_api_key_version" {
  secret      = google_secret_manager_secret.gemini_api_key.id
  secret_data = var.gemini_secret_value
  lifecycle {
    ignore_changes = ["secret_data"]
  }
}

resource "google_secret_manager_secret_iam_member" "access" {
  secret_id = google_secret_manager_secret.gemini_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.function_service_account_email}"
}
