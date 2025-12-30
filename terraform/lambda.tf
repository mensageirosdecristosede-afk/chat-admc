# Empacotar código Lambda
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/lambda_function.zip"
  excludes    = ["__pycache__", "*.pyc", ".pytest_cache", "venv", "env"]
}

# Lambda Layer para dependências
resource "aws_lambda_layer_version" "dependencies" {
  filename            = "${path.module}/lambda_layer.zip"
  layer_name          = "${var.project_name}-dependencies"
  compatible_runtimes = ["python3.11"]
  description         = "Dependências para a função Lambda"

  lifecycle {
    create_before_destroy = true
  }
}

# Lambda Function
resource "aws_lambda_function" "webhook_handler" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.project_name}-webhook-handler"
  role            = aws_iam_role.lambda_role.arn
  handler         = "webhook_handler.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 60
  memory_size     = 512

  layers = [aws_lambda_layer_version.dependencies.arn]

  environment {
    variables = {
      S3_BUCKET_NAME      = aws_s3_bucket.chat_bucket.id
      META_VERIFY_TOKEN   = var.meta_verify_token
      META_APP_SECRET     = var.meta_app_secret
      WHATSAPP_PHONE_ID   = var.whatsapp_phone_id
      META_ACCESS_TOKEN   = var.meta_access_token
      GEMINI_API_KEY      = var.gemini_api_key
      AWS_REGION          = var.aws_region
    }
  }

  tags = {
    Name = "${var.project_name}-webhook-handler"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.webhook_handler.function_name}"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-lambda-logs"
  }
}

# Permissão para API Gateway invocar Lambda
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.webhook_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.webhook_api.execution_arn}/*/*"
}
