Flight Management Database

This project is a relational database system built using SQLite and Python.
It models a flight management system that stores and manages data for pilots, destinations, flights, and work schedules.

The project demonstrates practical database design, SQL querying, and integration with a Python application.

Database Design

The system consists of four related tables:

Pilot

Stores pilot details including contact information.

PilotID (Primary Key)

LicenseNumber

FirstName

LastName

PhoneNumber

Email

Address

Destination

Stores airport and location information.

DestinationID (Primary Key)

DestinationCountry

City

Airport

TimeZone

Flight

Stores flight records and connects pilots and destinations.

FlightID (Primary Key)

FlightNumber

Departure & Arrival Date/Time

Capacity

Status (Scheduled, Cancelled, Delayed)

ArrivalDestinationID (Foreign Key)

DepartureDestinationID (Foreign Key)

CaptainID (Foreign Key)

CoPilotID (Foreign Key)

Includes:

Multiple foreign key relationships

CHECK constraint to enforce valid flight status values

WorkSchedule

Stores pilot scheduling information.

WorkScheduleID (Primary Key)

PilotID (Foreign Key)

DayOfTheWeek

StartTime

EndTime

TotalHours

Technical Skills Demonstrated

Relational schema design

Primary and foreign key implementation

Data integrity constraints

SQL (SELECT, INSERT, JOIN, GROUP BY)

CRUD operations via Python

Database reproducibility using schema and seed files

Version control using Git

Project Structure
flight.py         # Main Python application (CRUD functionality)
schema.sql        # Database structure
seed_data.sql     # Sample data
.gitignore        # Excludes database file
README.md         # Documentation

How To Run
1. Create the database
sqlite3 flight.db < schema.sql
2. Insert sample data
sqlite3 flight.db < seed_data.sql
3. Run the application
python flight.py
