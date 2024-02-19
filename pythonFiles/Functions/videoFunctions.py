import cv2
from PIL import ImageChops, Image

def average_brightness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = int(gray.mean())
    return brightness

def crop_center(image, crop_width, crop_height):
    width, height = image.size
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = (width + crop_width) // 2
    bottom = (height + crop_height) // 2
    return image.crop((left, top, right, bottom))

def image_difference(img1, img2):
    diff = ImageChops.difference(img1, img2)
    diff = diff.convert('L')  # Convert to grayscale
    return diff

def calculate_difference_percentage(diff_img, threshold=10):
    pixels = diff_img.getdata()
    different_pixels = sum(1 for pixel in pixels if pixel > threshold)
    total_pixels = diff_img.width * diff_img.height
    percentage = (different_pixels / total_pixels) * 100
    return percentage

def draw_button(frame, button_img):
    # Overlay the button image onto the frame
    #button_height, button_width, _ = button_img.shape
    #frame[button_y:button_y + button_height, button_x:button_x + button_width] = button_img
    button_height, button_width, _ = button_img.shape
    for i in range(button_height):
        for j in range(button_width):
            if button_img[i, j, 3] != 0:  # Check alpha channel
                frame[10 + i, 300 + j] = button_img[i, j, :3]  # Blend RGB channels