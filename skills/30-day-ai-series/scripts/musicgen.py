"""Generate a music bed locally with MusicGen. Usage: musicgen.py OUT.wav SECONDS "prompt" [seed]"""
import sys, torch, numpy as np, soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration

out, seconds, prompt = sys.argv[1], float(sys.argv[2]), sys.argv[3]
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 7
torch.manual_seed(seed)
device = "mps" if torch.backends.mps.is_available() else "cpu"
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)
inputs = proc(text=[prompt], padding=True, return_tensors="pt").to(device)
tokens = int(min(seconds, 29) * 50)
audio = model.generate(**inputs, max_new_tokens=tokens, do_sample=True, guidance_scale=3.0)
sr = model.config.audio_encoder.sampling_rate
sf.write(out, audio[0, 0].float().cpu().numpy(), sr)
print("wrote", out, sr)
