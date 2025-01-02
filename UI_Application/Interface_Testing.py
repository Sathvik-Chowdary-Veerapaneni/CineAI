# Keys Avalible in Qdrant

#movie_title: str
#movie_id: float
#runtime: NoneType, float
#release_date: NoneType, str
# combined_text: str
# movie_id_1: int
# runtime_1: int
# movie_overview: str
# movie_original_language: str


import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, Range
from sentence_transformers import SentenceTransformer

# Qdrant configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "movie_collection_test_sample_1"

# Initialize Qdrant client
client = QdrantClient(url=QDRANT_URL)

# Load SentenceTransformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def search_qdrant(query_text: str, top_k: int = 5):
    """
    Embed the given query_text, then search Qdrant for the top_k results.
    """
    query_embedding = model.encode(query_text).tolist()
    return client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

def main():
    st.title("Chat Interface to Retrieve Movie")

    with st.form(key="search_form"):
        query_text = st.text_input("Enter the text")
        submitted = st.form_submit_button("Search")
    
    if submitted and query_text.strip():
        results = search_qdrant(query_text, top_k=5)

        st.subheader("Top Qdrant Matches:")
        for i, hit in enumerate(results, start=1):
            movie_title = hit.payload.get("movie_title", "No 'movie_title' found")
            release_date = hit.payload.get("release_date", "No 'release_date' found")
            runtime = hit.payload.get("runtime_1", "No 'runtime' found")
            overview = hit.payload.get("movie_overview", "No 'movie_overview' found")

            st.write(f"""
            **{i}.**  
            - **Movie Name**: {movie_title}
            - **Release Date**: {release_date}
            - **Runtime**: {runtime}
            - **Overview**: {overview}
            """)

if __name__ == "__main__":
    main()