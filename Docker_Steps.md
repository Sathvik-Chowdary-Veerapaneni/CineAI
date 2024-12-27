# Clean Setup of Qdrant in Docker

Below is a step-by-step explanation of what we’ve done so far, along with why it works and the expected results at each step.

---

## 1. Removing Old Containers, Volumes, and Images

**What We Did**
1. Stopped and removed any old Qdrant containers.  
2. Removed any Docker volumes associated with Qdrant (so we start fresh).  
3. Removed the Qdrant image from our local system.

**Why We Did It**
- We wanted a completely **clean environment** to prevent conflicts with old data or container settings.  
- Removing the old image forces Docker to **pull a fresh copy** of Qdrant the next time we run it.

**Expected Result**
- No Qdrant containers or volumes remain.  
- When we list images with `docker images`, Qdrant is no longer present.

---

## 2. Pulling and Running a Fresh Qdrant Image

**What We Did**
1. **Pulled the latest Qdrant image**:
   ```bash
   docker pull qdrant/qdrant:latest

tarted the container (detached mode, binding the container’s port 6333 to your local port 6333, and mounting a named volume):
bash
Copy code
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v qdrant_data_semantic_retrieval:/qdrant/storage \
  qdrant/qdrant:latest
Why We Did It

Pulling ensures we have the latest version of Qdrant.
Running Qdrant as a container:
-d runs it in detached (background) mode.
--name qdrant names the container for easier management.
-p 6333:6333 exposes the Qdrant server’s port to the host machine.
-v qdrant_data_semantic_retrieval:/qdrant/storage ensures persistent storage.
Expected Result

docker ps will show a running container named qdrant.
Qdrant is listening on port 6333 of your host.
3. Understanding the Entrypoint (./entrypoint.sh)
What It Is

In Qdrant’s Docker image, the ENTRYPOINT directive is set to run entrypoint.sh.
This script automatically starts the Qdrant server (the actual database process).
Why This Is the Default

By specifying ENTRYPOINT ["./entrypoint.sh"] in the Dockerfile, Docker automatically runs entrypoint.sh each time the container starts, ensuring Qdrant is up and running.
Expected Result

When you run docker run ... qdrant/qdrant:latest, Docker executes that script, so Qdrant is ready to handle requests inside the container.
4. Verifying Qdrant with curl
What We Did

bash
Copy code
curl http://localhost:6333/collections
This endpoint lists all collections in Qdrant.

Why We Did It

Checking /collections confirms Qdrant is running and responding to the default REST API.
Expected Result

A JSON response, for example:
json
Copy code
{"result": {"collections": []}, "status": "ok", "time": 0.000036916}
Indicates no collections (an empty list) since we haven’t created any yet.
Summary
We removed all old Qdrant containers, volumes, and images for a fresh start.
We pulled and ran the latest Qdrant Docker image, which automatically executes entrypoint.sh to start Qdrant.
We verified Qdrant is live by using curl to call the /collections endpoint, returning an empty array.