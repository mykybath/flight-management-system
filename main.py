from db import get_connection

conn = get_connection()
c = conn.cursor()

#I HAVE LEFT THESE SELECT QUERIES HERE SO YOU CAN EASILY SEE THEM WHEN TESTING THE FUNCTIONS
c.execute("SELECT * FROM Pilot WHERE LicenseNumber = 'I12345678';")
print(c.fetchone())
c.execute("SELECT * FROM Destination WHERE DestinationID = '1';")
print(c.fetchone())
c.execute("SELECT * FROM Flight WHERE Status = 'Delayed';")
#this one looks like it has repeated values 
#but it is just the arrdestid,depdestid, copid, capid input data
print(c.fetchone())
c.execute("SELECT * FROM WorkSchedule WHERE PilotID = '9';")
print(c.fetchone())

def menu(): #created menu function 
    print("[1] Add Flight")
    print("[2] View Flight by Criteria")
    print("[3] Update Flight")
    print("[4] Assign Pilot to Flight")
    print("[5] View Pilot Schedule")
    print("[6] View/Update Destination")
    print("[7] Add New Destination")
    print("[8] Delete Pilot")
    print("[9] Add Pilot")
    print("[10] Exit")
menu()
option = int(input("Enter Option:"))


def addflight():  # add flight function to insert new flights
    FlightNumber = input("Enter Flight Number:")
    DepartureTime = input("Enter departure time:")
    ArrivalTime = input("Enter arrival time:")
    DepartureDate = input("Enter departure date:")
    ArrivalDate = input("Enter arrival date:")
    Capacity = input("Enter Total Seat Capacity:")
    DepartureCity = input("Enter Departure City:")
    DepartureAirport = input("Enter Airport CODE:") 
    ArrivalCity = input("Enter Arrival City:")
    ArrivalAirport = input("Enter Arrival Airport:") #ididnt include pilot prompts as this ca nbe assinged later
    # Checking destinationid for matching city and airport as specified by user
    c.execute("""SELECT COUNT(DestinationID) FROM Destination WHERE City = ? AND Airport = ?""",
    (DepartureCity, DepartureAirport)) #? act as placeholders for user input
    #sql query to count how many rows in destination match the user input for city airport
    dep = c.fetchone()[0] #accessing value of count
    if dep == 0: #if no rows match
        print("No destination found for departure - please update destination records first")
        return
    # same for arrival destination
    c.execute("""SELECT COUNT(DestinationID) FROM Destination WHERE City = ? AND Airport = ?""", 
    (ArrivalCity, ArrivalAirport))
    arr = c.fetchone()[0]
    if arr == 0:
        print("No destination found for arrival - please update destination records first")
        return
    Status = input("Enter Current Status (Scheduled/Cancelled/Delayed):") #it needs to be one of these due to check constraint upon table creation
    # Insertng the data into the flight table
    #inner join required as city aiport data used from destination - can inner join the depart/arr ids to the dest data
    c.execute("""
    INSERT INTO Flight (FlightNumber, DepartureTime, DepartureDate, ArrivalTime, ArrivalDate, Capacity, Status, ArrivalDestinationID, DepartureDestinationID)
    SELECT ?, ?, ?, ?, ?, ?, ?, dep.DestinationID AS DepartureDestinationID, arr.DestinationID AS ArrivalDestinationID
    FROM Destination dep
    INNER JOIN Destination arr 
    ON dep.City = ? AND dep.Airport = ? 
    AND arr.City = ? AND arr.Airport = ?""", (FlightNumber, DepartureTime, DepartureDate, ArrivalTime, ArrivalDate, Capacity, 
    Status, DepartureCity, DepartureAirport, ArrivalCity, ArrivalAirport))
    conn.commit() #ALWAYS NEED TO COMMIT CHANGES
    print("Flight added successfully - please now assign pilot and/or copilot from menu.")

    

