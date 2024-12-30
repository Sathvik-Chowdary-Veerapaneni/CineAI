import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, Range
from sentence_transformers import SentenceTransformer

# 1. Configure Qdrant connection
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "movie_collection_test_sample_1"

# 2. Initialize Qdrant client
client = QdrantClient(url=QDRANT_URL)

# 3. Load SentenceTransformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def search_qdrant(query_text: str, top_k: int = 5):
    """
    Embed the given query_text, then search Qdrant for the top_k results.
    """
    query_embedding = model.encode(query_text).tolist()
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )
    return search_results

def main():
    """
    Streamlit app for querying Qdrant.
    """
    st.title("Chat Interface to Retrieve Movie")

    # User inputs a query
    query_text = st.text_input("Enter the text", value="Iron Man")
    
    if st.button("Search"):
        if query_text.strip():
            # Perform the Qdrant search
            results = search_qdrant(query_text, top_k=5)

            st.subheader("Top Qdrant Matches:")
            for i, hit in enumerate(results, start=1):
                # Use the correct payload fields (no "text" field!)
                movie_id = hit.payload.get("movie_id", "No 'movie_id' found")
                runtime = hit.payload.get("runtime", "No 'runtime' found")
                release_date = hit.payload.get("release_date", "No 'release_date' found")
                combined_text = hit.payload.get("combined_text", "No 'combined_text' found")
                score = hit.score

                # Show them in any format you like
                st.write(f"""
                **{i}.**  
                - **Movie ID**: {movie_id}  
                - **Runtime**: {runtime}  
                - **Release Date**: {release_date}  
                - **Combined Text**: {combined_text}  
                - **Score**: {score:.4f}
                """)
        else:
            st.warning("Please enter a valid query.")

if __name__ == "__main__":
    main()
