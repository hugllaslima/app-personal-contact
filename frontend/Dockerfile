# Usa a imagem oficial do Nginx
FROM nginx:alpine

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuração personalizada (SEM template)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos estáticos do frontend
COPY src/ /usr/share/nginx/html/

# Expõe a porta 80
EXPOSE 80

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]
