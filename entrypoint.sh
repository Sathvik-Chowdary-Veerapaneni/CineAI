#!/usr/bin/env bash

# Start Qdrant (REST on 0.0.0.0:6333, gRPC on 0.0.0.0:6334), 
# storing data in /qdrant/storage
qdrant \
  --uri "0.0.0.0:6333" \
  --grpc-uri "0.0.0.0:6334" \
  --storage "/qdrant/storage" &

# Optionally, run any Python app here or just keep the container running
# For example, to keep the container alive indefinitely:
tail -f /dev/null