#OPTION 2 VIEW FLIGHT BY ONE CRITERIA - Sorry i couldnt do it for multiple criteria
def viewflight():
    criteria = input("Enter flight details: DEPARTURE DATE, STATUS, FLIGHT NUMBER, FROM, TO, FROM:").upper() #asks user to specify criteria first
    if criteria == "DEPARTURE DATE":
        depdate = input("Enter Departure Date (YYYY-MM-DD): ")#user can enter the value for the criteria they are searching
        c.execute("""SELECT * FROM Flight WHERE DepartureDate = ?""",(depdate,))   
    elif criteria == "STATUS":
        status = input("Enter Status (Scheduled/Cancelled/Delayed): ")
        c.execute("""SELECT * FROM Flight WHERE Status = ?""",(status,))
    elif criteria == "FLIGHT NUMBER":
        flightnum = input("Enter Flight Number: ")
        c.execute("""SELECT * FROM Flight WHERE FlightNumber = ?""",(flightnum,))
    elif criteria == "TO":
        dest = input("Enter Destination Country: ")
        #sql queries to select to view by critiera - inner joins done again for dest and flight link by foreing key arrdest id 
        c.execute("""SELECT 
        Flight.Status, 
        Flight.FlightNumber, 
        Destination.DestinationCountry, 
        Destination.City 
        FROM Flight
        INNER JOIN 
        Destination ON Flight.ArrivalDestinationID = Destination.DestinationID 
        WHERE Destination.DestinationCountry = ?;""", 
        (dest,))
    elif criteria == "FROM":
        fromcountry = input("Enter Country of Departure:")   
        c.execute("""
        SELECT Flight.Status, Flight.FlightNumber,Destination.DestinationCountry, 
        Destination.City 
        FROM Flight
        INNER JOIN 
        Destination ON Flight.DepartureDestinationID = Destination.DestinationID 
        WHERE Destination.DestinationCountry = ?;
        """, (fromcountry,))
    else:
        print("Criteria not found")
        return
    flights = c.fetchall()
    print("Flights found:")
    for flight in flights:
        print(flight)



#option3 update flight info
def updateflight():
    flightnum = input("Enter Flight number: ")
    c.execute("SELECT COUNT(*) FROM Flight WHERE FlightNumber = ?", (flightnum,))
    flight_exists = c.fetchone()[0]
    if flight_exists == 0:
        print("Error: Flight number does not exist.")
        return
    c.execute("SELECT * FROM Flight WHERE FlightNumber = ?", (flightnum,))
    flight = c.fetchone()
    updflightnum = input("Enter updated flight number: (original: {}) ".format(flight[1])) or flight[1] #if no update the user can leave it blank and it will keep original value - flight[1] used to access value of first row in Flight
    upddeptime = input("Enter updated departure time: (original: {}) ".format(flight[2])) or flight[2]
    updepdate = input("Enter Updated Departure Date: (original: {}) ".format(flight[3])) or flight[3]
    uparrtime = input("Enter Updated Arrival Time: (original: {}) ".format(flight[4])) or flight[4]
    updarrdate = input("Enter Updated arrival Date: (original: {}) ".format(flight[5])) or flight[5]
    updcapacity = input("Enter Updated Capacity: (original: {}) ".format(flight[6])) or flight[6]
    updstatus = input("Enter Updated Status: (original: {}) ".format(flight[7])) or flight[7]
    updarrdestid = input("Enter Updated arrival Destination ID: (original: {}) ".format(flight[8])) or flight[8]
    updeptdestid = input("Enter Updated Departure Destination ID: (original: {}) ".format(flight[9])) or flight[9]
    updCaptain = input("Enter Updated Captain ID: (original: {}) ".format(flight[10])) or flight[10] #can update if want to if not can leave it as is 
    updcopilot = input("Enter Updated CoPilot ID: (original: {}) ".format(flight[11])) or flight[11]
    #sql query to update and set the attributes to the new ones using ? placeholders specified by user
    c.execute("""UPDATE Flight SET FlightNumber = ?, DepartureTime = ?, DepartureDate = ?, ArrivalTime = ?, 
    ArrivalDate = ?, Capacity = ?, Status = ?, ArrivalDestinationID = ?, DepartureDestinationID = ?, CaptainID = ?, CoPilotID = ?
    WHERE FlightNumber = ?""", (updflightnum, upddeptime, updepdate, uparrtime, updarrdate, updcapacity, updstatus, updarrdestid, updeptdestid, updCaptain, updcopilot, flightnum))

    conn.commit()

    c.execute("SELECT * FROM Flight WHERE FlightNumber = ?", (updflightnum,))
    updated_flight = c.fetchone()
    if updated_flight:
        print("Flight updated successfully", updated_flight)
    else:
        print("Flight not found")




