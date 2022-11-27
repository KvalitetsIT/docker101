FROM node:16         
ENV NODE_ENV=production
WORKDIR /app
COPY app/package.json .
RUN npm install
COPY app/source/app.js app.js
RUN whoami
CMD node app.js
