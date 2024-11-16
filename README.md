# YouTube Video Summarizer

A command-line tool that automatically transcribes and summarizes YouTube videos using yt-dlp, Whisper, and Fabric/LLaMA. This tool is particularly useful for videos without available transcripts or when you need quick summaries of video content.

## Features

- Downloads audio from YouTube videos
- Transcribes speech to text using Whisper
- Generates summaries using Fabric/LLaMA models
- Handles temporary file cleanup automatically

## Prerequisites

The following tools need to be installed:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - For YouTube video downloading
- [ffmpeg](https://ffmpeg.org/) - For audio processing
- [Fabric](https://github.com/danielmiessler/fabric) - For text summarization
- [Whisper](https://github.com/ggerganov/whisper.cpp) - For speech-to-text conversion

### Installation

brew install yt-dlp ffmpeg

go install github.com/danielmiessler/fabric@latest

read whisper.cpp/README.md for how to download models

## Usage Examples

### Basic Usage

```bash
# Summarize a single video using llama3.2
python summarize_yt.py -y "https://www.youtube.com/watch?v=dQw
```

### Using a different model

```bash
python summarize_yt.py --youtube-url "https://youtu.be/abc123" --model-name "gpt4:latest"
```

### Command Line Arguments

| Argument | Short | Required | Description |
|----------|--------|----------|-------------|
| `--youtube-url` | `-y` | Yes | The URL of the YouTube video to process |
| `--model-name` | `-m` | Yes | The Fabric/LLaMA model to use for summarization |
