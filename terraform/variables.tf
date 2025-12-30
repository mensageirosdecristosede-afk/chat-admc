# Configurações AWS
variable "aws_region" {
  description = "Região AWS para deploy dos recursos"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "chat-admc"
}

variable "environment" {
  description = "Ambiente (dev, prod)"
  type        = string
  default     = "prod"
}

# Configurações Meta
variable "meta_verify_token" {
  description = "Token de verificação do webhook do Meta"
  type        = string
  sensitive   = true
}

variable "meta_app_secret" {
  description = "App Secret do Meta para validação de assinatura"
  type        = string
  sensitive   = true
}

variable "whatsapp_phone_id" {
  description = "Phone Number ID do WhatsApp Business"
  type        = string
}

variable "instagram_account_id" {
  description = "Instagram Business Account ID"
  type        = string
}

variable "facebook_page_id" {
  description = "Facebook Page ID"
  type        = string
}

variable "meta_access_token" {
  description = "Token de acesso permanente do Meta"
  type        = string
  sensitive   = true
}

# Tags
variable "tags" {
  description = "Tags para aplicar em todos os recursos"
  type        = map(string)
  default = {
    Project     = "ChatADMC"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}
