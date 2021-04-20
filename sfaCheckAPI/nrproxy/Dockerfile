FROM nginx:alpine
LABEL  maintainer "y.yoshimoto"


# コンテツファイルの設置
COPY contents/* /usr/share/nginx/html/

# nginx設定ファイルの設置
COPY nginx.conf /etc/nginx/nginx.conf
COPY server.conf /etc/nginx/conf.d/server.conf

# コンテナ実行時の動作設定
EXPOSE 80
ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]