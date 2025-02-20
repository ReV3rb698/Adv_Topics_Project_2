FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install bcrypt
COPY . .
EXPOSE 5000
CMD ["node", "server.js"]
