resource "google_cloudfunctions_function" "main" {
  name        = "chat-admc-handler"
  description = "Função principal do chat ADMC"
  runtime     = "python311"
  entry_point = "main"
  region      = var.region

  source_archive_bucket = google_storage_bucket.main.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  trigger_http = true
  available_memory_mb   = 256
  timeout              = 60
  environment_variables = {
    BUCKET_NAME = var.bucket_name
  }
  service_account_email = "chat-bot-admc@appspot.gserviceaccount.com"
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.main.name
  source = "./function-source.zip"
}