#option 4 assigning a pilot to a flight
def assignpilot():
    c.execute("""SELECT * FROM Flight Where CaptainID IS NULL""")
    print("These flights have no captain assigned", c.fetchall()) #this sql select query allows the user to first see what flights have no captain yet - there will be some as it is not asked for in the addflight function
    FlightNumber = input("Enter Flight Number: ")
    DepartureTime = input("Enter Departure Time: ")
    DepartureDate = input("Enter Departure Date: ")
    #this sql query selects the flight based on the prompted info from user
    c.execute("""SELECT Flight.FlightNumber, 
    Flight.DepartureTime, 
    Flight.DepartureDate
    FROM Flight 
    WHERE Flight.FlightNumber = ? 
    AND Flight.DepartureTime = ? 
    AND Flight.DepartureDate = ?;""", 
    (FlightNumber, DepartureTime, DepartureDate))
    data = c.fetchall() #retrieves it
    
    if data:  
        print("Flight exists")
        CapName = input("Enter Captain First Name: ") #get captain details
        CapLastName = input("Enter Captain Last Name: ")
        CapEmail = input("Enter Captain Email Address: ")
        #need to get pilotid as this filed exists in flight not the prompts
        c.execute("""SELECT PilotID FROM Pilot 
        WHERE FirstName = ? AND LastName = ? AND Email = ?;""", 
        (CapName, CapLastName, CapEmail))
        pilotdata = c.fetchone() #retrieves the pilot
        if pilotdata: 
            CaptainID = pilotdata[0]  # ACCessing pilot id 
            print("Pilot found.")
            #updating flight where db matches user inputs
            c.execute("""UPDATE Flight SET CaptainID = ?
            WHERE FlightNumber = ? 
            AND DepartureTime = ? 
            AND DepartureDate = ?;""", 
            (CaptainID, FlightNumber, DepartureTime, DepartureDate))
            conn.commit()
            print("Captain assigned to flight")
        else:  
            print("Pilot not found")
    else:  
        print("No results found for the flight")

    


def viewpilotschedule():
    # Get pilot info from user
        FirstName = input("Enter pilot first name: ")
        LastName = input("Enter pilot last name: ")
        #sql query - returns pilot info, flight info asosciared with pilot, and wokr schedule info - 2 inner joins done to get all the info
        c.execute("""SELECT 
        Pilot.FirstName, 
        Pilot.LastName, 
        WorkSchedule.Dayoftheweek, 
        WorkSchedule.StartTime, 
        WorkSchedule.EndTime, 
        Flight.DepartureDate,
        Flight.ArrivalDate,
        Flight.FlightNumber
        FROM Pilot 
        INNER JOIN WorkSchedule ON Pilot.PilotID = WorkSchedule.PilotID 
        INNER JOIN Flight ON Flight.CaptainID = Pilot.PilotID OR Flight.CoPilotID = Pilot.PilotID 
        WHERE Pilot.FirstName = ? AND Pilot.LastName = ?;
        """, (FirstName, LastName))  
        Pilotschedule = c.fetchall() #returns all their work schedules - differs by day 
        if Pilotschedule:
            for data in Pilotschedule:
                print(data)
        else:
            print("No results found")


# def viewdestination():
#     # Get pilot info from user
#     DestinationCountry = input("Enter Destination:")
#     City = input("Enter City")
#     DestinationCountry = input("Enter Destination:")
#     Airport = input("Enter Airport")
#     DestinationCountry = input("Enter Destination:")
#     Timezone = input("Enter Timezone")
#     c.execute("SELECT * FROM Destination WHERE DestinationCountry = ?, Destination.City = ?, Destination." (DestinationCountry,))
#     destination = c.fetchall()
#     print(destination)
    
