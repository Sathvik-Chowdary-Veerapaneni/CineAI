# Use a lightweight Python base image
FROM python:3.10-slim

# Set an environment variable for Qdrant version
ENV QDRANT_VERSION="v1.4.0"

# Update packages and install dependencies for downloading/unzipping Qdrant
RUN apt-get update -y && \
    apt-get install -y curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Download and install Qdrant (Linux x86_64 MUSL build)
RUN curl -L \
    "https://github.com/qdrant/qdrant/releases/download/${QDRANT_VERSION}/qdrant-${QDRANT_VERSION}-x86_64-unknown-linux-musl.zip" \
    -o qdrant.zip \
 && unzip qdrant.zip -d /usr/local/bin \
 && rm qdrant.zip

# Install Python packages you need (example: semantic retrieval libs)
RUN pip install --no-cache-dir \
    qdrant-client \
    sentence-transformers \
    uvicorn \
    fastapi

# Create a directory for Qdrant data (if you want to store inside container)
RUN mkdir -p /qdrant/storage

# Copy a simple entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Qdrant's ports (REST on 6333, gRPC on 6334)
EXPOSE 6333
EXPOSE 6334

# By default, run the entrypoint
CMD ["/entrypoint.sh"]
