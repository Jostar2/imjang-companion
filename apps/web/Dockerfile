FROM node:22-alpine

WORKDIR /app/apps/web

ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

COPY apps/web/package.json /app/apps/web/package.json
COPY apps/web/package-lock.json /app/apps/web/package-lock.json
RUN npm install

COPY apps/web /app/apps/web

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
