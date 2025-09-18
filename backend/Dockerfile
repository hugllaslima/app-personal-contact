# Usa uma imagem base Python oficial
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação da pasta 'src' para o diretório de trabalho do contêiner
COPY src/ /app/src/

# Expõe a porta em que a aplicação Flask será executada
EXPOSE 5000

# Comando para iniciar a aplicação Flask usando Gunicorn
# Note que o caminho agora é 'src.app:app' porque 'app.py' está dentro de 'src'
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
