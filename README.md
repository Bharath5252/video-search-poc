# Video Search PoC - Transcript-based Semantic Search

A Python proof-of-concept for video search using transcript-based semantic similarity. This project demonstrates how to build a video search engine that can find specific content within videos using natural language queries.

## Features

- 🎥 **Video Transcription**: Uses OpenAI Whisper for accurate speech-to-text conversion
- 📝 **Smart Chunking**: Segments transcripts into ~30-second chunks with timestamps
- 🔍 **Semantic Search**: Uses sentence transformers for semantic similarity matching
- ⚡ **Fast Search**: FAISS index for efficient similarity search
- 🎯 **Precise Results**: Returns exact video timestamps for matched content
- 🧪 **Mock Data**: Includes sample transcripts for immediate testing

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Video Files   │───▶│  Whisper Model   │───▶│  Transcripts    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Search Query   │───▶│ Sentence Encoder │───▶│  FAISS Index    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Search Results │◀───│  Similarity      │◀───│  Chunk          │
│  (Video + Time) │    │  Matching        │    │  Embeddings     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd video_search_poc
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python main.py demo
   ```

## Usage

### Interactive Mode

Run the main application for an interactive experience:

```bash
python main.py
```

**Available Commands:**
- `search <query>` - Search for content across all videos
- `video <video_id>` - Show information about a specific video
- `list` - List all available videos
- `help` - Show help message
- `quit` - Exit the application

### Demo Mode

Run a quick demonstration with predefined queries:

```bash
python main.py demo
```

### Programmatic Usage

```python
from transcript_processor import TranscriptProcessor, generate_mock_transcripts
from search_engine import VideoSearchEngine

# Initialize components
processor = TranscriptProcessor()
search_engine = VideoSearchEngine()

# Load mock data (or process real videos)
chunks = generate_mock_transcripts()
search_engine.add_chunks(chunks)

# Search for content
results = search_engine.search("machine learning algorithms")
for result in results:
    print(f"Video: {result['video_id']}")
    print(f"Timestamp: {result['timestamp_formatted']}")
    print(f"Text: {result['text']}")
```

## Processing Real Videos

To process your own videos, use the `TranscriptProcessor`:

```python
# Process a single video
processor = TranscriptProcessor()
chunks = processor.process_video("path/to/video.mp4", "video_001")

# Add to search engine
search_engine = VideoSearchEngine()
search_engine.add_chunks(chunks)
```

## Mock Data

The demo includes 3 sample videos with educational content:

1. **video_001**: Machine Learning Basics
   - Linear regression
   - Classification problems
   - Logistic regression

2. **video_002**: Deep Learning Fundamentals
   - Neural network structure
   - Backpropagation
   - Training algorithms

3. **video_003**: Natural Language Processing
   - NLP techniques
   - Word embeddings
   - Model deployment

## Technical Details

### Components

- **`transcript_processor.py`**: Handles video transcription, chunking, and embedding generation
- **`search_engine.py`**: Manages FAISS index and similarity search
- **`main.py`**: CLI interface and demo functionality

### Models Used

- **Whisper**: OpenAI's speech recognition model for transcription
- **all-MiniLM-L6-v2**: Sentence transformer for semantic embeddings
- **FAISS**: Facebook's similarity search library

### Data Structures

```python
@dataclass
class TranscriptChunk:
    video_id: str
    start_time: float
    end_time: float
    text: str
    embedding: np.ndarray = None
```

## Performance Considerations

- **Memory**: FAISS index stores embeddings in memory for fast access
- **Scalability**: For large video collections, consider using pgvector with PostgreSQL
- **Accuracy**: Whisper model quality depends on audio clarity and language
- **Speed**: Search time scales with the number of chunks in the index

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Video thumbnail generation
- [ ] Web interface with video player integration
- [ ] Advanced filtering (duration, date, speaker)
- [ ] Real-time transcription for live videos
- [ ] Integration with video hosting platforms

## Troubleshooting

### Common Issues

1. **Whisper model download fails:**
   ```bash
   # Clear cache and retry
   rm -rf ~/.cache/whisper
   python main.py
   ```

2. **FAISS installation issues:**
   ```bash
   # Try CPU-only version
   pip install faiss-cpu
   ```

3. **Memory issues with large videos:**
   - Reduce chunk duration
   - Process videos in batches
   - Use disk-based storage for embeddings

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to submit issues and enhancement requests! 