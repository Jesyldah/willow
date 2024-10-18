import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from PIL import Image

# Set page config
im = Image.open("./willow_logo.png")

st.set_page_config(layout="wide", page_title="Willow Travel Request", page_icon = im)

# Initialize the last number (this would ideally be persistent)
if 'last_no' not in st.session_state:
    st.session_state.last_no = 0  # Start at 0 for demonstration

# Function to auto-generate 'No' in the format 'ST001', 'ST002', etc.
def generate_no():
    st.session_state.last_no += 1  # Increment the last number
    return f"S-TR{st.session_state.last_no:04d}"  # Zero-padded to 3 digits

# Function to send POST request
def send_data(data):
    # Fetch credentials from Streamlit secrets
    username = st.secrets["API_USERNAME"]
    password = st.secrets["API_PASSWORD"]
    
    # API URL
    server_url = "http://102.37.155.57:5098/Willow/ODataV4/Company('Willow%20test')/travelRequest"
    
    # Send POST request with Basic Auth
    try:
        response = requests.post(server_url, json=data, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            return "Data sent successfully!"
        else:
            return f"Failed to send data. Status code: {response.status_code}, Message: {response.text}"
    except Exception as e:
        return f"Error: {e}"

# Custom style for headers and inputs
st.markdown("""

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

    <style>
    .header-text {
        font-size: 16px;
        font-weight: bold;
        color: #4682b4; /* SteelBlue for headers  */
        padding: 0px 0px;
    }
    .input-box {
        font-size: 15px;
        color: #fbe482; /*Tomato color for input fields*/
        font-weight: bold;
        padding: 0px 0px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #03396c, #03396c, #03396c, #E5E4E2); /* Green and grey background shades */
        background-color: #03396c;  /* Light grey-blue background color for sidebar */
    }

    .social-icons {
        position: fixed;
        bottom: 20px;
        left: 20px;
        font-size: 20px;
    }
    .social-icons a {
        margin-right: 15px;
        color: #fbe482;  /* SteelBlue for icon color */
        text-decoration: none;
    }
    .social-icons a:hover {
        color: #80c066;  /* Tomato color on hover */
    }

     #MainMenu, header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Sidebar with clickable buttons
st.sidebar.title("📃 :green[Busniess Forms]")
form_button = st.sidebar.button(" 🚘 Travel Request Form")
form_button2 = st.sidebar.button(" 🏖️ Leave Request Form")

# Check if Travel Request Form button is clicked
if form_button or 'form_button_clicked' in st.session_state:
    st.session_state.form_button_clicked = True  # Store state to keep form active

# Display Travel Request Form if button clicked
if 'form_button_clicked' in st.session_state and st.session_state.form_button_clicked:

    st.subheader(":grey[:green-background[Travel Request Form]]")

    # Auto-generate 'No'
    no = generate_no()

    # Fix 'Application_Date' to the current date
    application_date = datetime.now().date()

    # Define a list of projects for the dropdown
    project_names = [
        "Agriculture and Processing (AP)",
        "Education and Training",
        "Health and Wellness",
        "Infrastructure Development",
        "Technology and Innovation",
        "Environmental Conservation"
    ]

    # Collect other input data
    with st.form("travel_request_form"):
        # Display the auto-generated 'No' and fixed 'Application_Date'
        col5,col6 = st.columns(2)
        # Display the auto-generated 'No' and fixed 'Application_Date'
        with col5:
            st.markdown(f"<div class='header-text'>Generated No: </div>", unsafe_allow_html=True)
            st.markdown(f"<div class='input-box'>{no}</div>", unsafe_allow_html=True)
        with col6:
            st.markdown(f"<div class='header-text'>Application Date: </div>", unsafe_allow_html=True)
            st.markdown(f"<div class='input-box'>{application_date}</div>", unsafe_allow_html=True)

        st.markdown(f"<hr>", unsafe_allow_html=True)
        # Arrange Period Start Date and Period End Date side by side
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='header-text'>Period Start Date: </div>", unsafe_allow_html=True)
            period_start_date = st.date_input("", key="period_start_date")
        with col2:
            st.markdown(f"<div class='header-text'>Period End Date: </div>", unsafe_allow_html=True)
            period_end_date = st.date_input("", key="period_end_date")
        
        st.markdown(f"<div class='header-text'>Travel Description: </div>", unsafe_allow_html=True)
        travel_description = st.text_area("", "Flight request from Nairobi to Mombasa on 24th July & return on 30th July. Afternoon flight and a taxi to & fro")
        
        st.markdown(f"<div class='header-text'>PAF_No</div>", unsafe_allow_html=True)
        paf = st.text_input("", value="PAF0552")

        # Arrange Amount and Department side by side
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"<div class='header-text'>Amount: </div>", unsafe_allow_html=True)
            amount = st.number_input("", value=124000)
        with col4:
            st.markdown(f"<div class='header-text'>Department: </div>", unsafe_allow_html=True)
            department = st.text_input("", value="H")
        
        st.markdown(f"<div class='header-text'>Global Dimension 1 Code: </div>", unsafe_allow_html=True)
        global_dim_1_code = st.text_input("", value="AP00000")
        
        st.markdown(f"<div class='header-text'>Shortcut Dimension 3 Code: </div>", unsafe_allow_html=True)
        shortcut_dim_3_code = st.text_input("", value="OP3000")
        
        st.markdown(f"<div class='header-text'>Shortcut Dimension 4 Code: </div>", unsafe_allow_html=True)
        shortcut_dim_4_code = st.text_input("", value="OP32000")
        
        # Dropdown for 'Project Name'
        st.markdown(f"<div class='header-text'>Project Name: </div>", unsafe_allow_html=True)
        project_name = st.selectbox("", project_names)

        st.markdown(f"<div class='header-text'>Global Dimension 2 Code: </div>", unsafe_allow_html=True)
        global_dim_2_code = st.text_input("", value="OP32101")
        
        st.markdown(f"<div class='header-text'>Status: </div>", unsafe_allow_html=True)
        status = st.selectbox("", ["Open", "Closed"])

        # Submit button
        submitted = st.form_submit_button("Submit")

    # When form is submitted
    if submitted:
        data = {
            # "@odata.etag": "",
            # "No": no,
            # "Application_Date": str(application_date),
            "Period_Start_Date": str(period_start_date),
            "Period_End_Date": str(period_end_date),
            "Staff_Travel_Description": travel_description,
            "PAF_No": paf,
            "Amount": amount,
            "Amount_LCY": amount,
            "Department": department,
            "Global_Dimension_1_Code": global_dim_1_code,
            "Shortcut_Dimension_3_Code": shortcut_dim_3_code,
            "Shortcut_Dimension_4_Code": shortcut_dim_4_code,
            "Project_Name": project_name,
            "Global_Dimension_2_Code": global_dim_2_code,
            "Status": status,
        }

        # Send the data to the server
        result = send_data(data)
        st.success(result)

# Add social media icons at the bottom of the sidebar
st.sidebar.markdown("""
    <div class="social-icons">
        <a href="https://www.facebook.com/profile.php?id=61564968016761" target="_blank"><i class="fab fa-facebook-f"></i></a>
        <a href="https://tiktok.com/@willowhealthmedia" target="_blank"><i class="fab fa-tiktok"></i></a>
        <a href="https://www.linkedin.com/company/willow-health-media/posts/?feedView=all" target="_blank"><i class="fab fa-linkedin-in"></i></a>
        <a href="https://www.instagram.com/willowhealthmedia?igsh=cjQzNXowZWdoNWhy" target="_blank"><i class="fab fa-instagram"></i></a>
        <a href="https://youtube.com/@willowhealthmedia?si=LXaYkRbzUk8IGchN" target="_blank"><i class="fab fa-youtube"></i></a>
        <a href="https://whatsapp.com/channel/0029Vap3SMfEVccQCIpBaP12" target="_blank"><i class="fab fa-whatsapp"></i></a>
    </div>
    """, unsafe_allow_html=True)