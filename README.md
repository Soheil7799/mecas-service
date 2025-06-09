# <ins>Me</ins>dia <ins>C</ins>onversion <ins>a</ins>nd <ins>S</ins>treaming Service (MECAS)

MECAS is a web service for uploading, processing, and streaming audio/video files with customizable filters.  
Final Project for the course "Music and multimedia streaming over the Internet".

## 🎯 Project Overview

This project implements a full-stack web service that allows users to:

1. **Upload Video Files**: Support for MP4, AVI, and MOV formats (up to 200MB)
2. **Configure Audio and Video Filters**: Interactive web interface for filter selection and parameter adjustment
3. **Apply Advanced Processing**: Real-time application of selected filters to uploaded content
4. **Stream Processed Media**: Direct browser streaming of the processed video with applied filters

The system combines Python-based audio processing with FFmpeg-powered video processing to deliver a comprehensive media manipulation platform.

## ✨ Features

### 🎵 Audio Filters (Python Implementation)

- **Gain Compression**✅: Dynamic range compression with configurable thresholds and ratios  
- **Voice Enhancement**⏳: Pre-emphasis filtering combined with band-pass filtering for vocal clarity
- **Noise Reduction with Delay**⏳: Wiener filter-based noise reduction with configurable delay effects
- **Phone-like Filter**⏳: Mono enhancement with band-pass filtering to simulate telephone audio
- **Car Audio Effect**⏳: Stereo enhancement with low-pass filtering for automotive audio simulation

### 🎬 Video Filters (FFmpeg Implementation)

- **Grayscale Conversion**✅: Convert color video to monochrome
- **Color Inversion**✅: Invert all colors in the video for artistic effects
- **Frame Interpolation**✅: Increase frame rate through advanced motion interpolation
- **Upscaling**✅: Enhance video resolution with configurable target dimensions

### 🌐 Web Interface

- **Drag & Drop Upload**: Intuitive file upload with visual feedback
- **Real-time Parameter Control**: Interactive sliders and inputs for filter configuration
- **Live Preview**: Immediate streaming of processed content
- **Modern UI**: Dark theme with Catppuccin Mocha color scheme

## 🛠 Technology Stack

### Backend

- **Framework**: FastAPI (Python 3.13)
- **Audio Processing**: SciPy, NumPy with custom algorithm implementations
- **Video Processing**: FFmpeg for professional-grade video manipulation
- **API Architecture**: RESTful endpoints with comprehensive error handling

### Frontend

- **Core Technologies**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Custom responsive design with modern CSS features
- **Media Handling**: HTML5 video player with streaming support

### Infrastructure

- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for development
- **CI/CD**: GitHub Actions with AWS ECR integration
- **Deployment**: EC2 with automated container management

## 📋 Prerequisites

- Docker and Docker Compose (Newer versions of Docker come with `docker compose` integrated)
- Python 3.13+ (for local development)
- FFmpeg (automatically included in Docker container)
- Git for version control

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
    
    ```bash
    git clone https://github.com/Soheil7799/mecas-service.git
    cd mecas-service
    ```
    
2. **Start the service**
    
    ```bash
    docker-compose up --build
    ```
    
3. **Access the application**
    
    - Open your browser and navigate to `http://localhost:8000`
    - The web interface will be ready for file uploads and processing

### Local Development Setup
1.  **Create virtual environment for this project**
	```
	python -m venv .venv
	source .venv/bin/activate 
	```
2. **Install Python dependencies**
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. **Install FFmpeg**
    
    ```bash
    # Ubuntu/Debian
    sudo apt update && sudo apt install ffmpeg
    
    # macOS
    brew install ffmpeg
    
    # Windows
    # Download from https://ffmpeg.org/download.html
    ```
    
4. **Run the development server**
    
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    

## 📖 Usage Guide

### 1. Upload a Video File

- Click the upload area or drag and drop a video file
- Supported formats: MP4, AVI, MOV (max 200MB)
- Wait for the upload confirmation

### 2. Configure Filters

#### Audio Filters

- **Gain Compressor**: Set compressor and limiter thresholds
- **Voice Enhancement**: Adjust pre-emphasis and high-pass filter parameters
- **Denoise + Delay**: Configure noise power and delay settings
- **Phone-like Filter**: Set side gain and filter order
- **Car-like Filter**: Adjust stereo enhancement parameters

#### Video Filters

- **Grayscale**: Simple toggle activation
- **Color Invert**: Simple toggle activation
- **Frame Interpolation**: Set target FPS (recommended: 60)
- **Upscale**: Define target resolution (width × height)

### 3. Apply Processing

- Click "Apply Filters" to start processing
- Monitor progress through status messages
- Processing time varies based on file size and selected filters

### 4. Stream Results

- Processed video automatically appears in the player
- Use standard video controls for playback
- Full-screen viewing supported

### 5. Cleanup

- Use "Delete File" to remove uploaded content and reset the interface

## 🏗 Project Structure

```
mecas-service/
├── 📁 api/                     # FastAPI application structure
│   ├── 📁 routers/            # API endpoint definitions
│   │   ├── filters.py         # Filter application logic
│   │   ├── stream.py          # Video streaming endpoints
│   │   └── upload.py          # File upload handling
│   └── api.py                 # Router aggregation
├── 📁 filters/                # Processing algorithms
│   ├── 📁 audio/             # Python-based audio filters
│   │   ├── gain_compression.py
│   │   ├── voice_enhancement.py
│   │   ├── denoise_delay.py
│   │   ├── phone_like.py
│   │   └── car_like.py
│   ├── 📁 video/             # FFmpeg video processing
│   │   └── video_filter_manager.py
│   └── utilities.py          # Audio/video separation and merging
├── 📁 formatings/            # Pydantic data models
│   ├── audio.py              # Audio filter schemas
│   ├── video.py              # Video filter schemas
│   └── file.py               # File handling schemas
├── 📁 frontend/              # Web interface
│   ├── index.html            # Main application page
│   ├── styles.css            # Catppuccin-themed styling
│   └── script.js             # Client-side application logic
├── 📁 Dockerfiles/          # Container definitions
├── 📁 .github/workflows/    # CI/CD automation
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Development orchestration
└── README.md                # Project documentation
```

