import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# Configuration: Input and output image paths
input_image_path = "../media/shits_fired.png"  # Replace with your input image path
output_image_path = "../media/deep_fry_shits_fired.png"  # Replace with your desired output path

def increase_contrast(image, factor=1.8):
    """Increase the contrast of the image."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def add_noise(image, intensity=0.04):
    """Add random noise to the image."""
    np_image = np.array(image)
    noise = np.random.normal(loc=0, scale=255 * intensity, size=np_image.shape)
    np_image = np_image + noise
    np_image = np.clip(np_image, 0, 255).astype(np.uint8)
    return Image.fromarray(np_image)

def add_saturation(image, factor=1.8):
    """Boost the color saturation."""
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def add_sharpening(image, factor=1.8):
    """Sharpen the image."""
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def distort_image(image, intensity=4):
    """Apply a distortion effect to make the image look 'melted'."""
    np_image = np.array(image)
    h, w = np_image.shape[:2]
    flow = np.zeros((h, w, 2), dtype=np.float32)
    for i in range(h):
        for j in range(w):
            flow[i, j] = [
                np.sin(i / intensity) * intensity,
                np.sin(j / intensity) * intensity,
            ]
    map_x, map_y = cv2.split(flow)
    distorted = cv2.remap(
        np_image, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT
    )
    return Image.fromarray(distorted)

def apply_vignette(image, intensity=0.8):
    """Apply a vignette effect."""
    np_image = np.array(image)
    rows, cols = np_image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols * intensity)
    kernel_y = cv2.getGaussianKernel(rows, rows * intensity)
    kernel = kernel_y @ kernel_x.T
    mask = 255 * kernel / kernel.max()
    for i in range(3):  # Apply to RGB channels
        np_image[..., i] = np.clip(np_image[..., i] * mask, 0, 255)
    return Image.fromarray(np_image.astype(np.uint8))

def deepfry_image(image_path, output_path):
    """Apply deepfried effects to an image and save the result."""
    image = Image.open(image_path).convert("RGB")

    # Apply deepfried effects
    image = increase_contrast(image, factor=5.0)
    image = add_saturation(image, factor=5.0)
    image = add_noise(image, intensity=0.1)
    image = add_sharpening(image, factor=3.0)
    #image = distort_image(image, intensity=.1)
    image = apply_vignette(image, intensity=1)

    # Save the final image
    image.save(output_path, "PNG")
    print(f"Deepfried image saved to {output_path}")

# Run the program when the script is executed
if __name__ == "__main__":
    deepfry_image(input_image_path, output_image_path)
