#!/usr/bin/env python3
"""
Example usage of the Video Search PoC

This script demonstrates how to use the video search system with real videos.
"""

import os
import sys
from transcript_processor import TranscriptProcessor
from search_engine import VideoSearchEngine

def example_with_real_videos():
    """Example of processing real videos and searching through them."""
    print("🎥 Example: Processing Real Videos")
    print("=" * 50)
    
    # Initialize components
    processor = TranscriptProcessor()
    search_engine = VideoSearchEngine()
    
    # Example video files (you would replace these with actual video paths)
    video_files = [
        # ("path/to/video1.mp4", "video_001"),
        # ("path/to/video2.mp4", "video_002"),
        # ("path/to/video3.mp4", "video_003"),
    ]
    
    print("📝 Processing videos...")
    for video_path, video_id in video_files:
        if os.path.exists(video_path):
            print(f"Processing {video_id}...")
            chunks = processor.process_video(video_path, video_id)
            search_engine.add_chunks(chunks)
            print(f"✅ Added {len(chunks)} chunks from {video_id}")
        else:
            print(f"⚠️  Video file not found: {video_path}")
    
    # Example searches
    example_queries = [
        "machine learning algorithms",
        "neural network training",
        "data preprocessing",
        "model evaluation",
        "hyperparameter tuning"
    ]
    
    print("\n🔍 Example searches:")
    for query in example_queries:
        print(f"\nQuery: '{query}'")
        results = search_engine.search(query, top_k=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['video_id']} @ {result['timestamp_formatted']} (score: {result['similarity_score']:.3f})")
        else:
            print("  No results found")

def example_with_mock_data():
    """Example using the mock data for demonstration."""
    print("\n🧪 Example: Using Mock Data")
    print("=" * 50)
    
    from transcript_processor import generate_mock_transcripts
    
    # Initialize components
    search_engine = VideoSearchEngine()
    
    # Load mock data
    print("📝 Loading mock transcript data...")
    chunks = generate_mock_transcripts()
    search_engine.add_chunks(chunks)
    
    print(f"✅ Loaded {len(chunks)} chunks from {len(search_engine.get_all_videos())} videos")
    
    # Example searches
    queries = [
        "machine learning basics",
        "deep learning fundamentals", 
        "natural language processing",
        "regression algorithms",
        "neural network structure"
    ]
    
    print("\n🔍 Search results:")
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_engine.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['video_id']} @ {result['timestamp_formatted']}")
            print(f"     Score: {result['similarity_score']:.3f}")
            print(f"     Text: {result['text'][:80]}...")

def example_video_specific_search():
    """Example of searching within a specific video."""
    print("\n🎯 Example: Video-Specific Search")
    print("=" * 50)
    
    from transcript_processor import generate_mock_transcripts
    
    # Initialize components
    search_engine = VideoSearchEngine()
    chunks = generate_mock_transcripts()
    search_engine.add_chunks(chunks)
    
    # Search within a specific video
    video_id = "video_001"
    query = "regression"
    
    print(f"🔍 Searching for '{query}' within {video_id}")
    results = search_engine.search_by_video(video_id, query, top_k=3)
    
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['video_id']} @ {result['timestamp_formatted']}")
        print(f"     Score: {result['similarity_score']:.3f}")
        print(f"     Text: {result['text']}")

def example_batch_processing():
    """Example of batch processing multiple videos."""
    print("\n📦 Example: Batch Processing")
    print("=" * 50)
    
    # Initialize components
    processor = TranscriptProcessor()
    search_engine = VideoSearchEngine()
    
    # Example batch processing
    video_batch = [
        ("video_001", "Machine Learning Tutorial"),
        ("video_002", "Deep Learning Fundamentals"),
        ("video_003", "NLP Basics")
    ]
    
    print("📝 Batch processing videos...")
    for video_id, title in video_batch:
        print(f"Processing {video_id}: {title}")
        # In real usage, you would process actual video files here
        # chunks = processor.process_video(f"videos/{video_id}.mp4", video_id)
        # search_engine.add_chunks(chunks)
    
    print("✅ Batch processing completed")
    
    # Show video summaries
    print("\n📊 Video summaries:")
    for video_id in search_engine.get_all_videos():
        summary = search_engine.get_video_summary(video_id)
        print(f"  📹 {video_id}: {summary['duration_formatted']} ({summary['chunk_count']} chunks)")

def main():
    """Run all examples."""
    print("🚀 Video Search PoC - Usage Examples")
    print("=" * 60)
    
    # Run examples
    example_with_mock_data()
    example_video_specific_search()
    example_batch_processing()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("\nTo use with real videos:")
    print("1. Place your video files in a directory")
    print("2. Update the video_files list in example_with_real_videos()")
    print("3. Run the example function")
    print("\nFor interactive usage, run: python main.py")

if __name__ == "__main__":
    main() 