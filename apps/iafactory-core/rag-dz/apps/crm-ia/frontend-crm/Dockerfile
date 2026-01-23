# Use an official Node.js image as a base
FROM node:20-alpine AS base

# Install dependencies and build the project
FROM base AS build
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

# Set production environment
ENV NODE_ENV production

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED 1

# Copy built application from the build stage
COPY --from=build /app/.next ./.next
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/public ./public

# Copy other necessary files (package.json for metadata, etc.)
COPY package.json ./package.json

EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]
