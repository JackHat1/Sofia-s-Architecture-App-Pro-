import pandas as pd
import json
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

EXCEL_FILE = 'Παραδείγματα_Κτιρίων excel .xlsx'

print("🔄 Φόρτωση δεδομένων από το Excel...")
df = pd.read_excel(EXCEL_FILE)

geolocator = Nominatim(user_agent="sofias_architecture_app")
buildings_data = []

def get_coordinates(address):
    try:
        search_query = f"{address}, Athens, Greece"
        location = geolocator.geocode(search_query, timeout=10)
        if location:
            return location.latitude, location.longitude
        return 37.9838, 23.7275 
    except GeocoderTimedOut:
        return 37.9838, 23.7275

for index, row in df.iterrows():
    building_id = index + 1
    title = str(row['Τίτλος παραδείγματος']) if pd.notna(row['Τίτλος παραδείγματος']) else f"Κτήριο {building_id}"
    address = str(row['Οδός']) if pd.notna(row['Οδός']) else ""
    architect = str(row['Αρχιτέκτονας/Μελετητής']) if pd.notna(row['Αρχιτέκτονας/Μελετητής']) else "Άγνωστος"
    intervention_type = str(row['Τύπος επέμβασης']) if pd.notna(row['Τύπος επέμβασης']) else ""
    history = str(row['Σχέση παλιού–νέου (πώς «συνομιλούν»)']) if pd.notna(row['Σχέση παλιού–νέου (πώς «συνομιλούν»)']) else ""
    
    print(f"📍 Επεξεργασία & εύρεση συντεταγμένων: {title}...")
    lat, lng = get_coordinates(address)
    time.sleep(1) 

    # Φτιάχνουμε το "πακέτο" του κτηρίου και συνδέουμε τη φωτογραφία!
    building = {
        "id": building_id,
        "title": title.strip(),
        "address": address.strip(),
        "architect": architect.strip(),
        "type": intervention_type.strip(),
        "history": history.strip(),
        "lat": lat,
        "lng": lng,
        "visited": False,
        "notes": "",
        # Εδώ λέμε στο App: "Ψάξε στον φάκελο images για τη φωτό με τον αριθμό του ID"
        "photo_url": f"images/{building_id}.jpg" 
    }
    buildings_data.append(building)

with open('app_data.json', 'w', encoding='utf-8') as f:
    json.dump(buildings_data, f, ensure_ascii=False, indent=4)

print("\n✅ ΕΠΙΤΥΧΙΑ! Το αρχείο app_data.json δημιουργήθηκε. Τα κτήρια έχουν πλέον συνδεθεί με τις εικόνες του φακέλου 'images'!")