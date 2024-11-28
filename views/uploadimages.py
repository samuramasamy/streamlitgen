# # import streamlit as st
# # import psycopg2
# # import pandas as pd
# # from io import BytesIO
# # import base64

# # # Database connection configuration
# # db_connection = {
# #     "host": "34.93.64.44",
# #     "port": "5432",
# #     "dbname": "genai",
# #     "user": "postgres",
# #     "password": "postgres-genai"
# # }

# # # Function to fetch data from the PostgreSQL database
# # def fetch_data_from_db():
# #     try:
# #         conn = psycopg2.connect(**db_connection)
# #         query = "SELECT sno, status, image_feedback FROM upload_images;"
# #         df = pd.read_sql(query, conn)
# #         conn.close()
# #         return df
# #     except psycopg2.OperationalError as e:
# #         st.error(f"OperationalError: Unable to connect to the database: {e}")
# #         return None
# #     except Exception as e:
# #         st.error(f"Error: {e}")
# #         return None

# # # Function to insert a new image into the PostgreSQL database
# # def insert_new_image(serial_no, image_data, status, image_feedback):
# #     try:
# #         conn = psycopg2.connect(**db_connection)
# #         cursor = conn.cursor()
# #         query = """
# #         INSERT INTO upload_images (sno, image, status, image_feedback)
# #         VALUES (%s, %s, %s, %s);
# #         """
# #         cursor.execute(query, (serial_no, psycopg2.Binary(image_data), status, image_feedback))
# #         conn.commit()
# #         conn.close()
# #         st.success("Image uploaded successfully!")
# #     except Exception as e:
# #         st.error(f"Error inserting new image: {e}")

# # # Streamlit app layout
# # st.title("Upload Images to Database")

# # # Fetch and display data from the 'upload_images' table
# # st.subheader("Existing Data")
# # df = fetch_data_from_db()
# # if df is not None:
# #     st.write("Data from the 'upload_images' table:")
# #     st.dataframe(df)
# # else:
# #     st.write("No data available.")

# # # Section to Add New Image
# # st.subheader("Upload New Image")

# # # Streamlit form for uploading a new image
# # with st.form(key="image_upload_form"):
# #     serial_no = st.text_input("Serial No.")
# #     image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
# #     status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
# #     image_feedback = st.text_area("Image Feedback")

# #     submit_button = st.form_submit_button("Upload Image")

# #     # If the form is submitted, insert new data into the database
# #     if submit_button:
# #         if serial_no and image_file:
# #             if serial_no.isdigit():
# #                 # Read the uploaded image file
# #                 image_data = image_file.read()
# #                 insert_new_image(serial_no, image_data, status, image_feedback)
# #             else:
# #                 st.warning("Serial No. must be a valid number.")
# #         else:
# #             st.warning("Please fill in all required fields.")


# import streamlit as st
# import psycopg2
# import pandas as pd
# import os
# import shutil
# from pathlib import Path

# # Database connection configuration
# db_connection = {
#     "host": "34.93.64.44",
#     "port": "5432",
#     "dbname": "genai",
#     "user": "postgres",
#     "password": "postgres-genai"
# }

# # Directory to save uploaded images (you can change this as needed)
# UPLOAD_DIR = "uploaded_images"
# Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

# # Function to fetch data from the 'upload_images' table
# def fetch_data_from_db():
#     try:
#         # Connect to PostgreSQL database
#         conn = psycopg2.connect(**db_connection)
#         query = "SELECT * FROM upload_images;"  # SQL query to fetch all data from 'upload_images' table
#         df = pd.read_sql(query, conn)  # Using pandas to fetch data into a dataframe
#         conn.close()  # Close the connection
#         return df
#     except psycopg2.OperationalError as e:
#         st.error(f"OperationalError: Unable to connect to the database: {e}")
#         return None
#     except Exception as e:
#         st.error(f"Error: {e}")
#         return None

# # Function to insert a new image record into the 'upload_images' table
# def insert_new_image(sno, image_filename, status, image_feedback):
#     try:
#         # Connect to PostgreSQL database
#         conn = psycopg2.connect(**db_connection)
#         cursor = conn.cursor()
#         query = """
#         INSERT INTO upload_images (sno, image, status, image_feedback)
#         VALUES (%s, %s, %s, %s);
#         """
#         cursor.execute(query, (sno, image_filename, status, image_feedback))
#         conn.commit()  # Commit the transaction
#         conn.close()  # Close the connection
#         st.success("New image record added successfully!")
#     except Exception as e:
#         st.error(f"Error inserting new image record: {e}")

# # Streamlit app layout
# st.title("Upload Images - Data from Database")

# # Fetch and display data from the 'upload_images' table
# df = fetch_data_from_db()
# if df is not None:
#     st.write("Data from the 'upload_images' table:")
#     st.dataframe(df)  # Display data in a table format
# else:
#     st.write("No data available.")

# # Section to Add New Image
# st.subheader("Add New Image Record")

# # Streamlit form for adding a new image record
# with st.form(key="new_image_form"):
#     sno = st.text_input("Serial No.")
#     status = st.selectbox("Status", ["APPROVED", "REJECTED"])
#     image_feedback = st.number_input("Image Feedback (Integer)", min_value=0, value=0, step=1)

