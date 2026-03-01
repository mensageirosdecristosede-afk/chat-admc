# Infraestrutura GCP - Chat ADMC

## Componentes Criados

- **Cloud Storage Bucket**: Armazena arquivos e código da função.
- **Cloud Function (Python)**: Endpoint HTTP para processamento.
- **Artifact Registry**: Usado para build e cache de imagens.
- **Permissões**: Service accounts ajustadas para build, logs e deploy.

## Arquitetura

```
Usuário → Cloud Function (HTTP) → Cloud Storage
           ↑
         Cloud Build (deploy)
           ↑
     Artifact Registry (cache)
```

## Como testar

1. Após `terraform apply`, pegue o output `function_url`.
2. Faça uma requisição HTTP:
   ```
   curl https://<function_url>
   ```
   Deve retornar: `Hello from Chat ADMC Cloud Function!`

## Próximos passos

- Personalizar o código da Cloud Function conforme sua lógica.
- Integrar com Google Gemini API (aproveitando o free tier).
- Monitorar logs e permissões.
- Garantir que não há custos: use apenas recursos do free tier, evite uploads grandes e execuções excessivas.

## Revisão de custos (Free Tier)

- **Cloud Functions**: 2 milhões de invocações/mês, 400 mil GB-segundos/mês.
- **Cloud Storage**: 5 GB/mês.
- **Artifact Registry**: 0,5 GB/mês.
- **Cloud Build**: 120 minutos/mês.

> Se exceder esses limites, haverá cobrança. Monitore pelo console GCP (Billing).

## Checklist de monitoramento

- [ ] Verificar quotas e limites no console GCP.
- [ ] Configurar alertas de orçamento.
- [ ] Monitorar logs de invocações e uso.
- [ ] Evitar uploads e execuções fora do free tier.

---

**Qualquer dúvida ou erro, envie o log para análise!**
