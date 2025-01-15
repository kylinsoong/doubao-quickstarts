FROM node:16-alpine

WORKDIR /app

RUN npm init -y && \
    npm install express ejs axios express-session

COPY . .

ENV BACKEND_API_HOST=${BACKEND_API_HOST}

EXPOSE 3000

CMD ["node", "app.js"]