#     # Image upload
#     uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

#     submit_button = st.form_submit_button("Add Image Record")

#     # If the form is submitted, handle the image upload
#     if submit_button:
#         if sno and uploaded_file:  # Check for required fields
#             # Validate if sno is a valid integer
#             if sno.isdigit():
#                 # Save the uploaded image to the server's directory
#                 image_filename = f"{sno}_{uploaded_file.name}"
#                 image_path = os.path.join(UPLOAD_DIR, image_filename)

#                 # Save the uploaded image file to the directory
#                 with open(image_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())

#                 # Insert new record into the database with image filename
#                 insert_new_image(int(sno), image_filename, status, image_feedback)
#             else:
#                 st.warning("Serial No. must be a valid number.")
#         else:
#             st.warning("Please fill in all required fields and upload an image.")


import streamlit as st
import psycopg2
import pandas as pd
import os
from pathlib import Path

# Database connection configuration
db_connection = {
    "host": "34.93.64.44",
    "port": "5432",
    "dbname": "genai",
    "user": "postgres",
    "password": "postgres-genai"
}

# Directory to save uploaded images
UPLOAD_DIR = "uploaded_images"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

# Function to fetch data from the 'upload_images' table
def fetch_data_from_db():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_connection)
        query = "SELECT * FROM upload_images;"  # SQL query to fetch all data from 'upload_images' table
        df = pd.read_sql(query, conn)  # Using pandas to fetch data into a dataframe
        conn.close()  # Close the connection
        return df
    except psycopg2.OperationalError as e:
        st.error(f"OperationalError: Unable to connect to the database: {e}")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to insert a new image record into the 'upload_images' table
def insert_new_image(sno, image_filename, status, image_feedback):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_connection)
        cursor = conn.cursor()
        query = """
        INSERT INTO upload_images (sno, image, status, image_feedback)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (sno, image_filename, status, image_feedback))
        conn.commit()  # Commit the transaction
        conn.close()  # Close the connection
        st.success("New image record added successfully!")
    except Exception as e:
        st.error(f"Error inserting new image record: {e}")
# Streamlit app layout
st.title("Upload Images - Data from Database")

# Section to Add New Image
st.subheader("Add New Image Record")

# Placeholder to display uploaded images
uploaded_image_placeholder = st.empty()

# Streamlit form for adding a new image record
with st.form(key="new_image_form"):
    sno = st.text_input("Serial No.")
    status = st.selectbox("Status", ["APPROVED", "REJECTED"])
    image_feedback = st.slider("Image Feedback (Integer)", min_value=0,max_value=10, value=0, step=1)

    # Image upload
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    submit_button = st.form_submit_button("Add Image Record")

    # If the form is submitted, handle the image upload
    if submit_button:
        if sno and uploaded_file:  # Check for required fields
            if sno.isdigit():
                image_filename = f"{uploaded_file.name}"
                image_path = os.path.join(UPLOAD_DIR, image_filename)
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                insert_new_image(int(sno), image_filename, status, image_feedback)
                uploaded_image_placeholder.image(image_path, caption="Uploaded Image", use_container_width=True)
            else:
                st.warning("Serial No. must be a valid number.")
        else:
            st.warning("Please fill in all required fields and upload an image.")

# Fetch and display data from the 'upload_images' table at the bottom
st.subheader("Existing Data")
df = fetch_data_from_db()
if df is not None:
    st.write("Data from the 'upload_images' table:")
    st.dataframe(df)  # Display data in a table format
else:
    st.write("No data available.")



# # Streamlit app layout
# st.title("Upload Images - Data from Database")

# # Fetch and display data from the 'upload_images' table
# st.subheader("Existing Data")
# df = fetch_data_from_db()
# if df is not None:
#     st.write("Data from the 'upload_images' table:")
#     st.dataframe(df)  # Display data in a table format
# else:
#     st.write("No data available.")

# # Section to Add New Image
# st.subheader("Add New Image Record")

# # Placeholder to display uploaded images
# uploaded_image_placeholder = st.empty()

# # Streamlit form for adding a new image record
# with st.form(key="new_image_form"):
#     sno = st.text_input("Serial No.")
#     status = st.selectbox("Status", ["APPROVED", "REJECTED"])
#     image_feedback = st.number_input("Image Feedback (Integer)", min_value=0, value=0, step=1)

#     # Image upload
#     uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

#     submit_button = st.form_submit_button("Add Image Record")

#     # If the form is submitted, handle the image upload
#     if submit_button:
#         if sno and uploaded_file:  # Check for required fields
#             # Validate if sno is a valid integer
#             if sno.isdigit():
#                 # Save the uploaded image to the server's directory
#                 image_filename = f"{sno}_{uploaded_file.name}"
#                 image_path = os.path.join(UPLOAD_DIR, image_filename)

#                 # Save the uploaded image file to the directory
#                 with open(image_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())

#                 # Insert new record into the database with image filename
#                 insert_new_image(int(sno), image_filename, status, image_feedback)

#                 # Display the uploaded image below the form
#                 uploaded_image_placeholder.image(image_path, caption="Uploaded Image", use_column_width=True)
#             else:
#                 st.warning("Serial No. must be a valid number.")
#         else:
#             st.warning("Please fill in all required fields and upload an image.")


