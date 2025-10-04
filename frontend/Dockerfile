# Usa a imagem oficial do Nginx
FROM nginx:alpine

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia a sua configuração personalizada do Nginx
COPY nginx.conf.template /etc/nginx/templates/contact-app.conf.template

# Copia os arquivos estáticos do frontend da pasta 'src' para o diretório de serviço do Nginx
COPY src/ /usr/share/nginx/html

# Expõe a porta 80, que é a porta padrão do Nginx
EXPOSE 80

# O comando padrão do Nginx já inicia o servidor
CMD ["nginx", "-g", "daemon off;"]
