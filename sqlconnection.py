import streamlit as st
import pymysql
import pandas as pd

# 1. Connect to MySQL Database
def get_connection():
    return pymysql.connect(host='127.0.0.1', user='root', passwd='123456789', database='redbus')

# 2. Fetch Route Names starting with a specific letter
def fetch_route_names(connection, starting_letter):
    query = f"SELECT DISTINCT Route_Name FROM bus_routes WHERE Route_Name LIKE '{starting_letter}%' ORDER BY Route_Name"
    route_names = pd.read_sql(query, connection)['Route_Name'].tolist()
    return route_names

# 3. Fetch data based on Route_Name and price sort order
def fetch_data(connection, route_name, price_sort_order):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = f"SELECT * FROM bus_routes WHERE Route_Name = %s ORDER BY Star_Rating DESC, Price {price_sort_order_sql}"
    df = pd.read_sql(query, connection, params=(route_name,))
    return df

# 4. Filter data by Star Rating and Bus Type
def filter_data(df, star_ratings, bus_types):
    filtered_df = df[df['Star_Rating'].isin(star_ratings) & df['Bus_Type'].isin(bus_types)]
    return filtered_df

# 5. Main Streamlit app
def main():
    st.header('Easy and Secure Online Bus Tickets Booking')

    # Establish connection to the database
    connection = get_connection()

    try:
        # Sidebar input for starting letter of Route Name
        starting_letter = st.sidebar.text_input('Enter starting letter of Route Name', 'A')

        if starting_letter:
            # Fetch route names that start with the specified letter
            route_names = fetch_route_names(connection, starting_letter.upper())

            if route_names:
                # Sidebar - Select a route name
                selected_route = st.sidebar.radio('Select Route Name', route_names)

                if selected_route:
                    # Sidebar - Select sorting preference for price
                    price_sort_order = st.sidebar.selectbox('Sort by Price', ['Low to High', 'High to Low'])

                    # Fetch data for the selected route and sort by price
                    data = fetch_data(connection, selected_route, price_sort_order)

                    if not data.empty:
                        # Display the fetched data
                        st.write(f"### Data for Route: {selected_route}")
                        st.write(data)

                        # Filter options for Star Rating and Bus Type
                        star_ratings = data['Star_Rating'].unique().tolist()
                        selected_ratings = st.multiselect('Filter by Star Rating', star_ratings)

                        bus_types = data['Bus_Type'].unique().tolist()
                        selected_bus_types = st.multiselect('Filter by Bus Type', bus_types)

                        if selected_ratings and selected_bus_types:
                            # Filter the data based on user selection
                            filtered_data = filter_data(data, selected_ratings, selected_bus_types)

                            # Display the filtered data
                            st.write(f"### Filtered Data for Star Rating: {selected_ratings} and Bus Type: {selected_bus_types}")
                            st.write(filtered_data)
                    else:
                        st.write(f"No data found for Route: {selected_route} with the specified price sort order.")
            else:
                st.write("No routes found starting with the specified letter.")
    finally:
        # Close the database connection
        connection.close()

# Run the app
if __name__ == '__main__':
    main()
