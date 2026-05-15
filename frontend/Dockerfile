
FROM node:18-alpine

WORKDIR /app

RUN apk update && apk add --no-cache git

COPY package.json ./
RUN npm install

COPY . .

ENV REACT_APP_API_URL=http://localhost:8000

CMD ["npm", "start"]
