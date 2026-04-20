from fastapi import APIRouter
import requests
import math

router = APIRouter(prefix="/emergency", tags=["Emergency"])

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.get("/nearby-places")
def get_nearby_places(lat: float, lng: float, type: str = "hospital"):
    # Using OpenStreetMap Overpass API (Free)
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Simple query for hospitals or pharmacies
    query = f"""[out:json][timeout:15];(node["amenity"="{type}"](around:5000,{lat},{lng});way["amenity"="{type}"](around:5000,{lat},{lng}););out center;"""
    
    # Common medicines for stock simulation
    common_medicines = ["Sertraline", "Paracetamol", "Amoxicillin", "Metformin", "Atorvastatin"]

    # Type-specific fallback data
    if type == "pharmacy":
        fallback_data = [
            {"id": 201, "name": "Apollo Pharmacy", "distance": "0.4 km", "address": "Seawoods Grand Central Mall", "phone": "1860 500 0101", "rating": 4.5, "is_open": True, "bestOption": True, "stock": ["Sertraline", "Paracetamol", "Amoxicillin"]},
            {"id": 202, "name": "Wellness Forever", "distance": "0.9 km", "address": "Sector 11, CBD Belapur", "phone": "+91 22 2757 1234", "rating": 4.6, "is_open": True, "bestOption": False, "stock": ["Sertraline", "Metformin", "Atorvastatin"]},
            {"id": 203, "name": "MedPlus Pharmacy", "distance": "1.3 km", "address": "Sector 40, Seawoods", "phone": "+91 22 9876 5432", "rating": 4.3, "is_open": True, "bestOption": False, "stock": ["Paracetamol", "Amoxicillin", "Atorvastatin"]}
        ]
    else:
        fallback_data = [
            {"id": 101, "name": "Seawoods Hospital", "distance": "0.6 km", "address": "Sector 48, Seawoods", "phone": "+91 73046 83123", "rating": 4.5, "is_open": True, "emergency": True},
            {"id": 102, "name": "Dr. Jairaj's Hospital", "distance": "1.1 km", "address": "Sector 6, CBD Belapur", "phone": "+91 70450 11188", "rating": 4.3, "is_open": True, "emergency": True}
        ]

    try:
        response = requests.get(overpass_url, params={'data': query}, timeout=10)
        if response.status_code != 200:
            return fallback_data
            
        data = response.json()
        results = []
        for idx, element in enumerate(data.get('elements', [])):
            h_lat = element.get('lat') or element.get('center', {}).get('lat')
            h_lng = element.get('lon') or element.get('center', {}).get('lon')
            if not h_lat or not h_lng: continue
                
            dist = calculate_distance(lat, lng, h_lat, h_lng)
            tags = element.get('tags', {})
            name = tags.get('name') or f"Nearby {type.capitalize()}"
            address = tags.get('addr:street') or "Address not available"
            phone = tags.get('contact:phone') or tags.get('phone') or "Phone not available"
            
            item = {
                "id": element.get('id'),
                "name": name,
                "distance": f"{dist:.1f} km",
                "address": address,
                "phone": phone,
                "rating": 4.5,
                "is_open": True,
                "bestOption": True if idx == 0 and type == "pharmacy" else False,
                "emergency": True if type == "hospital" else False
            }
            
            # Add stock for pharmacies to ensure they show up in medicine search
            if type == "pharmacy":
                item["stock"] = common_medicines
                
            results.append(item)
            
        # If the API returned nothing, use fallback
        if not results:
            return fallback_data
            
        return results[:10]
        
    except Exception as e:
        print(f"DEBUG: API Error - {e}")
        return fallback_data

@router.get("/contacts")
def get_emergency_contacts():
    return [
        {"name": "Ambulance", "number": "102"},
        {"name": "Emergency Police", "number": "100"},
        {"name": "Blood Bank", "number": "104"}
    ]
