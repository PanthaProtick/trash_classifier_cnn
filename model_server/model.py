from PIL import Image
import numpy as np  
import fastapi
import tensorflow as tf
import os

classes=['cardboard', 'trash', 'glass', 'paper', 'plastic', 'metal']

def preprocess_image(image_path, target_size=(128, 128)):
  img = Image.open(image_path).convert('RGB') # Ensure image is RGB
  img = img.resize(target_size) # Resize to model's input size
  img_array = np.array(img) # Convert to numpy array
  img_array = img_array / 255.0 # Normalize pixel values to 0-1
  img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
  return img_array

model_name = 'model_v1'
loaded_model = tf.keras.models.load_model('models/'+model_name+'.keras')

app=fastapi.FastAPI()

@app.post("/predict")
def predict(image_path: str):
    try:
        # Preprocess the image
        image_path = os.path.join("..", "uploads", image_path)
        preprocessed_image = preprocess_image(image_path)
        
        # Make prediction
        predictions = loaded_model.predict(preprocessed_image)
        
        # Convert logits to probabilities
        probabilities = tf.nn.softmax(predictions[0])

        # Get the predicted class index
        predicted_class_index = np.argmax(probabilities)
        predicted_class_name = classes[predicted_class_index]

        return {"predicted_class": predicted_class_name, "confidence": float(probabilities[predicted_class_index]), "model_name": model_name}
    except Exception as e:
        return {"error": str(e)}