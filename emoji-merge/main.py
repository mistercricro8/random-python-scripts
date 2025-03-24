import os
import requests
from PIL import Image
from io import BytesIO


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def draw_grid(rows, cols, current_index, emojis):
    for row in range(rows):
        line = []
        for col in range(cols):
            index = row * cols + col
            if index == current_index:
                line.append("[*]")
            elif index < len(emojis):
                line.append("[X]" if emojis[index] else "[ ]")
            else:
                line.append("[ ]")
        print(" ".join(line))


def download_image(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        return img
    except Exception as e:
        print(f"Error w {url}: {str(e)}")
        return None


def main():
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    total = rows * cols

    emojis = []
    for i in range(total):
        clear_screen()
        draw_grid(rows, cols, i, emojis)
        url = input(f"\nURL for pos ({i//cols}, {i%cols}): ").strip()
        emojis.append(url if url else None)

    images = []
    for url in emojis:
        images.append(download_image(url) if url else None)

    base_size = next((img.size for img in images if img), (48, 48))

    merged = Image.new("RGBA", (base_size[0] * cols, base_size[1] * rows))
    for i, img in enumerate(images):
        if img is None:
            img = Image.new("RGBA", base_size, (0, 0, 0, 0))
        else:
            img = img.resize(base_size)

        x = (i % cols) * base_size[0]
        y = (i // cols) * base_size[1]
        merged.paste(img, (x, y), img)

    os.makedirs("merged", exist_ok=True)
    merged.save("merged/merged.png")


if __name__ == "__main__":
    main()
