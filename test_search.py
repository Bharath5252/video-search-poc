#!/usr/bin/env python3
"""
Test script for video search functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transcript_processor import generate_mock_transcripts
from search_engine import VideoSearchEngine

def test_search_functionality():
    """Test the search functionality with mock data."""
    print("🧪 Testing Video Search Functionality")
    print("=" * 50)
    
    # Initialize components
    print("1. Initializing search engine...")
    search_engine = VideoSearchEngine()
    
    # Load mock data
    print("2. Loading mock transcript data...")
    chunks = generate_mock_transcripts()
    search_engine.add_chunks(chunks)
    
    print(f"✅ Loaded {len(chunks)} chunks from {len(search_engine.get_all_videos())} videos")
    print()
    
    # Test queries
    test_queries = [
        "machine learning",
        "neural networks",
        "natural language processing",
        "linear regression",
        "backpropagation",
        "word embeddings"
    ]
    
    print("3. Running search tests...")
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = search_engine.search(query, top_k=2)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result['video_id']} @ {result['timestamp_formatted']} (score: {result['similarity_score']:.3f})")
        else:
            print("   ❌ No results found")
    
    print("\n4. Testing video-specific search...")
    video_id = "video_001"
    print(f"🔍 Searching within {video_id} for 'regression'")
    results = search_engine.search_by_video(video_id, "regression", top_k=2)
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['video_id']} @ {result['timestamp_formatted']} (score: {result['similarity_score']:.3f})")
    
    print("\n5. Testing video information...")
    for video_id in search_engine.get_all_videos():
        summary = search_engine.get_video_summary(video_id)
        print(f"   📹 {video_id}: {summary['duration_formatted']} ({summary['chunk_count']} chunks)")
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_search_functionality() 