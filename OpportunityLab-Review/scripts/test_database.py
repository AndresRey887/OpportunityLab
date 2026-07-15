import sqlite3

connection = sqlite3.connect("data/opportunities.db")
cursor = connection.cursor()

cursor.execute("""
SELECT
    id,
    title,
    source,
    url
FROM opportunities
ORDER BY id;
""")

rows = cursor.fetchall()

print("\n=== Opportunities in Database ===\n")

for row in rows:
    print(f"ID     : {row[0]}")
    print(f"Title  : {row[1]}")
    print(f"Source : {row[2]}")
    print(f"URL    : {row[3]}")
    print("-" * 50)

print(f"\nTotal Opportunities: {len(rows)}")

connection.close()