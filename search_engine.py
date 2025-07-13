import faiss
import numpy as np
from typing import List, Tuple, Dict
from transcript_processor import TranscriptChunk
from sentence_transformers import SentenceTransformer
import json

class VideoSearchEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the video search engine with FAISS index and embedding model."""
        self.embedding_model = SentenceTransformer(model_name)
        self.chunks: List[TranscriptChunk] = []
        self.index = None
        self.dimension = None
        
    def add_chunks(self, chunks: List[TranscriptChunk]):
        """Add transcript chunks to the search index."""
        self.chunks.extend(chunks)
        
        # Initialize FAISS index if not already done
        if self.index is None and chunks:
            valid_chunks = [chunk for chunk in chunks if chunk.embedding is not None]
            if valid_chunks:
                self.dimension = valid_chunks[0].embedding.shape[0]  # type: ignore
                self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
            
        # Add embeddings to FAISS index
        if chunks:
            valid_chunks = [chunk for chunk in chunks if chunk.embedding is not None]
            if valid_chunks:
                embeddings = np.array([chunk.embedding for chunk in valid_chunks])  # type: ignore
                self.index.add(embeddings.astype('float32'))  # type: ignore
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for the most similar video chunks to the given query."""
        if not self.chunks or self.index is None:
            return []
        
        # Embed the query
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS index
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)  # type: ignore
        
        # Return results with metadata
        results = []
        for score, idx in zip(scores[0], indices[0]):
            chunk = self.chunks[idx]
            results.append({
                'video_id': chunk.video_id,
                'start_time': chunk.start_time,
                'end_time': chunk.end_time,
                'text': chunk.text,
                'similarity_score': float(score),
                'timestamp_formatted': self._format_timestamp(chunk.start_time)
            })
        
        return results
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds into MM:SS format."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def get_video_summary(self, video_id: str) -> Dict:
        """Get summary information for a specific video."""
        video_chunks = [chunk for chunk in self.chunks if chunk.video_id == video_id]
        
        if not video_chunks:
            return {}
        
        total_duration = max(chunk.end_time for chunk in video_chunks)
        chunk_count = len(video_chunks)
        
        return {
            'video_id': video_id,
            'total_duration': total_duration,
            'chunk_count': chunk_count,
            'duration_formatted': self._format_timestamp(total_duration)
        }
    
    def get_all_videos(self) -> List[str]:
        """Get list of all video IDs in the index."""
        return list(set(chunk.video_id for chunk in self.chunks))
    
    def search_by_video(self, video_id: str, query: str, top_k: int = 3) -> List[Dict]:
        """Search within a specific video only."""
        video_chunks = [chunk for chunk in self.chunks if chunk.video_id == video_id]
        
        if not video_chunks:
            return []
        
        # Create temporary index for this video
        temp_index = faiss.IndexFlatIP(self.dimension)
        valid_chunks = [chunk for chunk in video_chunks if chunk.embedding is not None]
        if valid_chunks:
            embeddings = np.array([chunk.embedding for chunk in valid_chunks])  # type: ignore
            temp_index.add(embeddings.astype('float32'))  # type: ignore
        
        # Search
        query_embedding = self.embedding_model.encode([query])
        scores, indices = temp_index.search(query_embedding.astype('float32'), top_k)  # type: ignore
        
        # Return results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            chunk = video_chunks[idx]
            results.append({
                'video_id': chunk.video_id,
                'start_time': chunk.start_time,
                'end_time': chunk.end_time,
                'text': chunk.text,
                'similarity_score': float(score),
                'timestamp_formatted': self._format_timestamp(chunk.start_time)
            })
        
        return results 