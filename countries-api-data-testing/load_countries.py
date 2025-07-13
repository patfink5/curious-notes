import requests
import sqlite3

# Step 1: Fetch data from Rest Countries API (with fields specified)
url = "https://restcountries.com/v3.1/all?fields=name,capital,region,population,area"
response = requests.get(url)

try:
    countries = response.json()
except Exception as e:
    print("❌ Failed to parse JSON:", e)
    print("🔎 Raw response text:")
    print(response.text[:500])
    exit()

# Safety check
if not isinstance(countries, list) or not isinstance(countries[0], dict):
    print("❌ Unexpected API format. Expected list of dicts.")
    exit()

# Step 2: Set up SQLite database
conn = sqlite3.connect("countries.db")
cur = conn.cursor()

# Step 3: Create table (if not exists)
cur.execute("""
CREATE TABLE IF NOT EXISTS countries (
    name TEXT,
    capital TEXT,
    region TEXT,
    population INTEGER,
    area REAL
)
""")

# Step 4: Insert data into table
for country in countries:
    if not isinstance(country, dict):
        continue  # skip anything malformed

    name = country.get("name", {}).get("common", "Unknown")

    # Handle capital safely
    capital_list = country.get("capital", [])
    capital = capital_list[0] if isinstance(capital_list, list) and capital_list else "Unknown"

    region = country.get("region", "Unknown")
    population = country.get("population", 0)
    area = country.get("area", 0.0)

    cur.execute("""
        INSERT INTO countries (name, capital, region, population, area)
        VALUES (?, ?, ?, ?, ?)
    """, (name, capital, region, population, area))

# Step 5: Commit and close
conn.commit()
conn.close()

print("✅ Countries data loaded into countries.db")
