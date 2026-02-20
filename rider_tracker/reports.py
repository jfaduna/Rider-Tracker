import sqlite3

DB_PATH = "db.sqlite3"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = """
    WITH pickup_events AS (
        SELECT 
            re.ride_id,
            re.created_at AS pickup_time
        FROM rides_rideevent re
        WHERE re.description LIKE '%picked up%'
    ),
    dropoff_events AS (
        SELECT 
            re.ride_id,
            re.created_at AS dropoff_time
        FROM rides_rideevent re
        WHERE re.description LIKE '%dropped off%'
    ),
    trip_durations AS (
        SELECT
            r.id AS ride_id,
            u.first_name || ' ' || u.last_name AS driver_name,
            strftime('%Y-%m', p.pickup_time) AS month,
            (julianday(d.dropoff_time) - julianday(p.pickup_time)) * 24 AS duration_hours
        FROM pickup_events p
        JOIN dropoff_events d ON p.ride_id = d.ride_id
        JOIN rides_ride r ON r.id = p.ride_id
        JOIN rides_user u ON u.id = r.driver_id
    )
    SELECT
        month AS "Month",
        driver_name AS "Driver",
        COUNT(*) AS "Count of Trips > 1 hour"
    FROM trip_durations
    WHERE duration_hours > 1
    GROUP BY month, driver_name
    ORDER BY month, driver_name;
"""

cursor.execute(query)
rows = cursor.fetchall()

print(f"{'Month':<10} {'Driver':<15} {'Count of Trips > 1 hour'}")
for row in rows:
    print(f"{row[0]:<10} {row[1]:<15} {row[2]}")

conn.close()
