"""Step 3: render slides with Pillow, time them to the voice with ffmpeg, concat to mp4."""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def slide(scene, idx, path):
    img = Image.new("RGB", (W, H), (18, 24, 38))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 24, H], fill=(99, 102, 241))
    y = 260
    for line in textwrap.wrap(scene["headline"], 26):
        d.text((140, y), line, font=font(FONT_BOLD, 96), fill=(255, 255, 255))
        y += 120
    y += 40
    for b in scene.get("bullets", []):
        for j, line in enumerate(textwrap.wrap(b, 55)):
            d.text((140, y), ("• " if j == 0 else "  ") + line, font=font(FONT, 52), fill=(200, 210, 230))
            y += 70
    d.text((W - 160, H - 90), f"{idx + 1}", font=font(FONT, 40), fill=(120, 130, 160))
    img.save(path)


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main(script_path, audio_dir, out):
    data = json.load(open(script_path))
    cdir = os.path.join(os.path.dirname(out) or ".", "clips")
    os.makedirs(cdir, exist_ok=True)
    clips = []
    for i, s in enumerate(data["scenes"]):
        png, mp3, clip = f"{cdir}/{i:02d}.png", f"{audio_dir}/scene_{i:02d}.mp3", f"{cdir}/{i:02d}.mp4"
        slide(s, i, png)
        run(["ffmpeg", "-y", "-loop", "1", "-i", png, "-i", mp3, "-c:v", "libx264", "-tune", "stillimage",
             "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-shortest", clip])
        clips.append(clip)
    with open(f"{cdir}/list.txt", "w") as f:
        f.writelines(f"file '{os.path.abspath(c)}'\n" for c in clips)
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{cdir}/list.txt", "-c", "copy", out])
    print(f"video -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
