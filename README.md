# ✈️ SkyBooker - Flight Booking Engine

A Streamlit-based flight booking application that allows users to search, filter, and book flights with seat selection.

## Features

- **Flight Search & Filtering**
  - Filter flights by source and destination cities
  - Filter by price range
  - Filter by number of stops
  - Filter by flight duration
  
- **Flight Display**
  - View available flights with details (airline, date, departure/arrival time, duration, stops, price)
  - Easy-to-read data table format
  
- **Seat Selection & Booking**
  - Select seats for flight bookings
  - Add multiple passengers
  - Track selected seats in real-time
  
- **Booking Management**
  - Save passenger details to CSV
  - Capture passenger names and contact email
  - Maintain booking history

## Project Structure

```
flight/
├── app.py                    # Main Streamlit application
├── flightdata.csv           # Flight data with routes and pricing
├── passenger_bookings.csv   # Booking records and passenger details
└── README.md               # This file
```

## Data Files

### flightdata.csv
Contains flight information with the following columns:
- `airline` - Airline name
- `date_of_journey` - Flight date
- `Source` - Departure city
- `destination` - Arrival city
- `route` - Flight route
- `dep_time` - Departure time
- `Arrival_time` - Arrival time
- `Duration` - Flight duration
- `Total_stops` - Number of stops
- `Additional_info` - Additional flight information
- `Price` - Ticket price (₹)

### passenger_bookings.csv
Stores booking records with:
- `Airline` - Airline name
- `Source`, `Destination` - Route details
- `Date` - Journey date
- `Seat` - Booked seat number
- `Passenger_Name` - Name of passenger
- `Contact_Email` - Passenger email
- `Price_Paid` - Amount paid

## Requirements

- Python 3.x
- Streamlit
- Pandas

## Installation

1. Install required packages:
```bash
pip install streamlit pandas
```

## Usage

Run the application:
```bash
streamlit run app.py
```

Then:
1. Open your browser and navigate to the Streamlit URL (usually `http://localhost:8501`)
2. Use the sidebar to filter flights by:
   - Source city
   - Destination city
   - Maximum price
   - Number of stops
   - Maximum duration
3. Select a flight from the filtered results
4. Choose your preferred seats
5. Enter passenger details
6. Complete your booking

## Key Functions

- `load_and_preprocess_data(file_path)` - Loads and cleans flight data, converts duration to minutes
- `save_passenger_details(flight_info, passengers, email)` - Records booking information to CSV
- `duration_to_minutes(duration_str)` - Converts duration string to minutes for filtering

## UI Customization

- Page configured with `wide` layout for better visibility
- Color-coded sections with emojis for better UX
- Session state management for selected seats and booking status
- Cached data loading for performance

## Notes

- Pre-occupied seats are marked as unavailable (currently: 1A, 2C, 4D)
- Prices are in Indian Rupees (₹)
- Data validation includes removal of null values in critical fields
- Application maintains booking history for records
