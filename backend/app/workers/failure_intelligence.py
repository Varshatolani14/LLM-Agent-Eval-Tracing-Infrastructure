from sklearn.cluster import KMeans
import numpy as np
from ..db.session import SessionLocal
from ..models.schemas import Trace, Span, FailureCluster
import asyncio

async def cluster_failures():
    db = SessionLocal()
    # Find spans with errors or low evaluation scores
    failed_spans = db.query(Span).filter(Span.status == "failure").all()
    
    if not failed_spans:
        print("No failures found to cluster.")
        return

    # Extract error messages or low-quality responses
    texts = [s.attributes.get("response", "") for s in failed_spans]
    
    # In a real system, we would use sentence-transformers to get embeddings
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    # embeddings = model.encode(texts)
    
    # Mock embeddings for demonstration
    embeddings = np.random.rand(len(texts), 384)
    
    if len(embeddings) < 2:
        print("Not enough failures to cluster.")
        return

    n_clusters = min(3, len(embeddings))
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(embeddings)
    
    for i in range(n_clusters):
        cluster_indices = np.where(clusters == i)[0]
        representative_idx = cluster_indices[0]
        
        new_cluster = FailureCluster(
            cluster_name=f"Failure Group {i+1}",
            description=f"Group of {len(cluster_indices)} similar failures.",
            representative_trace_id=failed_spans[representative_idx].trace_id
        )
        db.add(new_cluster)
    
    db.commit()
    print(f"Clustered failures into {n_clusters} groups.")
    db.close()

if __name__ == "__main__":
    asyncio.run(cluster_failures())
