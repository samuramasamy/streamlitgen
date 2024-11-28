import streamlit as st
import psycopg2
import pandas as pd

db_connection = {
    "host": "34.93.64.44",
    "port": "5432",
    "dbname": "genai",
    "user": "postgres",
    "password": "postgres-genai"
}

dialect = "postgresql"
host = "34.93.64.44"
port = "5432"
database = "genai"
username = "postgres"
password = "postgres-genai"

# Function to fetch data from the PostgreSQL database
def fetch_data_from_db():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_connection)
        query = "SELECT * FROM upload_prompts;"  # SQL query to fetch all data from 'upload_prompts' table
        df = pd.read_sql(query, conn)  # Using pandas to fetch data into a dataframe
        conn.close()  # Close the connection
        return df
    except psycopg2.OperationalError as e:
        st.error(f"OperationalError: Unable to connect to the database: {e}")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to insert a new prompt into the PostgreSQL database
def insert_new_prompt(serial_no, prompt_feedback, image_prompt, status):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_connection)
        cursor = conn.cursor()
        query = """
        INSERT INTO upload_prompts (sno, prompt_feedback, image_prompts, status)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (serial_no, prompt_feedback, image_prompt, status))
        conn.commit()  # Commit the transaction
        conn.close()  # Close the connection
        st.success("New prompt added successfully!")
    except Exception as e:
        st.error(f"Error inserting new prompt: {e}")

# Streamlit app layout
st.title("Upload Prompts - Data from Database")

# Fetch and display data from the 'upload_prompts' table in the database
# df = fetch_data_from_db()
# if df is not None:
#     st.write("Data from the 'upload_prompts' table:")
#     st.dataframe(df)  # Display data in a table format
# else:
#     st.write("No data available.")

# Section to Add New Prompt
st.subheader("Add New Prompt")

# Streamlit form for adding a new prompt
with st.form(key="new_prompt_form"):
    serial_no = st.text_input("Serial No.")
    image_prompt = st.text_area("Image Prompt")
    prompt_feedback = st.slider("Prompt Feedback(Integer)",min_value= 1, max_value=10, value=0,step=1)
    status = st.selectbox("Status", ["Pending", "Completed", "In Progress"])

    submit_button = st.form_submit_button("Add Prompt")

    # If the form is submitted, insert new data into the database
    if submit_button:
        if serial_no and prompt_feedback:  # Check for required fields
            # Validate if serial_no is a valid integer (or other desired checks)
            if serial_no.isdigit():
                insert_new_prompt(serial_no, prompt_feedback, image_prompt, status)
            else:
                st.warning("Serial No. must be a valid number.")
        else:
            st.warning("Please fill in all required fields.")

# Fetch and display data from the 'upload_prompts' table in the database            
df = fetch_data_from_db()
if df is not None:
    st.write("Data from the 'upload_prompts' table:")
    st.dataframe(df)  # Display data in a table format
else:
    st.write("No data available.")