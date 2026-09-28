# import streamlit as st 

# st.title('Hello World,This is My First Web Page Application')
# st.markdown('----')
# name = st.text_input("Enter your Name: ")
# st.number_input("Enter your age: ",min_value=5,max_value=105)
# st.selectbox('Gender: ',options=['Male','Female','Other'])
# st.radio('Maritial Staatus:',options=['Married','unmarried','separated'])
# st.multiselect('Meal: ',options=['Vadapav','Misalpav','Pavbhaji','pulav'],max_selections=2)
# st.segmented_control('Coach: ',options=['3Tier','2Tier','FirstClass','General'])
# st.date_input('Departure Date: ')
# st.time_input('Departure Time: ')

# st.date_input('Arrival Date: ')
# st.text_input('Arrival Time: ')

# st.feedback(options='stars')
# st.button("Click me")
# st.success(f'my Name os {name}')

import streamlit as st
import sqlite3
import random


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Railway Reservation System",
    page_icon="🚆",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

DATABASE = "railway.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (

            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,

            pnr TEXT UNIQUE NOT NULL,

            passenger_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            marital_status TEXT,

            source TEXT NOT NULL,
            destination TEXT NOT NULL,

            journey_date TEXT NOT NULL,
            boarding_time TEXT NOT NULL,

            arrival_date TEXT NOT NULL,
            arrival_time TEXT NOT NULL,

            coach TEXT NOT NULL,

            seat_count INTEGER NOT NULL,
            seat_numbers TEXT NOT NULL,

            meal TEXT,

            fare_per_seat REAL NOT NULL,
            total_fare REAL NOT NULL,

            booking_status TEXT DEFAULT 'Confirmed',

            feedback INTEGER,

            booking_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Create database when application starts
create_database()


# ============================================================
# PNR GENERATION
# ============================================================

def generate_pnr():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        pnr = str(random.randint(1000000000, 9999999999))

        cursor.execute(
            "SELECT pnr FROM bookings WHERE pnr = ?",
            (pnr,)
        )

        result = cursor.fetchone()

        if result is None:

            conn.close()

            return pnr


# ============================================================
# SEAT GENERATION
# ============================================================

def generate_seats(coach, number_of_seats):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT seat_numbers
        FROM bookings
        WHERE coach = ?
        """,
        (coach,)
    )

    previous_bookings = cursor.fetchall()

    conn.close()

    occupied_seats = set()

    for booking in previous_bookings:

        if booking[0]:

            seats = booking[0].split(",")

            for seat in seats:

                occupied_seats.add(int(seat))


    available_seats = []

    seat_number = 1

    while len(available_seats) < number_of_seats:

        if seat_number not in occupied_seats:

            available_seats.append(seat_number)

        seat_number += 1


    return available_seats


# ============================================================
# SAVE BOOKING
# ============================================================

def save_booking(
    passenger_name,
    age,
    gender,
    marital_status,
    source,
    destination,
    journey_date,
    boarding_time,
    arrival_date,
    arrival_time,
    coach,
    seat_count,
    meal,
    fare_per_seat,
    feedback
):

    pnr = generate_pnr()

    seats = generate_seats(
        coach,
        seat_count
    )

    total_fare = fare_per_seat * seat_count

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO bookings (

            pnr,

            passenger_name,
            age,
            gender,
            marital_status,

            source,
            destination,

            journey_date,
            boarding_time,

            arrival_date,
            arrival_time,

            coach,

            seat_count,
            seat_numbers,

            meal,

            fare_per_seat,
            total_fare,

            booking_status,

            feedback
        )

        VALUES (
            ?, ?, ?, ?, ?,
            ?, ?,
            ?, ?,
            ?, ?,
            ?,
            ?, ?,
            ?,
            ?, ?,
            ?,
            ?
        )
        """,

        (
            pnr,

            passenger_name,
            age,
            gender,
            marital_status,

            source,
            destination,

            str(journey_date),
            str(boarding_time),

            str(arrival_date),
            str(arrival_time),

            coach,

            seat_count,
            ",".join(map(str, seats)),

            ", ".join(meal),

            fare_per_seat,
            total_fare,

            "Confirmed",

            feedback
        )
    )

    conn.commit()
    conn.close()

    return pnr, seats, total_fare


