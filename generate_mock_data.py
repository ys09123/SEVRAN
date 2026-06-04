"""
generate_mock_data.py
─────────────────────
Generate mock EV charging station data for Bangalore, India.
Prototype data for the Smart EV Routing & Availability Network hackathon demo.

Repurposes K-Means clustering from the original ev_sales analysis to assign
spatial density zones, which drive AI-predicted wait times.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

np.random.seed(42)

# ═══════════════════════════════════════════════════════
#  Bangalore Charging Locations  (15 areas × 5 stations)
# ═══════════════════════════════════════════════════════
LOCATIONS = [
    {"area": "Koramangala",       "suffix": "5th Block Hub",       "lat": 12.9352, "lon": 77.6245},
    {"area": "Indiranagar",       "suffix": "100ft Road",          "lat": 12.9784, "lon": 77.6408},
    {"area": "Whitefield",        "suffix": "ITPL Main Gate",      "lat": 12.9698, "lon": 77.7500},
    {"area": "Electronic City",   "suffix": "Phase 1 Plaza",       "lat": 12.8440, "lon": 77.6593},
    {"area": "MG Road",           "suffix": "Metro Station",       "lat": 12.9756, "lon": 77.6066},
    {"area": "HSR Layout",        "suffix": "Sector 2 Park",       "lat": 12.9116, "lon": 77.6389},
    {"area": "JP Nagar",          "suffix": "6th Phase Circle",    "lat": 12.9063, "lon": 77.5857},
    {"area": "Marathahalli",      "suffix": "Bridge Junction",     "lat": 12.9591, "lon": 77.7019},
    {"area": "Hebbal",            "suffix": "Flyover Complex",     "lat": 13.0358, "lon": 77.5970},
    {"area": "Jayanagar",         "suffix": "4th Block",           "lat": 12.9308, "lon": 77.5838},
    {"area": "Bannerghatta Road", "suffix": "Main Junction",       "lat": 12.8876, "lon": 77.5969},
    {"area": "Rajajinagar",       "suffix": "Metro Hub",           "lat": 12.9883, "lon": 77.5533},
    {"area": "Yelahanka",         "suffix": "New Town Center",     "lat": 13.1007, "lon": 77.5963},
    {"area": "Sarjapur Road",     "suffix": "Tech Park Gate",      "lat": 12.9107, "lon": 77.6872},
    {"area": "Malleshwaram",      "suffix": "Sampige Road",        "lat": 13.0035, "lon": 77.5710},
]

# ═══════════════════════════════════════════════════════
#  Provider Configurations
# ═══════════════════════════════════════════════════════
PROVIDERS = [
    {"name": "Tata Power EZ Charge", "price_min": 14.0, "price_max": 16.0},
    {"name": "ChargeZone",           "price_min": 12.0, "price_max": 15.0},
    {"name": "Ather Grid",          "price_min": 13.0, "price_max": 15.5},
    {"name": "Statiq",              "price_min": 15.0, "price_max": 18.0},
    {"name": "JEEV",                "price_min": 11.0, "price_max": 14.0},
]

# ═══════════════════════════════════════════════════════
#  Charger Types & Amenities
# ═══════════════════════════════════════════════════════
CHARGER_TYPES = [
    {"type": "AC Level 2",        "power_kw": 7},
    {"type": "AC Level 2",        "power_kw": 22},
    {"type": "DC Fast (CCS2)",    "power_kw": 50},
    {"type": "DC Fast (CCS2)",    "power_kw": 150},
    {"type": "DC Fast (CHAdeMO)", "power_kw": 50},
]

AMENITIES = [
    "WiFi", "Restroom", "Café", "Parking",
    "Lounge", "Vending Machine", "Security Camera", "24/7 Access",
]

STATUS_CHOICES  = ["Available", "In Use", "Offline"]
STATUS_WEIGHTS  = [0.50, 0.35, 0.15]


def generate():
    """Generate mock charging station data with K-Means density clustering."""

    records = []
    station_id = 1

    for loc in LOCATIONS:
        for _ in range(5):
            provider = PROVIDERS[np.random.randint(len(PROVIDERS))]
            charger  = CHARGER_TYPES[np.random.randint(len(CHARGER_TYPES))]
            status   = np.random.choice(STATUS_CHOICES, p=STATUS_WEIGHTS)

            lat = loc["lat"] + np.random.uniform(-0.006, 0.006)
            lon = loc["lon"] + np.random.uniform(-0.006, 0.006)

            price = round(np.random.uniform(provider["price_min"], provider["price_max"]), 2)
            rating = round(np.random.uniform(3.5, 5.0), 1)

            n_amenities = np.random.randint(2, 6)
            amenities = ", ".join(
                np.random.choice(AMENITIES, size=n_amenities, replace=False)
            )

            records.append({
                "station_id":    f"BLR-{station_id:03d}",
                "station_name":  f"{provider['name']} — {loc['area']} {loc['suffix']}",
                "provider":      provider["name"],
                "area":          loc["area"],
                "lat":           round(lat, 6),
                "lon":           round(lon, 6),
                "charger_type":  charger["type"],
                "power_kw":      charger["power_kw"],
                "status":        status,
                "price_per_kwh": price,
                "rating":        rating,
                "amenities":     amenities,
            })
            station_id += 1

    df = pd.DataFrame(records)

    # ── K-Means Clustering (spatial density) ──────────────
    X = df[["lat", "lon"]].values
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
    df["cluster"] = kmeans.labels_

    # Map clusters to density labels based on distance from city center
    city_center = np.array([12.9716, 77.5946])  # Bangalore center
    centroids   = kmeans.cluster_centers_
    distances   = np.linalg.norm(centroids - city_center, axis=1)
    sorted_idx  = np.argsort(distances)

    density_map = {
        sorted_idx[0]: "High",    # closest to center → most congested
        sorted_idx[1]: "Medium",
        sorted_idx[2]: "Low",     # furthest → least congested
    }
    df["density_zone"] = df["cluster"].map(density_map)

    # ── Base Wait Time from Density Zone ──────────────────
    wait_ranges = {"High": (12, 25), "Medium": (5, 15), "Low": (0, 8)}
    df["base_wait_min"] = df["density_zone"].apply(
        lambda z: np.random.randint(wait_ranges[z][0], wait_ranges[z][1] + 1)
    )

    # Offline stations have no meaningful wait
    df.loc[df["status"] == "Offline", "base_wait_min"] = 0

    # ── Save ──────────────────────────────────────────────
    df.to_csv("mock_chargers.csv", index=False)

    print(f"[OK] Generated {len(df)} mock charging stations -> mock_chargers.csv")
    print(f"     Density zones : {df['density_zone'].value_counts().to_dict()}")
    print(f"     Statuses      : {df['status'].value_counts().to_dict()}")
    print(f"     Providers     : {df['provider'].value_counts().to_dict()}")
    print(f"     Charger types : {df['charger_type'].value_counts().to_dict()}")


if __name__ == "__main__":
    generate()
