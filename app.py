import streamlit as st
import pandas as pd
import os 

st.set_page_config(page_title="SkyBooker", layout="wide")


def save_passenger_details(flight_info, passengers, email):
    
    new_bookings = []
    for seat, name in passengers.items():
        new_bookings.append({
            "Airline": flight_info['airline'],
            "Source": flight_info['Source'],
            "Destination": flight_info['destination'],
            "Date": flight_info['date_of_journey'],
            "Seat": seat,
            "Passenger_Name": name,
            "Contact_Email": email,
            "Price_Paid": flight_info['Price']
        })
    
    new_df = pd.DataFrame(new_bookings)
    

    file_path = 'passenger_bookings.csv'
    if not os.path.isfile(file_path):
        new_df.to_csv(file_path, index=False)
    else:
        new_df.to_csv(file_path, mode='a', header=False, index=False)

@st.cache_data
def load_and_preprocess_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df = df.dropna(subset=['Source', 'destination', 'Price', 'Total_stops', 'Duration'])
        
        def duration_to_minutes(duration_str):
            try:
                h, m = 0, 0
                parts = str(duration_str).split()
                for p in parts:
                    if 'h' in p: h = int(p.replace('h', ''))
                    elif 'min' in p: m = int(p.replace('min', ''))
                return (h * 60) + m
            except: return 0

        df['Duration_minutes'] = df['Duration'].apply(duration_to_minutes)
        df['Price'] = df['Price'].astype(int)
        return df
    except FileNotFoundError:
        st.error(f"Error: '{file_path}' not found.")
        return pd.DataFrame()

df = load_and_preprocess_data('flightdata.csv')


if 'selected_seats' not in st.session_state:
    st.session_state.selected_seats = []
if 'booking_complete' not in st.session_state:
    st.session_state.booking_complete = False

st.sidebar.header("🔍 Filter Flights")
if not df.empty:
    sources = sorted(df['Source'].unique())
    destinations = sorted(df['destination'].unique())

    source_city = st.sidebar.selectbox("Select Source", sources)
    dest_city = st.sidebar.selectbox("Select Destination", destinations)
    max_price = st.sidebar.slider("Maximum Price (₹)", int(df['Price'].min()), int(df['Price'].max()), int(df['Price'].max()))
    stop_options = sorted(df['Total_stops'].unique())
    selected_stops = st.sidebar.multiselect("Stops", stop_options, default=stop_options)
    max_dur_mins = int(df['Duration_minutes'].max())
    duration_limit = st.sidebar.slider("Maximum Duration (hours)", 1, (max_dur_mins // 60) + 1, (max_dur_mins // 60) + 1)
    
    filtered_df = df[
        (df['Source'] == source_city) & 
        (df['destination'] == dest_city) & 
        (df['Price'] <= max_price) &
        (df['Total_stops'].isin(selected_stops)) &
        (df['Duration_minutes'] <= duration_limit * 60)
    ]

st.title("✈️ SkyBooker: Booking Engine")

if not filtered_df.empty:
    st.subheader(f"Flights from {source_city} to {dest_city}")
    st.dataframe(filtered_df[['airline', 'date_of_journey', 'dep_time', 'Arrival_time', 'Duration', 'Total_stops', 'Price']], use_container_width=True)
    st.divider()

    st.subheader("🎟️  Select Flight")
    flight_options = filtered_df.apply(lambda x: f"ID: {x.name} | {x['airline']} - ₹{x['Price']}", axis=1).tolist()
    selected_flight_label = st.selectbox("Choose your flight:", options=flight_options, index=None)

    if selected_flight_label:
        selected_index = int(selected_flight_label.split("|")[0].replace("ID: ", "").strip())
        flight_details = filtered_df.loc[selected_index]

        st.subheader("💺 Select Seats")
        occupied_seats = ['1A', '2C', '4D']
        rows, cols = range(1, 7), ['A', 'B', 'C', 'D']

        for r in rows:
            c1, c2, gap, c3, c4 = st.columns([1, 1, 0.4, 1, 1])
            seat_cols = [c1, c2, c3, c4]
            for i, char in enumerate(cols):
                sid = f"{r}{char}"
                if sid in occupied_seats:
                    seat_cols[i].button(sid, key=sid, disabled=True)
                else:
                    is_mine = sid in st.session_state.selected_seats
                    if seat_cols[i].button(sid, key=sid, type="primary" if is_mine else "secondary", use_container_width=True):
                        if is_mine: st.session_state.selected_seats.remove(sid)
                        else: st.session_state.selected_seats.append(sid)
                        st.rerun()

        if st.session_state.selected_seats:
            st.divider()
            st.subheader("💳 Passenger Details")
            
            with st.form("multi_passenger_form"):
                passenger_data = {}
                st.write(f"Total Seats: {len(st.session_state.selected_seats)}")
                
                for seat in st.session_state.selected_seats:
                    st.write(f"**Seat {seat}**")
                    passenger_data[seat] = st.text_input(f"Full Name for Seat {seat}", key=f"name_{seat}")
                
                st.write("---")
                contact_email = st.text_input("Contact Email Address")
                
                if st.form_submit_button("Confirm & Take Off"):
                    if all(passenger_data.values()) and contact_email:
                      
                        save_passenger_details(flight_details, passenger_data, contact_email)
                        
                        st.session_state.booking_complete = True
                        st.session_state.final_passengers = passenger_data
                    else:
                        st.error("Please provide names for ALL selected seats and a contact email.")

        if st.session_state.booking_complete:
           
            st.markdown("""
                <div style="position: fixed; top: 40%; left: -100px; font-size: 90px; z-index: 1000; animation: takeoff 3.5s linear forwards;">✈️</div>
                <style>
                    @keyframes takeoff {
                        0% { left: -100px; transform: rotate(0deg); }
                        100% { left: 115%; transform: rotate(-20deg) translateY(-250px); }
                    }
                </style>
            """, unsafe_allow_html=True)
            
            st.success("Tickets Booked and Details Saved Locally!")
            with st.container(border=True):
                st.write(f"### 🎫 Booking Confirmed: {flight_details['airline']}")
                for seat, name in st.session_state.final_passengers.items():
                    st.write(f"✈️ **Seat {seat}**: {name}")
                st.write(f"**Total Paid:** ₹{len(st.session_state.selected_seats) * flight_details['Price']}")
            
            if st.checkbox("Show all saved bookings"):
                stored_data = pd.read_csv('passenger_bookings.csv')
                st.table(stored_data.tail(10))

            if st.button("Start New Booking"):
                st.session_state.selected_seats = []
                st.session_state.booking_complete = False
                st.rerun()
else:
    st.warning("No flights matching your filters.")