#option 5 updating the destination for a flight
def updatedestforflight():
    flightnum = input("Enter Flight Number: ") #updates upon getting flight number
    c.execute("SELECT COUNT(*) FROM Flight WHERE FlightNumber = ?", (flightnum,))
    flightexists = c.fetchone()[0] #maks sure it exists fitst by using select count - counts matches 
    if flightexists == 0:
        print("Error: Flight number not found")
        return
    if flightexists > 1:
        print("Flight Number references more than one flight: Flight ID required") #the user can input flight id here if needed - i did this as it would probs require higher up authorisation to update a flight 
        flightid = input("Enter FlightID: ")
    else:
        flightid = flightnum
    c.execute("""SELECT * FROM Flight WHERE FlightNumber = ? AND FlightID = ?""", 
    (flightnum, flightid)) #SELECTS MATCHING FLIGHTS FOR BOTH HERE 
    destination = c.fetchone()
    if destination:
        print("Destination details:", destination)
        flightnum = flightid 
    else:
        print("Error: No flight found")
    checkdest = input("Update ARRIVAL or DEPARTURE: ").upper() #the user has to enter uppercase ARRIVAL ETC
    updcountry = input("Enter country (leave blank if no update): ")
    updcity = input("Enter city (leave blank if no update): ")
    updairport = input("Enter updated airport (leave blank if no update): ")
    updtimezone = input("Enter updated timezone (leave blank if no update): ")

    if checkdest == "ARRIVAL": #if checkdest = uppercase arrival it will update arrival dest
        if updcountry:
            c.execute("""UPDATE Destination
            SET DestinationCountry = ?
            WHERE DestinationID = (SELECT ArrivalDestinationID FROM Flight WHERE FlightNumber = ?)""", 
            (updcountry, flightnum))
            conn.commit()  
        if updcity: #done multiple if statements to update each individually if required
            c.execute("""UPDATE Destination 
            SET City = ?
            WHERE DestinationID = (SELECT ArrivalDestinationID FROM Flight WHERE FlightNumber = ?)""", (updcity, flightnum))
            conn.commit()  
        if updairport:
            c.execute("""UPDATE Destination
            SET Airport = ?
            WHERE DestinationID = (SELECT ArrivalDestinationID FROM Flight WHERE FlightNumber = ?)""", 
            (updairport, flightnum))
            conn.commit()  
        if updtimezone:
            c.execute("""UPDATE Destination
            SET Timezone = ?
            WHERE DestinationID = (SELECT ArrivalDestinationID FROM Flight WHERE FlightNumber = ?)""", 
            (updtimezone, flightnum))
            conn.commit()  
        print("Arrival destination updated")
        #same for departure
    elif checkdest == "DEPARTURE":
        if updcountry:
            c.execute("""UPDATE Destination
            SET DestinationCountry = ?
            WHERE DestinationID = (SELECT DepartureDestinationID FROM Flight WHERE FlightNumber = ?)""", 
            (updcountry, flightnum))
            conn.commit()  
        if updcity:
            c.execute("""UPDATE Destination
            SET City = ?
            WHERE DestinationID = (SELECT DepartureDestinationID FROM Flight WHERE FlightNumber = ?)""", 
            (updcity, flightnum))
            conn.commit()  
        if updairport:
            c.execute("""UPDATE Destination
            SET Airport = ?
            WHERE DestinationID = (SELECT DepartureDestinationID FROM Flight WHERE FlightNumber = ?)""", 
            (updairport, flightnum))
            conn.commit()  
        if updtimezone:
            c.execute("""UPDATE Destination
            SET Timezone = ?
            WHERE DestinationID = (SELECT DepartureDestinationID FROM Flight WHERE FlightNumber = ?)""", 
            (updtimezone, flightnum))
            conn.commit()  
        print("Departure destination updated")  
    else:
        print("Invalid option - please enter either 'ARRIVAL' or 'DEPARTURE'")
        return
    c.execute("""
    SELECT * FROM Destination
    WHERE DestinationID = (SELECT ArrivalDestinationID FROM Flight WHERE FlightNumber = ?
    UNION
    SELECT DepartureDestinationID FROM Flight WHERE FlightNumber = ?)""", 
    (flightnum, flightnum))
    
    updated_dest = c.fetchone()
    if updated_dest:
        print("Updated destination:", updated_dest)
    else:
        print("Error: No destination found")


