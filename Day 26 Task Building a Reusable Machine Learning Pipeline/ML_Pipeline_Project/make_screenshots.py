from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def render_terminal_image(text_file, out_file, title):
    with open(text_file, "r") as f:
        lines = f.read().splitlines()

    font = ImageFont.load_default()
    line_height = 16
    width = 800
    height = line_height * (len(lines) + 3) + 40

    img = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, 30], fill=(50, 50, 50))
    draw.text((10, 8), title, fill=(255, 255, 255), font=font)

    y = 45
    for line in lines:
        draw.text((15, y), line, fill=(0, 255, 100), font=font)
        y += line_height

    img.save(out_file)
    print("saved", out_file)

render_terminal_image("screenshots/non_pipeline_output.txt", "screenshots/screenshot_non_pipeline.png", "Terminal - train_without_pipeline.py")
render_terminal_image("screenshots/pipeline_output.txt", "screenshots/screenshot_pipeline.png", "Terminal - pipeline.py")
render_terminal_image("screenshots/predict_output.txt", "screenshots/screenshot_predict.png", "Terminal - predict.py")

accuracies = [0.70, 0.70]
labels = ["Without Pipeline", "With Pipeline"]

plt.figure(figsize=(5, 4))
plt.bar(labels, accuracies, color=["gray", "green"])
plt.ylim(0, 1)
plt.ylabel("Accuracy")
plt.title("Accuracy Comparison")
for i, v in enumerate(accuracies):
    plt.text(i, v + 0.02, str(v), ha="center")
plt.tight_layout()
plt.savefig("screenshots/accuracy_comparison.png")
print("saved screenshots/accuracy_comparison.png")
