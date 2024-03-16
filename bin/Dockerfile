# Use Node.js version 18 as the base image
FROM node:18

# Set the working directory in the container
WORKDIR .

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Expose the port your app runs on
EXPOSE 3000

# Command to run your application
CMD ["node", "src/app.js"]
