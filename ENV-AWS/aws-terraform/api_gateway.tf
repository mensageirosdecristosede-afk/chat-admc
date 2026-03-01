# API Gateway REST API
resource "aws_api_gateway_rest_api" "webhook_api" {
  name        = "${var.project_name}-webhook-api"
  description = "API Gateway para receber webhooks do Meta"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = "${var.project_name}-webhook-api"
  }
}

# Resource /webhook
resource "aws_api_gateway_resource" "webhook" {
  rest_api_id = aws_api_gateway_rest_api.webhook_api.id
  parent_id   = aws_api_gateway_rest_api.webhook_api.root_resource_id
  path_part   = "webhook"
}

# Método GET (para verificação)
resource "aws_api_gateway_method" "webhook_get" {
  rest_api_id   = aws_api_gateway_rest_api.webhook_api.id
  resource_id   = aws_api_gateway_resource.webhook.id
  http_method   = "GET"
  authorization = "NONE"
}

# Método POST (para mensagens)
resource "aws_api_gateway_method" "webhook_post" {
  rest_api_id   = aws_api_gateway_rest_api.webhook_api.id
  resource_id   = aws_api_gateway_resource.webhook.id
  http_method   = "POST"
  authorization = "NONE"
}

# Integração Lambda GET
resource "aws_api_gateway_integration" "webhook_get_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.webhook_api.id
  resource_id             = aws_api_gateway_resource.webhook.id
  http_method             = aws_api_gateway_method.webhook_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.webhook_handler.invoke_arn
}

# Integração Lambda POST
resource "aws_api_gateway_integration" "webhook_post_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.webhook_api.id
  resource_id             = aws_api_gateway_resource.webhook.id
  http_method             = aws_api_gateway_method.webhook_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.webhook_handler.invoke_arn
}

# Deploy da API
resource "aws_api_gateway_deployment" "webhook_api" {
  rest_api_id = aws_api_gateway_rest_api.webhook_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.webhook.id,
      aws_api_gateway_method.webhook_get.id,
      aws_api_gateway_method.webhook_post.id,
      aws_api_gateway_integration.webhook_get_lambda.id,
      aws_api_gateway_integration.webhook_post_lambda.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Stage da API
resource "aws_api_gateway_stage" "webhook_api" {
  deployment_id = aws_api_gateway_deployment.webhook_api.id
  rest_api_id   = aws_api_gateway_rest_api.webhook_api.id
  stage_name    = var.environment

  xray_tracing_enabled = false

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
}

# Configurações de throttling (logging desabilitado para evitar erro de CloudWatch role)
resource "aws_api_gateway_method_settings" "webhook_api" {
  rest_api_id = aws_api_gateway_rest_api.webhook_api.id
  stage_name  = aws_api_gateway_stage.webhook_api.stage_name
  method_path = "*/*"

  settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
    metrics_enabled        = true
  }
}

# CloudWatch Log Group para API Gateway
resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/${var.project_name}-webhook-api"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-api-gateway-logs"
  }
}
