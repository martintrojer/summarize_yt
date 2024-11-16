import argparse
import subprocess
from pathlib import Path


def run_workflow():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="YouTube Transcription Workflow")
    parser.add_argument("--youtube-url", "-y", required=True, help="YouTube video URL")
    parser.add_argument(
        "--model-name", "-m", required=True, help="Model name (e.g. llama3.2:latest)"
    )
    args = parser.parse_args()

    # Initialize filename variables
    audio_filename = wav_filename = temp_dir = None

    try:
        # Create temp directory for files
        temp_dir = Path("temp_downloads")
        temp_dir.mkdir(exist_ok=True)

        print("Downloading audio from YouTube...")
        result = subprocess.run(
            ["yt-dlp", "--print", "filename", "--paths", str(temp_dir), args.youtube_url],
            capture_output=True,
            text=True,
            check=True,
        )
        base_filename = Path(result.stdout.strip()).stem
        subprocess.run(
            ["yt-dlp", "-x", "--paths", str(temp_dir), args.youtube_url],
            check=True,
        )
        
        audio_filename = Path(temp_dir).joinpath(f"{base_filename}.opus")
        wav_filename = Path(temp_dir).joinpath(f"{base_filename}.wav") 
        txt_filename = Path(temp_dir).joinpath(f"{base_filename}.txt")

        print("Converting audio to WAV format...")
        subprocess.run(
            ["ffmpeg", "-i", str(audio_filename), "-ar", "16000", str(wav_filename)], 
            check=True,
            capture_output=True,  # Suppress ffmpeg output
        )

        print("Running Whisper model on audio...")
        subprocess.run(
            [
                "./whisper.cpp/main",
                "-m",
                "whisper.cpp/models/ggml-large-v3-turbo.bin",
                "-nt",
                str(wav_filename),
            ],
            check=True,
        )

        print("Summarizing transcript using Fabric model...")
        subprocess.run(
            [
                "fabric",
                "-m",
                args.model_name,
                "-p",
                "summarize",
                str(txt_filename),
            ],
            check=True,
        )

    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        if e.output:
            print(f"Output: {e.output}")
        raise
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
    finally:
        # Cleanup temporary files
        if audio_filename and audio_filename.exists():
            audio_filename.unlink()
        if wav_filename and wav_filename.exists():
            wav_filename.unlink()
        if temp_dir and temp_dir.exists():
            try:
                temp_dir.rmdir()  # Will only remove if empty
            except OSError:
                pass


if __name__ == "__main__":
    run_workflow()
