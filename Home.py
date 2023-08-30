import streamlit as st
import cv2
import face_recognition as frg
import yaml
import time
from utils import recognize, build_dataset

# Initialize session state
if 'captured_frame' not in st.session_state:
    st.session_state.captured_frame = None

st.set_page_config(layout="wide")
cfg = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

st.sidebar.title("Settings")
menu = ["IMG", "Webcam"]
choice = st.sidebar.selectbox("Input type", menu)
TOLERANCE = st.sidebar.slider("Tolerance", 0.0, 1.0, 0.5, 0.01)

st.sidebar.title("Person ID")

# Initialize an empty list for name and ID containers
name_containers = []
id_containers = []

if choice == "IMG":
    st.title("FaceRS - Recognition System")
    st.write(PICTURE_PROMPT)
    uploaded_images = st.file_uploader("Upload", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
    if len(uploaded_images) != 0:
        for image in uploaded_images:
            image = frg.load_image_file(image)
            image, names, ids, matched_images = recognize(image, TOLERANCE)
            
            # Create a name and ID container for each recognized face
            for i in range(len(names)):
                name_containers.append(st.sidebar.empty())
                id_containers.append(st.sidebar.empty())

            # Update each container with the corresponding face name and ID
            for i in range(len(names)):
                name_containers[i].info(f"Name: {names[i]}")
                id_containers[i].success(f"ID: {ids[i]}")
                
                col1, col2 = st.columns(2)
                col1.image(image, caption="Uploaded Image")
                if matched_images[i] is not None:
                    col2.image(matched_images[i], caption="Matched Image from Database")
                else:
                    col2.info("No match found in database")
    else:
        st.info("Please upload an image")

elif choice == "Webcam":
    st.title("FaceRS - Recognition System")
    st.write(WEBCAM_PROMPT)
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        st.error("Could not open video device")
        st.stop()
    else:
        st.info("Successfully accessed the webcam")
        time.sleep(2)

    FRAME_WINDOW = st.empty()
    capture_button = st.button("Capture Frame")

    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to capture frame from camera")
            st.info("Please turn off the other app that is using the camera and restart app")
            st.stop()
        if capture_button or st.session_state.captured_frame is not None:
            if capture_button:
                st.session_state.captured_frame = frame
            image, name, id, matched_image = recognize(st.session_state.captured_frame, TOLERANCE)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            col1, col2 = st.columns(2)
            col1.image(image, caption="Captured Image")
            if matched_image is not None:
                col2.image(matched_image, caption="Matched Image from Database")
            else:
                col2.info("No match found in database")
        FRAME_WINDOW.image(frame, channels="BGR")
st.sidebar.title("Dev Interface")
with st.sidebar.form(key='my_form'):
    submit_button = st.form_submit_button(label='REBUILD Database')
    if submit_button:
        with st.spinner("Rebuilding Database..."):
            build_dataset()
        st.success("Database has been reset");
st.sidebar.title("@martintmv")
        