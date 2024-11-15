A simple script that stitches together yt-dlp, whisper and fabric/llama.

This is useful for youtube videos without a transcript.

I most cases `fabric -y` is enough. Which means you don't need whisper and ffmpeg.

## Install stuff

brew install yt-dlp
brew install ffmpeg

go install github.com/danielmiessler/fabric@latest

read whisper.cpp/README.md for how to download models
