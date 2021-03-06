# Stage 1 - the build process
FROM node:12.16.1-slim as build-deps

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source (specify folders to max efficiency fo docker cache)
COPY src ./src
COPY public ./public

RUN npm run build

# Stage 2 - the production environment
FROM nginx:1.17.9-alpine
COPY --from=build-deps /usr/src/app/build /var/www
COPY nginx.conf /etc/nginx/nginx.conf.template
# default container port for GCP is 8080
EXPOSE 8080
ENV PORT 8080

# Default env vars for accessing proxied services
ENV BLOCK_ENDPOINT http://block:8000

CMD envsubst '$PORT $BLOCK_ENDPOINT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'
