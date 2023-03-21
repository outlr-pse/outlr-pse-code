# build stage
FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
ARG API_URL
RUN printf '{ "API_URL": "%s" }' "$API_URL" > src/config.json
RUN npm run build

# production stage
FROM nginx:1.23-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
