FROM node:14-bullseye-slim as develop-stage
WORKDIR /app

COPY ./SearchQAArbeitsrecht_o/package*.json ./
RUN npm ci

COPY ./SearchQAArbeitsrecht_o/*.json /app/
COPY ./SearchQAArbeitsrecht_o/src ./src
COPY ./SearchQAArbeitsrecht_o/e2e ./e2e
COPY ./server.js /app/server.js

RUN npm run build -- --configuration production

RUN chown -R 1001:0 /app && \
    chmod -R g=u /app

USER 1001

EXPOSE 4200

CMD ["node", "server.js"]
