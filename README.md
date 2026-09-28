# 🚆 Railway Reservation System

A database-driven Railway Reservation System built using **Python, Streamlit, and SQLite3**.

The application allows users to book railway tickets, automatically generate a PNR number, assign seats, calculate fares, store booking information in SQLite3, and retrieve previously booked tickets using the PNR number.

---

## 📌 Project Overview

The Railway Reservation System is a Streamlit-based web application connected to a SQLite3 database.

The application provides three main functionalities:

1. 🎟️ Book Ticket
2. 🔎 Check Ticket using PNR
3. 📊 View Booking Details

All booking information entered by the user is stored permanently in the SQLite3 database.

---

## ✨ Features

### 🎟️ Book Ticket

Users can enter:

- Passenger Name
- Age
- Gender
- Marital Status
- Source Station
- Destination Station
- Journey Date
- Boarding Time
- Arrival Date
- Arrival Time
- Coach Type
- Number of Seats
- Meal Preference
- Feedback

After submitting the booking:

- A unique PNR number is generated.
- Seat numbers are automatically assigned.
- Fare is calculated according to the selected coach.
- Total fare is calculated based on the number of seats.
- All booking details are stored in SQLite3.
- Booking confirmation is displayed to the user.

---

### 🔎 Check Booked Ticket

Users can enter their PNR number to retrieve their ticket.

The application displays:

- PNR Number
- Passenger Details
- Journey Details
- Coach
- Seat Numbers
- Number of Seats
- Meal Preference
- Fare per Seat
- Total Fare
- Booking Status
- Booking Date

The information is retrieved directly from the SQLite3 database.

---

### 📊 Booking Details

The application provides an overview of stored bookings.

It displays:

- Total Bookings
- Total Seats Booked
- Total Revenue
- Complete Booking Records

The information is calculated using SQL queries on the SQLite3 database.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application logic |
| Streamlit | Web application frontend |
| SQLite3 | Database |
| SQL | Data storage and retrieval |

---

## 🗂️ Project Structure

```text
Railway_Reservation/
│
├── app.py
├── railway.db
└── README.md



[alt text](<diagram (1).png>)