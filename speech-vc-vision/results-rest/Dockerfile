FROM node:16-alpine

WORKDIR /app

RUN npm init -y && \
    npm install express cors mongodb

COPY . .

ENV DB_URL=${DB_URL}
ENV DB_NAME=${DB_NAME}
ENV DB_TABLE_NAME=${DB_TABLE_NAME}

EXPOSE 3000

CMD ["node", "app.js"]

