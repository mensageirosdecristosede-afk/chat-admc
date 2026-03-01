# IAM Role para Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Policy para CloudWatch Logs
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# Policy customizada para S3 (Bedrock removido - usando Gemini gratuito)
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.chat_bucket.arn,
          "${aws_s3_bucket.chat_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ]
        Resource = [
          "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.project_name}/*"
        ]
      }
    ]
  })
}

# Armazenar secrets no SSM Parameter Store
resource "aws_ssm_parameter" "meta_verify_token" {
  name        = "/${var.project_name}/meta/verify-token"
  description = "Token de verificação do Meta"
  type        = "SecureString"
  value       = var.meta_verify_token

  tags = {
    Name = "${var.project_name}-meta-verify-token"
  }
}

resource "aws_ssm_parameter" "meta_app_secret" {
  name        = "/${var.project_name}/meta/app-secret"
  description = "App Secret do Meta"
  type        = "SecureString"
  value       = var.meta_app_secret

  tags = {
    Name = "${var.project_name}-meta-app-secret"
  }
}

resource "aws_ssm_parameter" "meta_access_token" {
  name        = "/${var.project_name}/meta/access-token"
  description = "Token de acesso do Meta"
  type        = "SecureString"
  value       = var.meta_access_token

  tags = {
    Name = "${var.project_name}-meta-access-token"
  }
}

resource "aws_ssm_parameter" "gemini_api_key" {
  name        = "/${var.project_name}/gemini/api-key"
  description = "API Key do Google Gemini"
  type        = "SecureString"
  value       = var.gemini_api_key

  tags = {
    Name = "${var.project_name}-gemini-api-key"
  }
}
