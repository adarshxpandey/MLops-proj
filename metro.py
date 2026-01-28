# Approximate distance (km) to nearest metro station
# These are rough but realistic values

METRO_DISTANCE = {
    "Whitefield": 0.5,
    "Indiranagar": 0.3,
    "MG Road": 0.2,
    "Yelahanka": 3.0,
    "Electronic City": 4.5,
    "Marathahalli": 1.2,
    "BTM Layout": 1.8,
    "other": 2.5
}

def get_metro_distance(location):
    return METRO_DISTANCE.get(location, METRO_DISTANCE["other"])
