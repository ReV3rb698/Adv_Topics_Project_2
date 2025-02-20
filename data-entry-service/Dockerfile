FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install bcrypt
COPY . .
EXPOSE 5001
CMD ["node", "server.js"]
