# Usa a imagem oficial do Nginx
FROM nginx:alpine

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuração personalizada do Nginx (SEM .template)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos estáticos do frontend
COPY src/ /usr/share/nginx/html/

# Expõe a porta 80
EXPOSE 80

# Healthcheck para o Nginx
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]
