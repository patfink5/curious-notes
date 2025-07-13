import sqlite3
import csv

# Connect to the existing database
conn = sqlite3.connect("countries.db")
cur = conn.cursor()

# Query all data
cur.execute("SELECT name, capital, region, population, area FROM countries")
rows = cur.fetchall()

# CSV header
header = ["name", "capital", "region", "population", "area"]

# Write to CSV
with open("countries.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

conn.close()
print("✅ Exported to countries.csv")

