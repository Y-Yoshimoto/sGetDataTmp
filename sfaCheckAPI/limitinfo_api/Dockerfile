FROM node:latest
LABEL  maintainer "y.yoshimoto"
ENV APPNAME limitinfo_api

# ワークディレクトリ作成
#WORKDIR /usr/src/app
RUN mkdir -p /$APPNAME/src
WORKDIR /$APPNAME

# npmパッケージ
# COPY package*.json ./
COPY ./package.json /$APPNAME/package.json
#RUN npm install

RUN yarn install 

# RUN npm install --only=production
# ソースコード配置
COPY ./src/* src/

EXPOSE 8040
#ENTRYPOINT ["yarn", "start"]
ENTRYPOINT ["yarn", "debug"]
