output "webhook_url" {
  description = "URL do webhook para configurar no Meta"
  value       = "${aws_api_gateway_stage.webhook_api.invoke_url}/webhook"
}

output "s3_bucket_name" {
  description = "Nome do bucket S3 para armazenamento"
  value       = aws_s3_bucket.chat_bucket.id
}

output "lambda_function_name" {
  description = "Nome da função Lambda"
  value       = aws_lambda_function.webhook_handler.function_name
}

output "lambda_function_arn" {
  description = "ARN da função Lambda"
  value       = aws_lambda_function.webhook_handler.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch Log Group da Lambda"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

output "api_gateway_id" {
  description = "ID da API Gateway"
  value       = aws_api_gateway_rest_api.webhook_api.id
}

output "setup_instructions" {
  description = "Próximos passos"
  value       = <<-EOT
    ✅ Infraestrutura criada com sucesso!
    
    📋 PRÓXIMOS PASSOS:
    
    1. Configure o webhook no Meta Developer Console:
       URL: ${aws_api_gateway_stage.webhook_api.invoke_url}/webhook
       Verify Token: [O token configurado no tfvars]
    
    2. Faça upload do contexto da igreja:
       aws s3 cp church-context.txt s3://${aws_s3_bucket.chat_bucket.id}/knowledge-base/
    
    3. Teste o webhook:
       curl -X GET "${aws_api_gateway_stage.webhook_api.invoke_url}/webhook?hub.mode=subscribe&hub.verify_token=SEU_TOKEN&hub.challenge=test"
    
    4. Monitore os logs:
       aws logs tail ${aws_cloudwatch_log_group.lambda_logs.name} --follow
    
    📦 Recursos criados:
       - Lambda: ${aws_lambda_function.webhook_handler.function_name}
       - S3 Bucket: ${aws_s3_bucket.chat_bucket.id}
       - API Gateway: ${aws_api_gateway_rest_api.webhook_api.name}
  EOT
}
