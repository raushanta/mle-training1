# Use a base image with the desired runtime (e.g., Node.js, Python, etc.)
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose the port your web application is listening on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
