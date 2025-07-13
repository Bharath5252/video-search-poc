#!/usr/bin/env python3
"""
Video Search PoC - Main Application

This script demonstrates video search using transcript-based semantic similarity.
It uses mock data for demonstration purposes.
"""

import sys
import json
from transcript_processor import generate_mock_transcripts
from search_engine import VideoSearchEngine

def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("🎥 VIDEO SEARCH PoC - Transcript-based Semantic Search")
    print("=" * 60)
    print()

def print_help():
    """Print help information."""
    print("Available commands:")
    print("  search <query>     - Search for content across all videos")
    print("  video <video_id>   - Show information about a specific video")
    print("  list               - List all available videos")
    print("  help               - Show this help message")
    print("  quit               - Exit the application")
    print()

def print_search_results(results):
    """Print search results in a formatted way."""
    if not results:
        print("❌ No results found.")
        return
    
    print(f"🔍 Found {len(results)} result(s):")
    print("-" * 60)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. Video: {result['video_id']}")
        print(f"   📍 Timestamp: {result['timestamp_formatted']}")
        print(f"   📊 Similarity: {result['similarity_score']:.3f}")
        print(f"   📝 Text: {result['text'][:100]}{'...' if len(result['text']) > 100 else ''}")
        print()

def print_video_info(video_id, summary, chunks):
    """Print detailed information about a video."""
    print(f"📹 Video: {video_id}")
    print(f"⏱️  Duration: {summary['duration_formatted']}")
    print(f"📦 Chunks: {summary['chunk_count']}")
    print("-" * 60)
    
    for i, chunk in enumerate(chunks, 1):
        print(f"{i}. [{chunk['timestamp_formatted']}] {chunk['text']}")
    print()

def main():
    """Main application loop."""
    print_banner()
    
    # Initialize the search engine with mock data
    print("🚀 Initializing video search engine...")
    search_engine = VideoSearchEngine()
    
    # Generate mock transcript data
    print("📝 Loading mock transcript data...")
    chunks = generate_mock_transcripts()
    search_engine.add_chunks(chunks)
    
    print(f"✅ Loaded {len(chunks)} transcript chunks from {len(search_engine.get_all_videos())} videos")
    print()
    
    # Main interaction loop
    while True:
        try:
            command = input("🎯 Enter command (or 'help'): ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("👋 Goodbye!")
                break
            elif command == "help":
                print_help()
            elif command == "list":
                videos = search_engine.get_all_videos()
                print(f"📚 Available videos ({len(videos)}):")
                for video_id in videos:
                    summary = search_engine.get_video_summary(video_id)
                    print(f"  • {video_id} ({summary['duration_formatted']})")
                print()
            elif command.startswith("video "):
                parts = command.split(" ", 1)
                if len(parts) == 2:
                    video_id = parts[1]
                    summary = search_engine.get_video_summary(video_id)
                    if summary:
                        video_chunks = [chunk for chunk in chunks if chunk.video_id == video_id]
                        chunk_data = []
                        for chunk in video_chunks:
                            chunk_data.append({
                                'timestamp_formatted': search_engine._format_timestamp(chunk.start_time),
                                'text': chunk.text
                            })
                        print_video_info(video_id, summary, chunk_data)
                    else:
                        print(f"❌ Video '{video_id}' not found.")
                else:
                    print("❌ Usage: video <video_id>")
            elif command.startswith("search "):
                parts = command.split(" ", 1)
                if len(parts) == 2:
                    query = parts[1]
                    print(f"🔍 Searching for: '{query}'")
                    results = search_engine.search(query, top_k=5)
                    print_search_results(results)
                else:
                    print("❌ Usage: search <query>")
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_search():
    """Run a quick demo of the search functionality."""
    print("🚀 Running demo search...")
    
    # Initialize search engine
    search_engine = VideoSearchEngine()
    chunks = generate_mock_transcripts()
    search_engine.add_chunks(chunks)
    
    # Demo queries
    demo_queries = [
        "machine learning algorithms",
        "neural networks and deep learning",
        "natural language processing",
        "linear regression",
        "backpropagation training"
    ]
    
    for query in demo_queries:
        print(f"\n🔍 Query: '{query}'")
        results = search_engine.search(query, top_k=3)
        print_search_results(results)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_search()
    else:
        main() 