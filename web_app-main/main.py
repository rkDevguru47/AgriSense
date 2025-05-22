import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps 
import numpy as np
import urllib.parse

np.set_printoptions(suppress=True)
model = load_model("model/keras_model.h5", compile=False)
class_names = open("model/labels.txt", "r").readlines()

#Tensorflow Model Prediction
def model_prediction(test_image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(test_image).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    class_name = class_names[index].lstrip('0123456789').replace(",_"," : ").replace("__"," : ").replace("_"," ").title()
    return class_name, round(confidence_score*100,2)

#Initializing page configuration
st.set_page_config(page_title="AgriSense",page_icon="assets/logo.png",layout="wide")

#Sidebar
st.sidebar.image("assets/logo.png", use_column_width=False, width=148)
st.sidebar.title("AgriSense")
st.sidebar.write("Intelligent plant disease detection system for enhanced agricultural productivity ✨")

#Global header image
image_path = "assets/background.png"
st.image(image_path,use_column_width=True)

app_section = st.sidebar.selectbox("Select Page",["🏠 Home","ℹ️ About","🩺 Disease Detection"])

#Main Page
if(app_section=="🏠 Home"):
    st.header("AgriSense")

    st.markdown("""
    Welcome to the AgriSense! 🌿📸
    
    Our mission is to help in identifying plant diseases efficiently. Upload an image of a plant, and our system will analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!

    ### How It Works
    1. **Upload Image:** Go to the **Disease Detection** page and upload an image of a plant with suspected diseases.
    2. **Analysis:** Our system will process the image using advanced algorithms to identify potential diseases.
    3. **Results:** View the results and recommendations for further action.

    ### Why Choose Us?
    - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
    - **User-Friendly:** Simple and intuitive interface for seamless user experience.
    - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

    ### Get Started
    Click on the **Disease Detection** page in the sidebar to upload an image and experience the power of our Plant Disease Detection System!

    ### About Us
    Learn more about the project, our team, and our goals on the **About** page.
    """)

#About Page
elif(app_section=="ℹ️ About"):
    st.header("About")

    st.markdown("""
                #### Introduction :
                AgriSense, developed by Group R2 of batch 2024, ITER-SOA is an advanced system utilizing computer vision and machine learning to revolutionize agricultural practices. It aims to address the challenges faced by farmers in timely and accurate plant disease detection, thereby enhancing agricultural productivity and ensuring vegetable safety.

                #### Key Features :
                - Utilizes image processing technology to analyze plant images captured with smartphones or digital cameras.
                - Employs deep learning algorithms, including convolutional neural networks (CNNs), for disease classification and identification.
                - Provides farmers with timely disease detection and recommendations for appropriate treatment or prevention.
                - Offers a user-friendly interface accessible via mobile or web platforms, enabling easy image uploads and access to diagnostic information, articles, and videos related to identified diseases.

                #### Benefits :
                - Reduces crop losses and improves crop quality by facilitating early and accurate disease detection.
                - Decreases dependence on pesticides, fostering sustainable agricultural practices.
                - Promotes permaculture by integrating with fundamental permaculture design principles and facilitating knowledge sharing.
                - Enhances agricultural productivity and vegetable safety, benefiting both farmers and society at large.

                #### Team : 
                - Vishal Kumar
                - Rishu Kumar
                - Preetish Kumar Sethi
                - Rishi Kant

                #### Guidance :
                - Dr. Binayak Panda (Project Supervisor)
                - Dr. Rasmita Dash (Section Coordinator, SDP)

                AgriSense represents a paradigm shift in agricultural management, combining technological innovation with sustainability for a more resilient and productive agricultural sector.
                """)

#Prediction Page
elif(app_section=="🩺 Disease Detection"):
    st.header("Disease Detection")
    st.subheader("Upload an image of a plant to detect any signs of diseases")
    st.image("assets/sample_image_grid.png")
    st.caption("\* Ensure images are well-lit and properly composed to capture the subject clearly, avoiding shadows, glare, or distracting backgrounds as shown in the examples above.")

    test_image = st.file_uploader("Choose an Image :", type=['png','jpg','jpeg'])
    if(test_image is not None):
        if(st.button("🖼️ Show Image")):
            st.image(test_image, width=512)

        #Predict button
        if(st.button("🪄 Predict")):
            st.write("Our Prediction")
            disease_detected, probability = model_prediction(test_image)   
            st.balloons()
            disease_detected = "None" if (("healthy".casefold() in disease_detected.casefold()) or probability < 60) else disease_detected         
            confidence = f"\nConfidence : {probability}%" if disease_detected!="None" else ""
            st.success(f"Disease Detected : {disease_detected}  {confidence}")
            if(disease_detected!="None"):
                st.link_button("🔍 Know More ", "https://www.google.com/search?"+urllib.parse.urlencode({"q": f"{disease_detected} plant disease"}))
