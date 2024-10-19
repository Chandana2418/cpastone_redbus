import streamlit as st
import pandas as pd

# Function to load CSV data for the selected state
def load_csv_data(state_name):
    # Map state name to the corresponding CSV file
    state_csv_map = {
        'Andhra Pradesh': 'ap_bus_details.csv',
        'Assam': 'assam_bus_details.csv',
        'Chandigarh': 'chandigarh_bus_details.csv',
        'Himachal Pradesh': 'himachal_bus_details.csv',
        'Karnataka': 'kaac_bus_details.csv',
        'Kerala': 'kerala_bus_details.csv',
        'Meghalaya': 'meghalaya_bus_details.csv',
        'Rajasthan': 'rajastan_bus_details.csv',
        'Telangana': 'telangana_bus_details.csv',
        'West Bengal': 'wb_bus_details.csv'
    }

    # Load the corresponding CSV file into a DataFrame
    csv_file = state_csv_map.get(state_name)
    if csv_file:
        try:
            state_data = pd.read_csv(csv_file)
            return state_data
        except FileNotFoundError:
            st.error(f"CSV file for {state_name} not found!")
            return pd.DataFrame()  # Return an empty DataFrame if file not found
    else:
        st.error(f"No CSV mapping found for {state_name}")
        return pd.DataFrame()

# Streamlit app
state_options = ['Andhra Pradesh', 'Assam', 'Chandigarh', 'Himachal Pradesh', 
                 'Karnataka', 'Kerala', 'Meghalaya', 'Rajasthan', 'Telangana', 'West Bengal']

 # Title of the app
st.markdown("<h1 style='color: red;'>RED_BUS</h1>", unsafe_allow_html=True)


# Create a dropdown menu for selecting a state
selected_state = st.selectbox("Select a state", state_options)

if selected_state:
    state_data = load_csv_data(selected_state)

    # Check if the data is not empty
    if not state_data.empty:
        # Create two columns: left for the data, right for the filters
        left_col, right_col = st.columns([3, 1])

        with left_col:
            st.write(f"Data for {selected_state}")
            st.dataframe(state_data)

        with right_col:
            st.write("Filters")

            # Step 5: Create filters (dropdowns) based on the data columns
            if all(col in state_data.columns for col in ["Route_Name", "Bus_Name", "Bus_Type", "Price"]):

                # Dropdown for filtering by Route Name
                route_name = st.selectbox("Select Route Name", state_data["Route_Name"].unique())
                filtered_data = state_data[state_data["Route_Name"] == route_name]

                # Dropdown for filtering by Bus Name
                bus_name = st.selectbox("Select Bus Name", filtered_data["Bus_Name"].unique())
                filtered_data = filtered_data[filtered_data["Bus_Name"] == bus_name]

                # Dropdown for filtering by Bus Type
                bus_type = st.selectbox("Select Bus Type", filtered_data["Bus_Type"].unique())
                filtered_data = filtered_data[filtered_data["Bus_Type"] == bus_type]

                # Dropdown for filtering by Price
                price = st.selectbox("Select Price", filtered_data["Price"].unique())
                filtered_data = filtered_data[filtered_data["Price"] == price]

                # Step 6: Display the filtered data in the left column
                with left_col:
                    st.write("Filtered Data")
                    st.dataframe(filtered_data)  # Display the filtered data
            else:
                st.error("One or more required columns are missing in the data.")
    else:
        st.write(f"No data available for {selected_state}")
