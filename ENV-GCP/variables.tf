variable "project_id" {
  description = "ID do projeto GCP"
  type        = string
}

variable "region" {
  description = "Região GCP"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Nome do bucket Cloud Storage"
  type        = string
}

variable "gemini_secret_name" {
  description = "Nome do secret no Secret Manager para a chave Gemini"
  type        = string
  default     = "GEMINI_API_KEY"
}

variable "gemini_secret_value" {
  description = "Valor do secret (sensitive). Pode ser passado via -var ou via CI/secrets manager externo"
  type        = string
  sensitive   = true
  default     = null
}

variable "function_service_account_email" {
  description = "Email da service account usada pela Cloud Function"
  type        = string
  default     = "chat-bot-admc@appspot.gserviceaccount.com"
}
