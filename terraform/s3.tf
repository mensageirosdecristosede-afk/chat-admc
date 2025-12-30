# S3 Bucket para armazenamento de conversas e conhecimento
resource "aws_s3_bucket" "chat_bucket" {
  bucket = "${var.project_name}-data-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name = "${var.project_name}-data"
  }
}

resource "aws_s3_bucket_versioning" "chat_bucket" {
  bucket = aws_s3_bucket.chat_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "chat_bucket" {
  bucket = aws_s3_bucket.chat_bucket.id

  rule {
    id     = "delete-old-conversations"
    status = "Enabled"

    expiration {
      days = 90
    }

    filter {
      prefix = "conversations/"
    }
  }

  rule {
    id     = "delete-old-incoming"
    status = "Enabled"

    expiration {
      days = 30
    }

    filter {
      prefix = "incoming-messages/"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "chat_bucket" {
  bucket = aws_s3_bucket.chat_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Criar estrutura de pastas no S3
resource "aws_s3_object" "knowledge_base_folder" {
  bucket       = aws_s3_bucket.chat_bucket.id
  key          = "knowledge-base/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "conversations_folder" {
  bucket       = aws_s3_bucket.chat_bucket.id
  key          = "conversations/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "incoming_messages_folder" {
  bucket       = aws_s3_bucket.chat_bucket.id
  key          = "incoming-messages/"
  content_type = "application/x-directory"
}

# Upload de contexto padrão da igreja
resource "aws_s3_object" "church_context" {
  bucket       = aws_s3_bucket.chat_bucket.id
  key          = "knowledge-base/church-context.txt"
  content_type = "text/plain"
  content      = <<-EOT
    Igreja ADMC - Assembleia de Deus Ministério Caná
    
    INFORMAÇÕES GERAIS:
    - Nome: Assembleia de Deus Ministério Caná (ADMC)
    - Denominação: Evangélica Pentecostal
    - Missão: Pregar o evangelho e fazer discípulos
    
    HORÁRIOS DE CULTOS:
    - Terça-feira: 19h30 - Culto de Doutrina
    - Quinta-feira: 19h30 - Culto de Oração
    - Domingo: 09h00 - Escola Bíblica Dominical
    - Domingo: 19h00 - Culto de Celebração
    
    LOCALIZAÇÃO:
    [CONFIGURAR ENDEREÇO COMPLETO]
    
    CONTATOS:
    - Telefone: [CONFIGURAR]
    - Email: [CONFIGURAR]
    - WhatsApp: [CONFIGURAR]
    
    MINISTÉRIOS:
    - Ministério de Louvor
    - Ministério Infantil
    - Ministério de Jovens
    - Ministério de Mulheres
    - Ministério de Homens
    - Ministério de Intercessão
    
    EVENTOS REGULARES:
    - Congresso de Jovens
    - Conferência de Mulheres
    - Seminário de Casais
    - Retiro Espiritual
    
    INFORMAÇÕES PARA VISITANTES:
    - Seja bem-vindo! Nossa igreja está de portas abertas
    - Não há código de vestimenta específico
    - Temos estacionamento disponível
    - Ministério infantil durante os cultos
    - Após o culto, servimos um café de confraternização
    
    COMO POSSO AJUDAR:
    - Informações sobre horários e localização
    - Dúvidas sobre eventos e programações
    - Oração e aconselhamento espiritual
    - Informações sobre batismo e membresia
    - Contato com a liderança
    
    VERSÍCULOS IMPORTANTES:
    - "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito..." - João 3:16
    - "Vinde a mim, todos os que estais cansados..." - Mateus 11:28
    - "Eu sou o caminho, a verdade e a vida..." - João 14:6
  EOT
}

# Data source para obter account ID
data "aws_caller_identity" "current" {}
