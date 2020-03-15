# Noddy nginx server to pass healthcheck
FROM nginx
RUN mkdir -p /usr/share/nginx/html
RUN echo 'Hello world!' > /usr/share/nginx/html/index.html
COPY nginx/default.template /etc/nginx/conf.d/default.template
# Substitute the environment variables and generate the final config
CMD envsubst < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'