import sqlite3

def create_table():
    conn = sqlite3.connect("applications.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        application_id TEXT PRIMARY KEY,
        opening_ciphertext TEXT,
        charge_rate_amount REAL,
        charge_rate_currency TEXT,
        created_ts TEXT,
        modified_ts TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_applications(applications):
    conn = sqlite3.connect("applications.db")
    cur = conn.cursor()

    for app in applications:
        cur.execute("""
        INSERT OR IGNORE INTO applications (application_id, opening_ciphertext, charge_rate_amount, charge_rate_currency, created_ts, modified_ts)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (app["applicationUID"],
              app["openingCiphertext"],
              app["terms"]["chargeRate"]["amount"],
              app["terms"]["chargeRate"]["currency"],
              app["auditDetails"]["createdTs"],
              app["auditDetails"]["modifiedTs"]))

    conn.commit()
    conn.close()