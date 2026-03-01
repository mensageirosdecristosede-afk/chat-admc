resource "google_storage_bucket" "main" {
  name     = var.bucket_name
  location = var.region
  force_destroy = true
  uniform_bucket_level_access = trueterraform apply --auto-approve
}