#option 6 adding a new destination
def adddest():
    Country = input("Enter Country: ")
    City = input("Enter City: ")
    Airport = input("Enter Airport: ")
    Timezone = input("Enter TimeZone: ")
    #first checks if destination already exists
    c.execute("""SELECT DestinationID FROM Destination
    WHERE DestinationCountry = ? AND City = ? AND Airport = ? AND Timezone = ?""", 
    (Country, City, Airport, Timezone))
    destinationexists = c.fetchone() #destination id retrieval
    if destinationexists:
        print(f"Destination already exists: DestinationID = {destinationexists[0]}.")
        return destinationexists[0]
    else:
        c.execute("""INSERT INTO Destination (DestinationCountry, City, Airport, Timezone) VALUES (?, ?, ?, ?)""", 
        (Country, City, Airport, Timezone))
        conn.commit()
        new_destination_id = c.lastrowid #this gets the rowid in this case the destinationid as it is primary key for the last insert statement
        print(f"New destination created: DestinationID = {new_destination_id}.")
        return new_destination_id  

#option 7 in case a pilot quits or is fired and want to delete them from records so wont be assigned to any new flights
def delpilot():
    licenseno = input("Enter License Number:").strip() #i added .strip as had issues with testing the example data - accounts for spaces etc
    pfn = input("Enter first name:").strip()
    pln = input("Enter last name:").strip()
    ema = input("Enter email:").strip()
    phon = input("Enter phone number:").strip()
    address = input("Enter address:").strip()
    #checking if pilot exists
    c.execute("""SELECT * FROM Pilot WHERE LicenseNumber = ? AND FirstName = ? AND LastName = ? 
    AND Email = ? AND PhoneNumber = ? AND Address = ?""",
    (licenseno, pfn, pln, ema, phon, address)) #
    pildata = c.fetchone()  
    if pildata:
        print(pildata) #prints the pilot data so user can see it as one last double check
        confirm = input("Are you sure you want to delete this pilot from the records? Y/N: ").upper() #asks user to confirm to prevent wrong deletions
        if confirm == 'Y':
            #delete sql query used to delete from table 
            c.execute("""DELETE FROM Pilot WHERE LicenseNumber = ? AND FirstName = ? AND LastName = ? AND Email = ? AND PhoneNumber = ? AND Address = ?""",
            (licenseno, pfn, pln, ema, phon, address))
            conn.commit()
            print("Pilot deleted")
        elif confirm == 'N':
            print("Pilot info deletion canceled")
        else:
            print("Invalid option - please enter 'Y' or 'N'")
    else:
        print("No pilot found")



#option 9 may also want to add new pilots that have been hired
def addpilot():
    licenseno = input("Enter License Number:")
    pfn = input("Enter first name:")
    pln = input("Enter last name:")
    ema = input("Enter email:")
    phon = input("Enter phone number:")
    address = input("Enter address:") #need all info, pilot id isnt needed as it is integer primary key - set automatically
    c.execute("""INSERT INTO Pilot(LicenseNumber, FirstName, LastName, PhoneNumber, Email, Address) VALUES (?, ?, ?, ?, ?, ?)""",
    (licenseno, pfn, pln, ema, phon, address))
    conn.commit()
    newpilotid = c.lastrowid #get the pilotid of the newly inserted pilot so can print it nicely
    c.execute("SELECT * FROM Pilot WHERE PilotID = ?", (newpilotid,)) #sql statement to retrieve the newpilot info from the new pilotid
    newpilot = c.fetchone() 
    print("New pilot added", newpilot) #printed it so user can see if it is all ok 
    
    

def menu():
    print("[1] Add Flight")
    print("[2] View Flight by Criteria")
    print("[3] Update Flight")
    print("[4] Assign Pilot to Flight")
    print("[5] View Pilot Schedule")
    print("[6] View/Update Destination")
    print("[7] Add New Destination")
    print("[8] Delete Pilot")
    print("[9] Add Pilot")
    print("[10] Exit")
while True:
        if option == 1:
            addflight()
        elif option == 2:
            viewflight()
        elif option == 3:
            updateflight()
        elif option == 4:
            assignpilot()
        elif option == 5:
            viewpilotschedule()
        elif option == 6:
            updatedestforflight()
        elif option == 7:
            adddest()
        elif option == 8:
            delpilot()
        elif option == 9: 
            addpilot()
        elif option == 10:
            print("Exiting Menu")
            break
        else:
            print("Invalid Option")
        menu()
        option = int(input("Enter your option: ")) #will go back to menu after completing option