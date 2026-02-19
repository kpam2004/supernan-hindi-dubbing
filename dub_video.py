import os, subprocess, whisper
from gtts import gTTS
from pydub import AudioSegment
from transformers import MarianMTModel, MarianTokenizer

def extract_segment(input_video, output_dir, start=15, duration=15):
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(
        f"ffmpeg -y -ss {start} -i {input_video} -t {duration} "
        f"-c:v libx264 -crf 18 -preset fast -c:a aac {output_dir}/clip.mp4",
        shell=True, check=True, capture_output=True)
    subprocess.run(
        f"ffmpeg -y -i {output_dir}/clip.mp4 -ar 16000 -ac 1 -vn {output_dir}/clip.wav",
        shell=True, check=True, capture_output=True)
    return {"video": f"{output_dir}/clip.mp4", "audio": f"{output_dir}/clip.wav"}

def transcribe(audio_path, model_size="medium"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language="en")
    return result["text"].strip()

def translate_to_hindi(text):
    tok = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
    mt = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
    batch = tok([text], return_tensors="pt", padding=True, truncation=True, max_length=512)
    out = mt.generate(**batch)
    return tok.decode(out[0], skip_special_tokens=True)

def generate_hindi_audio(hindi_text, output_path):
    gTTS(text=hindi_text, lang="hi", slow=False).save(output_path.replace(".wav", ".mp3"))
    subprocess.run(
        f"ffmpeg -y -i {output_path.replace('.wav','.mp3')} -ar 16000 -ac 1 {output_path}",
        shell=True, check=True, capture_output=True)
    return output_path

def adjust_speed(audio_path, target_duration):
    dur = len(AudioSegment.from_wav(audio_path)) / 1000.0
    factor = dur / target_duration
    out = audio_path.replace(".wav", "_adj.wav")
    subprocess.run(
        f"ffmpeg -y -i {audio_path} -filter:a \"atempo={factor:.4f}\" {out}",
        shell=True, check=True, capture_output=True)
    return out

def merge_audio_video(video, audio, output):
    subprocess.run(
        f"ffmpeg -y -i {video} -i {audio} -map 0:v -map 1:a -c:v copy -shortest {output}",
        shell=True, check=True, capture_output=True)
    return output

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("input_video")
    p.add_argument("--start", type=float, default=15)
    p.add_argument("--duration", type=float, default=15)
    p.add_argument("--output-dir", default="output")
    args = p.parse_args()

    print("[1/5] Extracting clip...")
    paths = extract_segment(args.input_video, args.output_dir, args.start, args.duration)
    print("[2/5] Transcribing...")
    english = transcribe(paths["audio"])
    print(f"  English: {english}")
    print("[3/5] Translating...")
    hindi = translate_to_hindi(english)
    print(f"  Hindi: {hindi}")
    print("[4/5] Generating Hindi audio...")
    wav = generate_hindi_audio(hindi, f"{args.output_dir}/hindi_speech.wav")
    adj = adjust_speed(wav, args.duration)
    print("[5/5] Merging...")
    final = merge_audio_video(paths["video"], adj, f"{args.output_dir}/final_hindi_dubbed.mp4")
    print(f"Done! {final}")
