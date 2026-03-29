# Stage 1: Build the Vite frontend
FROM node:20-alpine AS build-stage
WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python backend
FROM python:3.13-slim
WORKDIR /app/backend

# Install system dependencies for any compiled python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory 
# (This includes .env and config/ intentionally to let the container have its own local copy modifiable via Admin API)
COPY backend/ ./

# Copy the built Vite static files from the build stage into the location expected by FastAPI
COPY --from=build-stage /app/frontend/dist /app/frontend/dist

# Expose port (FastAPI runs on 8000)
EXPOSE 8000

# Set the command to run FastAPI instead of Streamlit
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
