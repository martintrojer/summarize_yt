import argparse
import subprocess


def run_workflow():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="YouTube Transcription Workflow")
    parser.add_argument("--youtube-url", "-y", required=True, help="YouTube video URL")
    parser.add_argument(
        "--model-name", "-m", required=True, help="Model name (e.g. llama3.2:latest)"
    )
    args = parser.parse_args()

    print("Downloading audio from YouTube...")
    result = subprocess.run(
        ["yt-dlp", "--print", "filename", args.youtube_url],
        capture_output=True,
        text=True,
        check=True,
    )
    base_filename = result.stdout.strip().rsplit(".", 1)[0]
    subprocess.run(
        ["yt-dlp", "-x", args.youtube_url],
        check=True,
    )
    audio_filename = f"{base_filename}.opus"

    print("Converting audio to WAV format...")
    wav_filename = f"{base_filename}.wav"
    subprocess.run(
        ["ffmpeg", "-i", audio_filename, "-ar", "16000", wav_filename], check=True
    )

    print("Running Whisper model on audio...")
    subprocess.run(
        [
            "./whisper.cpp/main",
            "-m",
            "whisper.cpp/models/ggml-large-v3-turbo.bin",
            "-nt",
            wav_filename,
        ],
        check=True,
    )

    txt_filename = f"{wav_filename}.txt"
    print("Summarizing transcript using Fabric model...")
    subprocess.run(
        [
            "fabric",
            "-m",
            args.model_name,
            "-p",
            "summarize",
            txt_filename,  # Use the output from last step
        ],
        check=True,
    )


if __name__ == "__main__":
    run_workflow()
