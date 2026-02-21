# Supernan Hindi Dubbing Pipeline

<div align='center'>
  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpam2004/supernan-hindi-dubbing/blob/main/supernan_hindi_dubbing.ipynb)
[![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/kpamnani783/supernan-hindi-dubbing)

</div>
Zero-cost Python pipeline: Original video → Hindi dubbed video.

## Pipeline
1. Extract 15-second clip (ffmpeg)
2. Transcribe English (Whisper medium)
3. Translate to Hindi (Helsinki opus-mt)
4. Generate Hindi audio (gTTS)
5. Merge audio + video (ffmpeg)

---

## Setup

### Install FFmpeg (Required)

1. Install https://ffmpeg.org/download.html
2. Click Windows → Windows builds by BtbN
3. Download `ffmpeg-master-latest-win64-gpl.zip`
4. Extract the zip file
5. Copy the path to the bin folder inside (e.g. C:\ffmpeg\bin)
6. Search Environment Variables in Windows search
7. Click Environment Variables → under System Variables find Path → click Edit
8. Click New → paste C:\ffmpeg\bin → click OK

Verify installation:

```
ffmpeg -version
```
## Usage
[1. Run Locally](#Run-Locally)
[2. Run on Google Colab](#Run-on-Google-Colab)
[3. Run on Kaggle](#Run-on-Kaggle)
### Run Locally

Step 1 - Clone the repository
```
git clone https://github.com/kpam2004/supernan-hindi-dubbing.git
cd supernan-hindi-dubbing
```
Step 2 - Install required Python libraries
```
pip install openai-whisper transformers sentencepiece gtts pydub torch
```
Step 3 - Make sure Python is installed
```
python --version
```

If not installed, download from:
https://www.python.org/downloads/

Step 4 - Run the Python script
```
python dub_video.py supernan_source.mp4
```
Step 5 - Run with custom parameters
```
python dub_video.py supernan_source.mp4 --start 10 --duration 20 --output-dir output
```

Parameters:

`--start` → start time of clip (seconds)

`--duration` → clip length

`--output-dir` → output folder

Step 6 - Expected Output
```
[1/5] Extracting clip...
[2/5] Transcribing...
English: ...
[3/5] Translating...
Hindi: ...
[4/5] Generating Hindi audio...
[5/5] Merging...
Done! output/final_hindi_dubbed.mp4
```

Final video location:
```
output/final_hindi_dubbed.mp4
```

<div align='center'><b> OR </b></div>

### Run on Google Colab

Step 1 - Open Google Colab
1. Go to: https://colab.research.google.com/
2. Sign in with your Google account.

Step 2 - Upload the notebook
1. Click **File → Upload notebook**
2. Select:`supernan_hindi_dubbing.ipynb`

Step 3 - Enable GPU (recommended for Whisper)
1. Click **Runtime → Change runtime type**
2. Hardware accelerator → select **T4 GPU**
3. Click **Save**

Step 4 - Run the Cell

<div align='center'><b> OR </b></div>

### Run on Kaggle

Step 1 - Open Kaggle
1. Go to: https://www.kaggle.com/code
2. Login → Click **New Notebook**

Step 2 - Upload project files
1. Left panel → **Add data → Upload**
2. Upload: `supernan_hindi_dubbing.ipynb`

Step 3 - Enable GPU (recommended for Whisper)
1. Click **Settings (right panel)**
2. Accelerator → select **GPU T4 x2**
3. Save

Step 4 - Run the Cell

## Common Errors & Fix

Module not found - `pip install <module_name>`

ffmpeg not recognized - Install FFmpeg and restart terminal.

python not recognized - Reinstall Python and select Add Python to PATH.

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
- No voice cloning - gTTS does not clone the original speaker's voice
- No lip-sync - VideoReTalking had face detection issues with this video
- Hindi speech is slightly faster than natural pace due to speed adjustment
- gTTS requires internet connection
