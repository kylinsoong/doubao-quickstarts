FROM nginx:1.27.1

COPY conf/app.conf /etc/nginx/conf.d/
COPY tls/example.com.crt /etc/nginx
COPY tls/example.com.key /etc/nginx

EXPOSE 8080 8443

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
