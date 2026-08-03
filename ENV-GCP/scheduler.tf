resource "google_cloud_scheduler_job" "weekly_report" {
  name        = "sara-weekly-report"
  description = "Envia relatório semanal da SARA todo sábado"
  # Executa todo sábado às 09:00 (horário de Brasília)
  schedule  = "0 9 * * SAT"
  time_zone = "America/Sao_Paulo"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.main.https_trigger_url
    headers = {
      "Content-Type" = "application/json"
    }
    # Corpo opcional; a função pode inspecionar o payload para diferenciar chamadas
    body = base64encode(jsonencode({ action = "send_weekly_report" }))
  }
}