# ============================================================
# GET BOOKING BY PNR
# ============================================================

def get_booking_by_pnr(pnr):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM bookings
        WHERE pnr = ?
        """,
        (pnr,)
    )

    booking = cursor.fetchone()

    conn.close()

    return booking


# ============================================================
# GET TOTAL BOOKINGS
# ============================================================

def get_total_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


# ============================================================
# GET TOTAL SEATS
# ============================================================

def get_total_seats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(seat_count), 0)
        FROM bookings
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


# ============================================================
# GET TOTAL REVENUE
# ============================================================

def get_total_revenue():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(total_fare), 0)
        FROM bookings
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


# ============================================================
# GET ALL BOOKINGS
# ============================================================

def get_all_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            pnr,
            passenger_name,
            source,
            destination,
            journey_date,
            coach,
            seat_numbers,
            total_fare,
            booking_status
        FROM bookings
        ORDER BY booking_id DESC
        """
    )

    bookings = cursor.fetchall()

    conn.close()

    return bookings


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 17px;
    color: #777777;
}

.section-title {
    font-size: 21px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 12px;
}

div.stButton > button {
    width: 100%;
    height: 45px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
}

div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    height: 48px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🚆 Railway Reservation")

st.sidebar.divider()

page = st.sidebar.radio(
    "Select Page",
    [
        "🎟️ Book Ticket",
        "🔎 Check Ticket",
        "📊 Booking Details"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Railway Reservation System"
)


# ============================================================
# PAGE 1 — BOOK TICKET
# ============================================================

if page == "🎟️ Book Ticket":

    with st.container(border=True):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        st.markdown(
            '<div class="main-title">'
            '🚆 Railway Reservation System'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sub-title">'
            'Passenger Details & Journey Booking'
            '</div>',
            unsafe_allow_html=True
        )

        st.divider()


        # ----------------------------------------------------
        # BOOKING FORM
        # ----------------------------------------------------

        with st.form("railway_booking_form"):

            # =================================================
            # PASSENGER DETAILS
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '👤 Passenger Details'
                '</div>',
                unsafe_allow_html=True
            )

            passenger_col1, passenger_col2 = st.columns(2)


            # LEFT BOX
            with passenger_col1:

                with st.container(border=True):

                    name = st.text_input(
                        "Passenger Name",
                        placeholder="Enter passenger name"
                    )

                    age = st.number_input(
                        "Age",
                        min_value=5,
                        max_value=105,
                        value=18
                    )

                    gender = st.selectbox(
                        "Gender",
                        [
                            "Male",
                            "Female",
                            "Other"
                        ]
                    )


            # RIGHT BOX
            with passenger_col2:

                with st.container(border=True):

                    marital_status = st.radio(
                        "Marital Status",
                        [
                            "Single",
                            "Married",
                            "Separated"
                        ],
                        horizontal=True
                    )

                    meal = st.multiselect(
                        "Meal Preference",
                        [
                            "Vada Pav",
                            "Misal",
                            "Pav Bhaji",
                            "Pulav"
                        ],
                        max_selections=2
                    )

                    feedback = st.feedback(
                        "stars"
                    )


            st.write("")


            # =================================================
            # JOURNEY DETAILS
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🚆 Journey Details'
                '</div>',
                unsafe_allow_html=True
            )

            journey_col1, journey_col2 = st.columns(2)


            # LEFT JOURNEY BOX
            with journey_col1:

                with st.container(border=True):

                    source = st.selectbox(
                        "From Station",
                        [
                            "Mumbai",
                            "Thane",
                            "Pune",
                            "Nashik",
                            "Nagpur"
                        ]
                    )

                    destination = st.selectbox(
                        "To Station",
                        [
                            "Mumbai",
                            "Thane",
                            "Pune",
                            "Nashik",
                            "Nagpur"
                        ]
                    )

                    journey_date = st.date_input(
                        "Journey Date"
                    )

                    boarding_time = st.time_input(
                        "Boarding Time"
                    )


            # RIGHT JOURNEY BOX
            with journey_col2:

                with st.container(border=True):

                    arrival_date = st.date_input(
                        "Arrival Date"
                    )

                    arrival_time = st.time_input(
                        "Arrival Time"
                    )

                    seat_count = st.number_input(
                        "Number of Seats",
                        min_value=1,
                        max_value=6,
                        value=1
                    )


            st.write("")


            # =================================================
            # COACH SELECTION
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🎫 Coach Selection'
                '</div>',
                unsafe_allow_html=True
            )

            coach = st.segmented_control(
                "Select Coach",
                [
                    "3 Tier",
                    "2 Tier",
                    "First Class",
                    "General"
                ],
                label_visibility="collapsed"
            )


            st.write("")


            # =================================================
            # BOOK BUTTON
            # =================================================

            submitted = st.form_submit_button(
                "🎟️ Confirm Booking"
            )


    # ========================================================
    # PROCESS BOOKING
    # ========================================================

    if submitted:

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if name.strip() == "":

            st.error(
                "Please enter passenger name."
            )

            st.stop()


        if source == destination:

            st.error(
                "From and To stations cannot be the same."
            )

            st.stop()


        if coach is None:

            st.error(
                "Please select a coach."
            )

            st.stop()


        # ----------------------------------------------------
        # FARE
        # ----------------------------------------------------

        fare_rates = {

            "General": 250,

            "3 Tier": 500,

            "2 Tier": 800,

            "First Class": 1200
        }

        fare_per_seat = fare_rates[coach]


        # ----------------------------------------------------
        # SAVE TO SQLITE
        # ----------------------------------------------------

        pnr, seats, total_fare = save_booking(

            passenger_name=name,

            age=age,

            gender=gender,

            marital_status=marital_status,

            source=source,

            destination=destination,

            journey_date=journey_date,

            boarding_time=boarding_time,

            arrival_date=arrival_date,

            arrival_time=arrival_time,

            coach=coach,

            seat_count=seat_count,

            meal=meal,

            fare_per_seat=fare_per_seat,

            feedback=feedback
        )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            "✅ Ticket booked successfully!"
        )


        # ----------------------------------------------------
        # CONFIRMATION
        # ----------------------------------------------------

        with st.container(border=True):

            st.subheader(
                "🎟️ Booking Confirmation"
            )

            st.divider()

            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**PNR:** `{pnr}`"
                )

                st.write(
                    f"**Passenger:** {name}"
                )

                st.write(
                    f"**From:** {source}"
                )

                st.write(
                    f"**To:** {destination}"
                )

                st.write(
                    f"**Coach:** {coach}"
                )


            with col2:

                st.write(
                    f"**Seats:** "
                    f"{', '.join(map(str, seats))}"
                )

                st.write(
                    f"**Number of Seats:** "
                    f"{seat_count}"
                )

                st.write(
                    f"**Fare / Seat:** "
                    f"₹{fare_per_seat}"
                )

                st.write(
                    f"**Total Fare:** "
                    f"₹{total_fare:,.2f}"
                )


        st.info(
            f"🔐 Your PNR is {pnr}. "
            "Use this PNR on the Check Ticket page."
        )


