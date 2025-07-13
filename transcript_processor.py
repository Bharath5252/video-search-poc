import whisper
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Optional
import json
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class TranscriptChunk:
    video_id: str
    start_time: float
    end_time: float
    text: str
    embedding: Optional[np.ndarray] = None

class TranscriptProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the transcript processor with Whisper and sentence transformer models."""
        self.whisper_model = whisper.load_model("base")
        self.embedding_model = SentenceTransformer(model_name)
        
    def transcribe_video(self, video_path: str, video_id: str) -> List[Dict]:
        """Transcribe a video using Whisper and return segments with timestamps."""
        print(f"Transcribing video: {video_id}")
        result = self.whisper_model.transcribe(video_path)
        return result["segments"]  # type: ignore
    
    def chunk_transcript(self, segments: List[Dict], video_id: str, 
                        chunk_duration: float = 30.0) -> List[TranscriptChunk]:
        """Chunk transcript segments into ~30-second chunks."""
        chunks = []
        current_chunk_text = []
        current_start_time = segments[0]["start"] if segments else 0.0
        
        for segment in segments:
            segment_start = segment["start"]
            segment_end = segment["end"]
            segment_text = segment["text"].strip()
            
            # If adding this segment would exceed chunk duration, save current chunk
            if segment_end - current_start_time > chunk_duration and current_chunk_text:
                chunk = TranscriptChunk(
                    video_id=video_id,
                    start_time=current_start_time,
                    end_time=segment_start,
                    text=" ".join(current_chunk_text)
                )
                chunks.append(chunk)
                
                # Start new chunk
                current_chunk_text = [segment_text]
                current_start_time = segment_start
            else:
                current_chunk_text.append(segment_text)
        
        # Add the last chunk
        if current_chunk_text:
            chunk = TranscriptChunk(
                video_id=video_id,
                start_time=current_start_time,
                end_time=segments[-1]["end"] if segments else 0.0,
                text=" ".join(current_chunk_text)
            )
            chunks.append(chunk)
        
        return chunks
    
    def embed_chunks(self, chunks: List[TranscriptChunk]) -> List[TranscriptChunk]:
        """Generate embeddings for all chunks using sentence transformers."""
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedding_model.encode(texts)
        
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
        
        return chunks
    
    def process_video(self, video_path: str, video_id: str) -> List[TranscriptChunk]:
        """Complete pipeline: transcribe, chunk, and embed a video."""
        segments = self.transcribe_video(video_path, video_id)
        chunks = self.chunk_transcript(segments, video_id)
        chunks_with_embeddings = self.embed_chunks(chunks)
        return chunks_with_embeddings

# Mock data generator for demo purposes
def generate_mock_transcripts() -> List[TranscriptChunk]:
    """Generate mock transcript chunks for demonstration."""
    mock_data = [
        {
            "video_id": "video_001",
            "chunks": [
                {
                    "start_time": 0.0,
                    "end_time": 30.0,
                    "text": "Welcome to our tutorial on machine learning basics. In this video, we'll cover the fundamentals of supervised learning algorithms."
                },
                {
                    "start_time": 30.0,
                    "end_time": 60.0,
                    "text": "Let's start with linear regression. This is one of the simplest and most widely used machine learning algorithms for prediction."
                },
                {
                    "start_time": 60.0,
                    "end_time": 90.0,
                    "text": "Next, we'll discuss classification problems and how logistic regression can help us solve them effectively."
                }
            ]
        },
        {
            "video_id": "video_002",
            "chunks": [
                {
                    "start_time": 0.0,
                    "end_time": 30.0,
                    "text": "Today we're going to explore deep learning and neural networks. These powerful tools have revolutionized artificial intelligence."
                },
                {
                    "start_time": 30.0,
                    "end_time": 60.0,
                    "text": "We'll start with the basic structure of a neural network, including input layers, hidden layers, and output layers."
                },
                {
                    "start_time": 60.0,
                    "end_time": 90.0,
                    "text": "Understanding backpropagation is crucial for training neural networks. Let me explain how this algorithm works."
                }
            ]
        },
        {
            "video_id": "video_003",
            "chunks": [
                {
                    "start_time": 0.0,
                    "end_time": 30.0,
                    "text": "In this video, we'll discuss natural language processing techniques and how to build chatbots using modern NLP libraries."
                },
                {
                    "start_time": 30.0,
                    "end_time": 60.0,
                    "text": "We'll cover tokenization, word embeddings, and how to use transformers for text classification tasks."
                },
                {
                    "start_time": 60.0,
                    "end_time": 90.0,
                    "text": "Finally, let's look at how to deploy your NLP models in production and handle real-world text data."
                }
            ]
        }
    ]
    
    processor = TranscriptProcessor()
    all_chunks = []
    
    for video_data in mock_data:
        video_id = video_data["video_id"]
        for chunk_data in video_data["chunks"]:
            chunk = TranscriptChunk(
                video_id=video_id,
                start_time=chunk_data["start_time"],
                end_time=chunk_data["end_time"],
                text=chunk_data["text"]
            )
            all_chunks.append(chunk)
    
    # Generate embeddings for all chunks
    return processor.embed_chunks(all_chunks) 