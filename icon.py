from PIL import Image, ImageDraw

def create_icon():
    try:
        # Create a new image with a transparent background
        size = (256, 256)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Calculate dimensions
        padding = 20
        circle_bounds = (padding, padding, size[0] - padding, size[1] - padding)

        # Draw a circle with a blue color
        draw.ellipse(circle_bounds, fill='#2196F3', outline='white', width=8)

        # Save as ICO file
        image.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        return True
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

if __name__ == "__main__":
    success = create_icon()
    exit(0 if success else 1) 