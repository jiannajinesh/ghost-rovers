# Ghost Rovers

**NASA Space Apps Challenge 2026 – "Abandoned but not Forgotten"**

Ghost Rovers is a story-driven website for kids aged 10–14. It introduces 20 NASA machines left on the Moon, on Mars and in deep space. Each machine tells its own story in its own voice.

## Features
- 3D Moon and Mars globes with machines at their real landing spots
- 3D solar system for deep-space probes (Dawn, NEAR Shoemaker, Kepler, Pioneer 10 and 11)
- First-person diaries, read aloud with voices that change with each machine's age
- "Why I was sent / What I found / Where I am now" cards and a quiz for every machine
- Timeline of all 20 machines (1967 to today)
- Game: drive the Spirit rover until it gets stuck at Troy, as really happened
- About & Sources page with NASA and NSSDCA links

## How to run
Open `index.html` through any web server (for example GitHub Pages or Netlify).
The 3D views and voices need the page to be served from a web address, not opened as a local file.

## Folders
- `index.html` – the website
- `vendor/` – three.js 3D library (r147)
- `audio/` – voice clips (Kokoro open-source text-to-speech)
- `img/photo/` – real pictures, `img/3d/` – Meshy AI 3D model images, `img/icon/` – small icons
- `build/` – source content (`data.py`) and scripts used to build the page and record the voices

## Use of AI
Claude (Anthropic) helped write code and drafts. Meshy AI made the 3D model images. Voices were made with Kokoro, an open-source text-to-speech model.

## Team
A team of young space explorers, aged 10 to 14, from Kerala, India.
