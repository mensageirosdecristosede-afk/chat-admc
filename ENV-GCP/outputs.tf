output "bucket_name" {
  value = google_storage_bucket.main.name
}

output "function_url" {
  value = google_cloudfunctions_function.main.https_trigger_url
}
