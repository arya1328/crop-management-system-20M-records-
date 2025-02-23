import streamlit as st
import pandas as pd
import mysql.connector
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# MySQL Database Connection Details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "crop_management"
}

# Lists for Dropdowns
crop_names = ["Wheat", "Rice", "Corn", "Soybean", "Barley", "Sugarcane", "Cotton", "Potato", "Tomato", "Lettuce"]
growth_stages = ["Seedling", "Vegetative", "Flowering", "Fruiting", "Maturity"]
pest_control_measures_list = [
    "Use of organic pesticides",
    "Crop rotation",
    "Neem oil application",
    "Biological pest control",
    "Chemical pesticides",
    "Regular field monitoring"
]

# Connect to the Database
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Insert Manual Crop Record
def insert_manual_record(crop_name, planting_date, harvest_date, growth_stage, pest_control, yield_prediction):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO crops (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (crop_name, planting_date, harvest_date, growth_stage, pest_control, yield_prediction))
            conn.commit()
            st.success("✅ Crop record inserted successfully!")
            st.rerun()  # Live update the UI
        except mysql.connector.Error as e:
            st.error(f"⚠️ Error inserting record: {e}")
        finally:
            conn.close()

# Generate Random Data for Bulk Insert
def generate_data():
    crop_name = random.choice(crop_names)
    planting_date = fake.date_between(start_date="-2y", end_date="today")
    harvest_date = planting_date + timedelta(days=random.randint(60, 180))
    growth_stage = random.choice(growth_stages)
    pest_control = random.choice(pest_control_measures_list)
    yield_prediction = random.randint(500, 5000)
    return (crop_name, planting_date, harvest_date, growth_stage, pest_control, yield_prediction)

# Bulk Insert Records
def insert_bulk_records(total_records):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        batch_size = 10000 if total_records >= 10000 else total_records

        for i in range(0, total_records, batch_size):
            current_batch = min(batch_size, total_records - i)
            data_batch = [generate_data() for _ in range(current_batch)]
            cursor.executemany("""
                INSERT INTO crops (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, data_batch)
            conn.commit()
            st.info(f"🛠 {i + current_batch} records inserted...")
        st.success(f"✅ {total_records} records inserted successfully!")
        conn.close()
        st.rerun()  # Refresh UI after bulk insertion

# Fetch Crop Records
def get_top_10_records():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        # Pull all records, then we'll show the top 10 from the beginning
        cursor.execute("SELECT id, crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction FROM crops ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Add custom CSS with background image and styling
def add_bg_and_styling():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                            url("https://images.unsplash.com/photo-1574943320219-553eb213f72d");
            background-size: cover;
            background-attachment: fixed;
        }

        .css-1d391kg {
            background-color: rgba(28, 28, 28, 0.92) !important;
        }

        .crop-card {
            background-color: rgba(45, 75, 45, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            border: 2px solid #4CAF50;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }

        .stButton>button:hover {
            background-color: #45a049 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }

        .stSelectbox>div>div>div {
            background-color: rgba(45, 75, 45, 0.95) !important;
            color: white !important;
            border: 1px solid #4CAF50 !important;
        }

        h1, h2, h3 {
            color: #4CAF50 !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            font-weight: 600 !important;
        }

        .stMarkdown, .stText {
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }

        .stDataFrame {
            background-color: rgba(45, 75, 45, 0.95) !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }

        .css-1y4p8pa {
            padding: 3rem 1rem 1rem !important;
        }

        [data-testid="stFormSubmitButton"] {
            background-color: #4CAF50 !important;
            color: white !important;
        }

        .stDateInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 1px solid #4CAF50 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

# Update the main part of your script
def main():
    add_bg_and_styling()
    
    # Update title with emoji and styling
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50; margin-bottom: 30px;'>
            🌾 Smart Crop Management System
        </h1>
    """, unsafe_allow_html=True)

    # Create two tabs with custom styling
    tab1, tab2 = st.tabs(["📝 Insert Data", "📊 View Database"])

    with tab1:
        st.markdown('<div class="crop-card">', unsafe_allow_html=True)
        st.markdown("### 🌱 Insert a New Crop Record")
        with st.form("manual_entry_form"):
            selected_crop = st.selectbox("🌱 Crop Name", crop_names)
            planting_date = st.date_input("📅 Planting Date")
            harvest_date = st.date_input("📅 Harvest Date")
            selected_growth_stage = st.selectbox("🌿 Growth Stage", growth_stages)
            selected_pest_control = st.selectbox("🛡 Pest Control Measures", pest_control_measures_list)
            yield_prediction = st.number_input("📊 Yield Prediction (kg)", min_value=0, step=1)
            submitted = st.form_submit_button("➕ Insert Record")
            if submitted:
                insert_manual_record(selected_crop, planting_date, harvest_date, 
                                  selected_growth_stage, selected_pest_control, yield_prediction)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="crop-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Bulk Insert Crop Records")
        bulk_option = st.selectbox("Select number of records to insert", 
                                 options=[1000, 10000, 100000])
        if st.button("⚡ Start Bulk Insert"):
            insert_bulk_records(bulk_option)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="crop-card">', unsafe_allow_html=True)
        st.markdown("### 📑 Current Crop Records")
        records = get_top_10_records()
        if records:
            columns = ["ID", "Crop Name", "Planting Date", "Harvest Date", 
                      "Growth Stage", "Pest Control", "Yield Prediction"]
            df = pd.DataFrame(records, columns=columns)
            st.dataframe(df.drop(columns=["ID"]).head(10), 
                        use_container_width=True)
        else:
            st.warning("⚠️ No records found in database.")
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()