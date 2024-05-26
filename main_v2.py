import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import cv2

# Load pre-trained VGG16 model (with weights from ImageNet)
model = VGG16(weights='imagenet', include_top=False, input_shape=(1024, 1024, 3))


def add_zero_channels(image_gray):
    # print(image_gray)
    # Ensure that the input image is a 2D grayscale image
    if len(image_gray.shape) != 2:
        raise ValueError("Input image must be a 2D grayscale image")

    # Get the dimensions of the grayscale image
    height, width = image_gray.shape

    # Create a 3-channel blank image with zeros
    image_rgb = np.zeros((height, width, 3), dtype=np.uint8)

    # Set the first channel (red) to the grayscale image
    image_rgb[:, :, 0] = image_gray

    # Return the 3-channel image with two additional channels (green and blue) having zero values
    return image_rgb



def preprocess_image(image_path):
    # Open and preprocess the image
    # image = Image.open(image_path)
    # image = image.convert("L")  # Ensure 3 channels
    image = cv2.imread(image_path, 0)
    image=cv2.fastNlMeansDenoising(image,None)
    image=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    image = add_zero_channels(image)
    # print("check",image)
    image=cv2.resize(image,(1024,1024))
    
    # image = image.resize((224, 224))  # Resize to VGG16 input size
    # print("size",image)
    image_array = np.array(image, dtype=np.float32)
    # print("ss",image_array)
    image_array = preprocess_input(image_array)  # Preprocess for VGG16
    return image_array

def get_image_embedding(image_array):
    # Extract features from the image using the VGG16 model
    image_array = np.expand_dims(image_array, axis=0)
    features = model.predict(image_array)
    return features.flatten()  # Flatten the feature tensor into a 1D vector

# Paths to the two receipt images for comparison
user_receipt = "/home/gaditek/Receipt-Scanner/CustomerDataset/DUNKIN/Lucky-One-Mall/17389-6396100ad2cf5.png"
sample_receipt = "/home/gaditek/Receipt-Scanner/ReceiptDataset/DUNKIN/dunkin-lucky-one-mall-karachi/Tl0LOCfcRxQUY9FOvbvmD0dKByYxRWgzoxNhfcrV.jpg"

# Preprocess the images and get their embeddings
user_array = preprocess_image(user_receipt)
sample_array = preprocess_image(sample_receipt)

user_embedding = get_image_embedding(user_array)
sample_embedding = get_image_embedding(sample_array)

# Calculate the cosine similarity between the two embeddings
similarity_score = cosine_similarity(user_embedding.reshape(1, -1), sample_embedding.reshape(1, -1))

print(similarity_score)

# Set a similarity threshold (adjust as per your needs)
similarity_threshold = 0.65

if similarity_score >= similarity_threshold:
    print("The receipts are similar.")
else:
    print("The receipts are dissimilar.")