# ============================================================
# PAGE 2 — CHECK TICKET
# ============================================================

elif page == "🔎 Check Ticket":

    st.title("🔎 Check Booked Ticket")

    st.write(
        "Enter your PNR number to retrieve your booking."
    )

    st.divider()


    with st.container(border=True):

        pnr = st.text_input(
            "PNR Number",
            placeholder="Enter 10-digit PNR"
        )

        search = st.button(
            "🔎 Search Ticket"
        )


    if search:

        if pnr.strip() == "":

            st.warning(
                "Please enter a PNR number."
            )

        else:

            booking = get_booking_by_pnr(
                pnr.strip()
            )


            if booking is None:

                st.error(
                    "❌ No booking found for this PNR."
                )


            else:

                (
                    booking_id,
                    pnr,
                    passenger_name,
                    age,
                    gender,
                    marital_status,
                    source,
                    destination,
                    journey_date,
                    boarding_time,
                    arrival_date,
                    arrival_time,
                    coach,
                    seat_count,
                    seat_numbers,
                    meal,
                    fare_per_seat,
                    total_fare,
                    booking_status,
                    feedback,
                    booking_date

                ) = booking


                st.success(
                    "✅ Booking found successfully!"
                )


                # ==========================================
                # TICKET
                # ==========================================

                with st.container(border=True):

                    st.subheader(
                        f"🎟️ Railway Ticket | PNR: {pnr}"
                    )

                    st.divider()


                    # --------------------------------------
                    # PASSENGER
                    # --------------------------------------

                    st.markdown(
                        "### 👤 Passenger Details"
                    )

                    col1, col2 = st.columns(2)


                    with col1:

                        st.write(
                            f"**Passenger Name:** "
                            f"{passenger_name}"
                        )

                        st.write(
                            f"**Age:** {age}"
                        )

                        st.write(
                            f"**Gender:** {gender}"
                        )


                    with col2:

                        st.write(
                            f"**Marital Status:** "
                            f"{marital_status}"
                        )

                        st.write(
                            f"**Meal:** "
                            f"{meal if meal else 'No meal'}"
                        )


                    st.divider()


                    # --------------------------------------
                    # JOURNEY
                    # --------------------------------------

                    st.markdown(
                        "### 🚆 Journey Details"
                    )

                    col1, col2 = st.columns(2)


                    with col1:

                        st.write(
                            f"**From:** {source}"
                        )

                        st.write(
                            f"**To:** {destination}"
                        )

                        st.write(
                            f"**Journey Date:** "
                            f"{journey_date}"
                        )

                        st.write(
                            f"**Boarding Time:** "
                            f"{boarding_time}"
                        )


                    with col2:

                        st.write(
                            f"**Arrival Date:** "
                            f"{arrival_date}"
                        )

                        st.write(
                            f"**Arrival Time:** "
                            f"{arrival_time}"
                        )

                        st.write(
                            f"**Coach:** {coach}"
                        )


                    st.divider()


                    # --------------------------------------
                    # SEAT & FARE
                    # --------------------------------------

                    st.markdown(
                        "### 💺 Seat & Fare Details"
                    )

                    col1, col2, col3 = st.columns(3)


                    with col1:

                        st.metric(
                            "Seats Booked",
                            seat_count
                        )


                    with col2:

                        st.metric(
                            "Seat Numbers",
                            seat_numbers
                        )


                    with col3:

                        st.metric(
                            "Total Fare",
                            f"₹{total_fare:,.2f}"
                        )


                    st.write(
                        f"**Fare per Seat:** "
                        f"₹{fare_per_seat:,.2f}"
                    )

                    st.write(
                        f"**Booking Status:** "
                        f"{booking_status}"
                    )

                    st.write(
                        f"**Booking Date:** "
                        f"{booking_date}"
                    )


