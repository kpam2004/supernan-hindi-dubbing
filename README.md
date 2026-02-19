# Supernan Hindi Dubbing Pipeline

Zero-cost Python pipeline: Original video → Hindi dubbed video.

## Pipeline
1. Extract 15-second clip (ffmpeg)
2. Transcribe English (Whisper medium)
3. Translate to Hindi (Helsinki opus-mt)
4. Generate Hindi audio (gTTS)
5. Merge audio + video (ffmpeg)

## Setup
1. Install [ffmpeg](ffmpeg.org/download.html)
2. Click Windows → click Windows builds by BtbN
3. Download `ffmpeg-master-latest-win64-gpl.zip`
4. Extract the zip file
5. Copy the path to the bin folder inside (e.g. C:\ffmpeg\bin)
6. Search Environment Variables in Windows search
7. Click Environment Variables → under System Variables find Path → click Edit
8. Click New → paste C:\ffmpeg\bin → click OK

## Usage
```bash
# 1. Clone the repository
git clone https://github.com/kpam2004/supernan-hindi-dubbing.git
cd supernan-hindi-dubbing

# 2. Install packages:
pip install openai-whisper transformers sentencepiece gtts pydub

# 3. Install ffmpeg.org/download.html
apt-get install ffmpeg

# 3. Run the pipeline:
python dub_video.py supernan_source.mp4 --start 15 --duration 15
```

## Estimated Cost Per Minute of Video (At Scale)
| Step | Time per min video | Cost (50x T4 GPUs @ ₹125/hr) |
|---|---|---|
| Whisper transcription | ~15s | ~₹0.05 |
| opus-mt translation | ~5s | ~₹0.02 |
| gTTS | ~3s | ₹0 |
| ffmpeg merge | ~2s | ₹0 |
| **Total** | **~25s GPU time** | **~₹0.07/min** |

## What I'd improve with more time
- Use Coqui XTTS v2 on Python 3.9 for proper voice cloning
- Fix VideoReTalking face detection for lip-sync
- Use WhisperX for word-level timestamps for better audio alignment
- Use IndicTrans2 instead of opus-mt for more natural Hindi
- Add silence detection to split audio at natural pause points

## Known Limitations
- No voice cloning — gTTS does not clone the original speaker's voice
- No lip-sync — VideoReTalking had face detection issues with this video
- Hindi speech is slightly faster than natural pace due to speed adjustment
- gTTS requires internet connection
