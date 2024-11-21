import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
import io

# Set page config for mobile-friendly and centered layout
st.set_page_config(page_title="DevFest Coimbatore 2024", layout="centered")

# Google-themed colors
primary_color = "#4285F4"
secondary_color = "#34A853"
background_color = "#FFFFFF"
button_color = "#F4B400"

# Cover image at the top
cover_image_url = "https://res.cloudinary.com/startup-grind/image/upload/c_scale,w_2560/c_crop,h_640,w_2560,y_0.0_mul_h_sub_0.0_mul_640/c_crop,h_640,w_2560/c_fill,dpr_2.0,f_auto,g_center,q_auto:good/v1/gcs/platform-data-goog/event_banners/banner_devfest24_uy42yXv.png"
st.image(cover_image_url, use_column_width=True)

# Fixed template image
TEMPLATE_PATH = "frame.png"
CENTER_X, CENTER_Y, RADIUS = 1086, 1932, 910

# Load the template image
try:
    template_image = Image.open(TEMPLATE_PATH).convert("RGBA")
except Exception as e:
    st.error(f"Failed to load the template image. Ensure '{TEMPLATE_PATH}' exists.")
    st.stop()

# Title



# File uploader
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])

# Process the uploaded image
if uploaded_file:
    try:
        uploaded_image = Image.open(uploaded_file).convert("RGBA")
        st.write("Crop your image (1:1 aspect ratio):")
        
        # Crop the image with a fixed 1:1 ratio
        cropped_image = st_cropper(uploaded_image, box_color=primary_color, aspect_ratio=(1, 1))
        
        # Resize the cropped image to match the circle's diameter
        diameter = RADIUS * 2
        resized_image = cropped_image.resize((diameter, diameter))

        # Create a new canvas matching the template size
        final_image = Image.new("RGBA", template_image.size)

        # Paste the resized image at the circle's center
        offset_x = CENTER_X - RADIUS
        offset_y = CENTER_Y - RADIUS
        final_image.paste(resized_image, (offset_x, offset_y), mask=resized_image)

        # Overlay the template image on top
        final_image.paste(template_image, (0, 0), template_image)

        # Display the final image
        st.image(final_image, use_column_width=True)

        # Create a downloadable image file
        buf = io.BytesIO()
        final_image.save(buf, format="PNG")
        buf.seek(0)

        # Add Download Button with Google theme
        st.download_button(
            label="Download",
            data=buf,
            file_name="final-image.png",
            mime="image/png",
            use_container_width=True,
            key="download-button"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