# ============================================================
# PAGE 3 — BOOKING DETAILS
# ============================================================

else:

    st.title("📊 Booking Details")

    st.write(
        "Live information retrieved from SQLite3."
    )

    st.divider()


    # ========================================================
    # STATISTICS
    # ========================================================

    total_bookings = get_total_bookings()

    total_seats = get_total_seats()

    total_revenue = get_total_revenue()


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🎟️ Total Bookings",
            total_bookings
        )


    with col2:

        st.metric(
            "💺 Total Seats Booked",
            total_seats
        )


    with col3:

        st.metric(
            "💰 Total Revenue",
            f"₹{total_revenue:,.2f}"
        )


    st.divider()


    # ========================================================
    # ALL BOOKINGS
    # ========================================================

    st.subheader(
        "📋 Booking Records"
    )


    bookings = get_all_bookings()


    if bookings:

        st.dataframe(

            bookings,

            column_config={

                "pnr": "PNR",

                "passenger_name": "Passenger",

                "source": "From",

                "destination": "To",

                "journey_date": "Journey Date",

                "coach": "Coach",

                "seat_numbers": "Seats",

                "total_fare": "Total Fare",

                "booking_status": "Status"
            },

            hide_index=True,

            use_container_width=True
        )


    else:

        st.info(
            "No tickets have been booked yet."
        )


