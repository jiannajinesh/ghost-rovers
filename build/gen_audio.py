import os, re, sys, json, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from data import GHOSTS, HOSTS, HOST_VOICE, SPIRIT_VOICE, GAME, STORY, MISC
from kokoro_onnx import Kokoro
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "audio"); os.makedirs(OUT, exist_ok=True)
k = Kokoro("/home/claude/tts/kokoro-v1.0.int8.onnx", "/home/claude/tts/voices-v1.0.bin")
KEEP_CAPS = {"NASA", "ALSEP", "U.S.", "US", "NEAR", "AND", "CAN", "FIRST"}

def clean(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("km/h", "kilometres an hour").replace("1/6", "one sixth").replace("%", " percent")
    t = t.replace("3.8 cm", "3.8 centimetres").replace("21.5 kg", "21.5 kilograms").replace("10.6 kg", "10.6 kilograms")
    def low(m):
        w = m.group(0)
        if w in ("NASA", "ALSEP", "NEAR"):
            return w
        return w.lower()
    t = re.sub(r"\b[A-Z]{3,}\b", low, t)
    t = t.replace("Shhh", "Shh").replace("Ahem.", "Ahem,")
    return re.sub(r"\s+", " ", t).strip()

def era(year):
    if year is None: return "host"
    if year < 1980: return "old"
    if year < 2010: return "mid"
    return "new"

FX = {
 "old": ("asetrate=24000*0.965,aresample=24000,atempo=1.036,highpass=f=300,lowpass=f=3300,"
         "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,volume=1.6", 0.010),
 "mid": ("highpass=f=140,lowpass=f=6500,acompressor=threshold=-20dB:ratio=2.5,volume=1.25", 0.003),
 "new": ("highpass=f=70,acompressor=threshold=-20dB:ratio=2,volume=1.15", 0.0),
 "host": ("highpass=f=60,acompressor=threshold=-20dB:ratio=2,volume=1.15", 0.0),
}

def render(name, text, voice, speed, year=None):
    out = os.path.join(OUT, name + ".mp3")
    if os.path.exists(out):
        return out
    lang = "en-gb" if voice.startswith("b") else "en-us"
    s, sr = k.create(clean(text), voice=voice, speed=speed, lang=lang)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, s, sr); wav = f.name
    chain, hiss = FX[era(year)]
    if hiss > 0:
        fc = (f"[0:a]{chain}[v];[1:a]highpass=f=1500,lowpass=f=6000,volume={hiss*40}[n];"
              f"[v][n]amix=inputs=2:duration=first:normalize=0[m]")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-f", "lavfi", "-i",
               f"anoisesrc=color=pink:amplitude=0.05:r={sr}", "-filter_complex", fc, "-map", "[m]"]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", chain]
    cmd += ["-ac", "1", "-ar", "24000", "-b:a", "48k", out]
    subprocess.run(cmd, check=True); os.unlink(wav)
    print("ok", name, flush=True)
    return out

for g in GHOSTS:
    render("diary_" + g["id"], g["diary"], g["voice"], g["spd"], g["year"])
for w, lines in HOSTS.items():
    v, sp = HOST_VOICE[w]
    for i, t in enumerate(lines):
        render(f"host_{w}_{i}", t, v, sp)
for key, t in GAME.items():
    render("game_" + key, t, SPIRIT_VOICE[0], SPIRIT_VOICE[1], 2004)
for i, t in enumerate(STORY):
    render(f"story_{i}", t, SPIRIT_VOICE[0], SPIRIT_VOICE[1], 2004)
for key, (v, sp, t) in MISC.items():
    render("misc_" + key, t, v, sp)
print("DONE")
