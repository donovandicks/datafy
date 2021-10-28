FROM node:14-alpine AS base

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./

RUN npm ci

COPY . ./

CMD ["npm", "run", "dev"]