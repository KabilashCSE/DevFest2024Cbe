import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
import io

# Set page config for mobile-friendly and centered layout
st.set_page_config(page_title="DevFest-Coimbatore2024", layout="wide")

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

        # Fixed zoom level at 50% (no dynamic slider)
        zoom_level = 50  # Fixed zoom level

        # Resize the image based on the fixed zoom level
        width, height = uploaded_image.size
        new_width = int(width * zoom_level / 100)
        new_height = int(height * zoom_level / 100)

        # Resize the image to the selected zoom level
        resized_image = uploaded_image.resize((new_width, new_height))

        # Create a canvas to hold the image, placing it on the left side of the canvas
        final_image = Image.new("RGBA", (max(new_width, 800), max(new_height, 800)), (255, 255, 255, 0))

        # Paste the resized image near the left side of the canvas (aligned to the left)
        final_image.paste(resized_image, (0, (final_image.height - resized_image.height) // 2))

        # Create the cropping tool with a fixed 1:1 aspect ratio (square cropper)
        st.write("Crop your image:")
        
        # Adjust the cropper to remain a square and positioned on the left side
        cropped_image = st_cropper(final_image, box_color=primary_color, aspect_ratio=(1, 1))

        # Create the final image after cropping and overlaying it on the template
        diameter = RADIUS * 2
        resized_cropped_image = cropped_image.resize((diameter, diameter))

        # Create a new canvas matching the template size
        final_image = Image.new("RGBA", template_image.size)

        # Paste the resized image at the circle's center
        offset_x = CENTER_X - RADIUS
        offset_y = CENTER_Y - RADIUS
        final_image.paste(resized_cropped_image, (offset_x, offset_y), mask=resized_cropped_image)

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
