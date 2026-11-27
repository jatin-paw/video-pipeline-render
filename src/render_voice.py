"""Step 2: text-to-speech per scene with edge-tts (free, no API key)."""
import asyncio, json, os, sys
import edge_tts

VOICE = os.environ.get("TTS_VOICE", "en-US-AndrewNeural")


async def run(script_path: str, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)
    scenes = json.load(open(script_path))["scenes"]
    for i, s in enumerate(scenes):
        await edge_tts.Communicate(s["narration"], VOICE).save(f"{outdir}/scene_{i:02d}.mp3")
    print(f"voice: {len(scenes)} clips -> {outdir}")


if __name__ == "__main__":
    asyncio.run(run(sys.argv[1] if len(sys.argv) > 1 else "build/script.json",
                    sys.argv[2] if len(sys.argv) > 2 else "build/audio"))
