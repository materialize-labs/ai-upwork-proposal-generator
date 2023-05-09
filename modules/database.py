import sqlite3
import uuid

def create_tables():
    conn = sqlite3.connect("applications.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE,
        application_id TEXT UNIQUE,
        vendorUID INTEGER,
        vendorOrgUID INTEGER,
        openingUID INTEGER,
        opening_ciphertext TEXT,
        charge_rate_amount REAL,
        charge_rate_currency TEXT,
        duration INTEGER,
        upfront_payment_percent INTEGER,
        cover_letter TEXT,
        applying_as INTEGER,
        status INTEGER,
        created_ts TEXT,
        modified_ts TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT,
        question TEXT,
        answer TEXT,
        FOREIGN KEY (application_id) REFERENCES applications(application_id)
    )
    """)

    conn.commit()
    conn.close()

def insert_applications_and_questions(applications):
    conn = sqlite3.connect("applications.db")
    cur = conn.cursor()

    for app in applications:
        generated_uuid = str(uuid.uuid4())
        cur.execute("""
        INSERT OR IGNORE INTO applications (
            uuid,
            application_id,
            vendorUID,
            vendorOrgUID,
            openingUID,
            opening_ciphertext,
            charge_rate_amount,
            charge_rate_currency,
            duration,
            upfront_payment_percent,
            cover_letter,
            applying_as,
            status,
            created_ts,
            modified_ts
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (generated_uuid,
              app["applicationUID"],
              app["vendorUID"],
              app["vendorOrgUID"],
              app["openingUID"],
              app["openingCiphertext"],
              app["terms"]["chargeRate"]["amount"],
              app["terms"]["chargeRate"]["currency"],
              app["terms"]["duration"],
              app["terms"]["upfrontPaymentPercent"],
              app["coverLetter"],
              app["applyingAs"],
              app["status"],
              app["auditDetails"]["createdTs"],
              app["auditDetails"]["modifiedTs"]))

        for qa in app["questionsAnswers"]:
            cur.execute("""
            INSERT INTO questions_answers (application_id, question, answer)
            VALUES (?, ?, ?)
            """, (app["applicationUID"],
                  qa["question"],
                  qa["answer"]))

    conn.commit()
    conn.close()