## 🔧 API Endpoints

### File Management

- `POST /uploadfile/` - Upload video files with validation
- `DELETE /{filename}` - Remove specific uploaded files
- `DELETE /` - Clear all uploaded content

### Filter Processing

- `POST /application` - Apply configured filters to uploaded media

### Media Streaming

- `GET /stream/` - Stream processed video with appropriate MIME types

### Static Assets

- `GET /` - Serve main web interface
- `GET /static/*` - Serve CSS, JavaScript, and other assets

## 🔬 Filter Implementation Details

### Audio Processing Pipeline

1. **Audio Extraction**: FFmpeg separates audio track to WAV format
2. **Python Processing**: Custom algorithms process audio data
3. **Format Conversion**: Processed audio converted to AAC for web compatibility

### Video Processing Pipeline

1. **Video Isolation**: Original video copied to temporary workspace
2. **FFmpeg Filtering**: Professional video filters applied in sequence
3. **Output Optimization**: Processed video optimized for web streaming

### Merging Process

- **Synchronization**: Audio and video tracks precisely synchronized
- **Encoding**: Final output optimized for web delivery
- **Quality Preservation**: Maintains highest possible quality throughout pipeline

## 🚢 Deployment

### AWS Deployment (Production)

The project includes automated deployment to AWS using:

- **ECR**: Container image registry
- **EC2**: Application hosting
- **GitHub Actions**: Automated CI/CD pipeline

### Manual Deployment

1. Build the Docker image
2. Push to your container registry
3. Deploy to your cloud provider
4. Configure environment variables and secrets

## 🧪 Development
### Code Structure

- **Modular Design**: Separated concerns for audio, video, and web handling
- **Type Safety**: Comprehensive Pydantic models for data validation
- **Error Handling**: Robust error management throughout the pipeline
- **Logging**: Detailed logging for debugging and monitoring

### Adding New Filters

1. Implement filter logic in appropriate directory (`filters/audio/` or `filters/video/`)
2. Add Pydantic models in `formatings/`
3. Update API endpoints in `api/routers/`
4. Extend frontend interface in `frontend/`

## 🚀 Future Plans & Roadmap

### 🔄 Major Refactoring (v2.0)

- **Language Migration**: Complete rewrite from Python to **Go** for improved performance, better concurrency handling, and reduced memory footprint
- **Enhanced Architecture**: Implement clean architecture patterns with proper dependency injection and improved testability

### 🛣️ API Improvements

- **RESTful Route Structure**: Redesign API endpoints following REST conventions more strictly
    - `/api/v1/media/{id}/filters` - Apply filters to specific media
    - `/api/v1/media/{id}/stream` - Stream processed media
    - `/api/v1/filters/audio` - List available audio filters
    - `/api/v1/filters/video` - List available video filters
- **Rate Limiting**: Implement proper rate limiting and request throttling

### 🎵 Audio Filter Expansion

Complete the missing audio filter implementations:

- **Voice Enhancement**: Advanced pre-emphasis and band-pass filtering algorithms
- **Denoise & Delay**: Wiener filter implementation with configurable delay effects
- **Phone-like Filter**: Telecommunications audio simulation with mono enhancement
- **Car Audio Effect**: Automotive audio processing with stereo field manipulation


### 🗄️ Database Integration

- **PostgreSQL Database**: Add persistent data storage for:
    - **User Management**: User accounts, profiles, and preferences
    - **Media Metadata**: File information, processing history, and filter configurations
    - **Processing Jobs**: Job queues, status tracking, and processing logs
    - **Analytics**: Usage statistics, popular filters, and performance metrics
    - **Presets**: Save and share custom filter combinations
- **Use Cases**:
    - **User Sessions**: Persistent login and personalized experience
    - **File Management**: Track uploaded files across sessions with metadata
    - **Processing History**: View previously processed files and reapply configurations
    - **Collaboration**: Share filter presets and processed videos with other users
    - **Analytics Dashboard**: Monitor system usage and optimize performance
    - **Audit Trail**: Complete logging of all processing operations for debugging

### 🐳 Deployment Modernization

- **Docker Compose Production**: Replace single-container deployment with multi-service architecture
    - Separate services for API, audio processing, video processing, and database
    - Redis for caching and job queuing
    - PostgreSQL for metadata and user management
    - MinIO for object storage (alternative to local file system)
- **Load Balancing**: Implement proper load balancing for horizontal scaling

### 🔧 Technical Improvements

- **Microservices Architecture**: Split into dedicated services (upload, processing, streaming, API gateway)
- **Message Queues**: Add RabbitMQ or Apache Kafka for reliable job processing
- **Monitoring**: Integrate Prometheus metrics and Grafana dashboards

### 🔒 Security & Scalability

- **Authentication**: JWT-based user authentication and authorization
- **Resource Limits**: Implement proper resource quotas and processing timeouts
- **Multi-tenancy**: Support for multiple users with isolated processing environments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-filter`)
3. Commit your changes (`git commit -m 'Add amazing filter'`)
4. Push to the branch (`git push origin feature/amazing-filter`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Mostafa Shirvani**

- Final Project for "Music and multimedia streaming over the Internet"

---
**MECAS** - Transforming media processing with modern web technologies 🎬✨