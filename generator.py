import random


def bank_name():
    cardinal_directions = [
        "North",
        "South",
        "East",
        "West",
        "Northeast",
        "Southwest",
        "Northwest",
        "Southeast",
        "Midwest",
    ]

    fluff = [
        "First",
        "Second",
        "Freedom",
        "Liberty",
        "Tricounty",
        "Tri-state Area",
        "United",
        "National",
        "International",
        "Federal",
        "Central",
        "Citizens",
        "Pacific",
        "Atlantic",
        "Valley",
    ]

    middle = [
        "Trust",
        "Credit Union",
        "Financial",
        "Community Mutual",
        "Reserve",
        "Fund",
        "Bank",
        "Investment Solutions",
        "Group",
        "Mutual",
        "Financial Corporation",
        "Financial Group",
        "Holdings",
    ]

    state_names = [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
        "America",
    ]

    cities = [
        "Lincoln",
        "Detroit",
        "San Francisco",
        "Houston",
        "Akron",
        "Modesto",
        "Wichita",
        "Honolulu",
        "Tampa",
        "Las Vegas",
        "El Paso",
        "Tulsa",
        "Toledo",
        "Kansas City",
        "Anchorage",
        "St. Paul",
        "Anaheim",
        "Birmingham",
        "Atlanta",
        "St. Louis",
    ]

    choice = random.randint(1, 5)
    bank = ""

    # TODO fix possibilities of generating "Federal Reserve" specifically
    # TODO fix contradictory names like "Federal/National/International Bank of Kansas"

    if choice < 3:

        flags = {
            "add_direction": random.random() < 0.25,
            "add_middle": random.random() < 0.5,
            "add_state": random.random() < 0.4,
        }

        if flags["add_direction"]:
            bank += f"{random.choice(cardinal_directions)} "

        fluff = random.choice(fluff)

        bank += f"{fluff} "

        bank += random.choice(middle)

        if flags["add_state"] and fluff not in ["National", "International", "Federal"]:
            bank += f" of {random.choice(state_names)}"
    else:
        # bank name based on city

        if random.random() < 0.35:
            bank += random.choice(cardinal_directions)

            if random.random() < 0.5:
                bank += "ern"

            bank += " "

        bank += f"{random.choice(cities)} {random.choice(middle)}"

    return bank
