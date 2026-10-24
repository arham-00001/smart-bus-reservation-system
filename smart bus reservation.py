import json
try:
    with open("bookings.json","r") as file:
        bookings = json.load(file)
except FileNotFoundError:
    bookings = []
routes = [
    {
        "id": 1,
        "from": "Karachi",
        "to": "Hyderabad",
        "fare": 800,
        "seats": 40,
        "departure": "08:00 AM"
    },
    {
        "id": 2,
        "from": "Karachi",
        "to": "Lahore",
        "fare": 3500,
        "seats": 40,
        "departure": "10:00 AM"
    },
    {
        "id": 3,
        "from": "Lahore",
        "to": "Islamabad",
        "fare": 1200,
        "seats": 35,
        "departure": "09:00 AM"
    },
    {
            "id": 4,
            "from": "Lahore",
            "to": "Rawalpindi",
            "fare": 2000,
            "seats": 50,
            "departure": "11:30 AM"
    },
    {
            "id": 5,
            "from": "Islamabad",
            "to": "Multan",
            "fare": 4000,
            "seats": 55,
            "departure": "12:00 PM"
    }
]

print("===================================")
print("   SMART BUS RESERVATION SYSTEM")
print("===================================")

print("1. View Available Routes")
print("2. Search for a Route")
print("3. Book a Ticket")
print("4. View My Bookings")
print("5. Cancel a Booking")
print("6. View Seat Availability")
print("7. Generate Booking Report")
print("8. Exit")

choice = input("Enter your choice: ")

if choice == "1":
    print("\nAVAILABLE BUS ROUTES")
    for route in routes:
        print("----------------------------")
        print("Route ID:", route["id"])
        print("From:", route["from"])
        print("To:", route["to"])
        print("Fare: Rs.", route["fare"])
        print("Available Seats:", route["seats"])
        print ("Departure:", route["departure"])
elif choice == "2":
    city = input("Enter departure city: ").strip().lower()

    found = False

    for route in routes:
        if route["from"].lower() == city:
            print("----------------------------")
            print("Route ID:", route["id"])
            print("From:", route["from"])
            print("To:", route["to"])
            print("Fare: Rs.", route["fare"])
            print("Available Seats:", route["seats"])
            print ("Departure:", route["departure"])
            found = True

    if not found:
        print("Sorry, no routes found from this city.")
elif choice == "3":
    route_id = int(input("Enter route ID: "))
    name = input("Enter passenger name: ").capitalize()
    for route in routes:
        if route["id"] == route_id:
            if route["seats"] > 0:
                route["seats"] -= 1
                bookings.append({
                    "name" : name,
                    "route": route["from"]+ " " + "To" + " " + route["to"],
                    "fare" : route["fare"],
                    "departure" : route["departure"]
                })

                with open("bookings.json",'w') as file:
                    json.dump(bookings, file, indent=4)

                print ("Ticket booked successfully")
                print ("Passenger", name)
                print ("Route: from", route["from"], "to", route["to"])
                print ("Fare: Rs", route["fare"])
                print ("Departure:", route["departure"])
            else:
                print ("Sorry no seats available")
            break
    else:
            print ("Invalid route ID")
elif choice == "4":
    if len(bookings) == 0:
        print ("No bookings found")
    else:
        for booking in bookings:
            print ("----------------")
            print ("Passenger", booking["name"])
            print ("Route:", booking['route'])
            print ("Fare: Rs", booking['fare'])
            print ("Departure:", booking["departure"])
elif choice == "5":
    if len(bookings) == 0:
        print("No bookings to cancel.")
    else:
        for i, booking in enumerate(bookings):
            print(i + 1, booking["name"], "-", booking["route"])

        number = int(input("Enter booking number to cancel: "))

        if 1 <= number <= len(bookings):
            cancelled = bookings.pop(number - 1)

            with open("bookings.json", "w") as file:
                json.dump(bookings, file, indent=4)

            print("Booking cancelled for:", cancelled["name"])
        else:
            print("Invalid booking number.")
elif choice == "6":
    for route in routes:
        print ("------------")
        print ("Route:", route['from'], "to", route["to"])
        print ("Available seats:", route["seats"])
        print ("Departure:", route["departure"])
elif choice == "7":
    print ("==========BOOKING REPORT==========")
    print ("Total Bookings:", len(bookings))

    totalfare = 0
    for booking in bookings:
        totalfare += booking["fare"]

    print ("Total Revenue: Rs", totalfare)
elif choice == "8":
    print ("Thank you for using Smart Bus Reservation System!")
    print ("Goodbye")