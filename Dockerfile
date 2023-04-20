# Use uma imagem Python como base
FROM python:3.9-alpine

# Copie o arquivo de sincronização para o container
COPY sync.py /app/sync.py

# Instale as dependências necessárias
RUN pip install boto3 minio requests

# Defina as variáveis de ambiente como variáveis de tempo de execução
ENV AWS_ACCESS_KEY_ID <access-key-id>
ENV AWS_SECRET_ACCESS_KEY <secret-access-key>
ENV MINIO_ENDPOINT <minio-endpoint>
ENV MINIO_ACCESS_KEY <minio-access-key>
ENV MINIO_SECRET_KEY <minio-secret-key>

# Defina o comando para executar o código ao iniciar o container
CMD ["python", "/app/sync.py"]
