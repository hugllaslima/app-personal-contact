# Usa a imagem oficial do Nginx
FROM nginx:alpine

# Remove a configuração padrão do Nginx (se existir)
RUN rm -f /etc/nginx/conf.d/default.conf

# Copia configuração fixa do Nginx (sem uso de templates)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos estáticos do frontend
COPY src/ /usr/share/nginx/html/

# Expõe a porta 80
EXPOSE 80

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]
