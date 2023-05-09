import sqlite3
import uuid

# Function to create the required database tables
def create_tables():
    conn = sqlite3.connect("applications.db")
    cur = conn.cursor()

    # Create the Jobs table
    cur.execute('''CREATE TABLE IF NOT EXISTS jobs (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         job_key TEXT NOT NULL,
         job_category_level_one TEXT,
         job_category_level_two TEXT,
         job_type TEXT,
         description TEXT,
         location TEXT,
         min_hourly_rate REAL,
         max_hourly_rate REAL,
         contractor_tier INTEGER,
         engagement_weeks INTEGER,
         engagement TEXT,
         skills TEXT,
         created_time TEXT,
         UNIQUE(job_key)
     );''')

    # Create the Applications table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE,
        application_id TEXT UNIQUE,
        job_id INTEGER,
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
        modified_ts TEXT,
        FOREIGN KEY(job_id) REFERENCES Jobs (id) ON DELETE CASCADE,
        UNIQUE(application_id)
    )
    """)

    # Create the Questions_Answers table
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

# Function to insert applications and questions data into the appropriate tables 
def insert_applications_and_questions(applications, client, get_job_details):
    conn = sqlite3.connect("applications.db")
    cur = conn.cursor()

    # Iterate through each application
    for app in applications:
        # Get the job details
        job_key = app["openingCiphertext"]
        job_details = get_job_details(client, job_key)

        job_data = (
            job_key,
            job_details["profile"]["job_category_level_one"],
            job_details["profile"]["job_category_level_two"],
            job_details["profile"]["job_type"],
            job_details["profile"]["op_description"],
            job_details["profile"]["op_pref_location"],
            job_details["profile"]["op_pref_hourly_rate_min"],
            job_details["profile"]["op_pref_hourly_rate_max"],
            job_details["profile"]["op_contractor_tier"],
            job_details["profile"]["engagement_weeks"],
            job_details["profile"]["op_engagement"],
            job_details["profile"]["op_ctime"]
        )

        # Insert the job details into the Jobs table
        cur.execute('''INSERT OR IGNORE INTO Jobs (job_key, job_category_level_one, job_category_level_two, 
                     job_type, description, location, min_hourly_rate, max_hourly_rate, 
                     contractor_tier, engagement_weeks, engagement, created_time)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', job_data)

        # Get the job_id associated with the job_key
        cur.execute("SELECT id FROM Jobs WHERE job_key=?", (job_key,))
        job_id = cur.fetchone()[0]

        generated_uuid = str(uuid.uuid4())
        cur.execute("""
        INSERT OR IGNORE INTO applications (
            uuid,
            application_id,
            job_id,
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (generated_uuid,
              app["applicationUID"],
              job_id,
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

        # Insert the questions and answers into the Questions_Answers table
        for qa in app["questionsAnswers"]:
            cur.execute("""
            INSERT INTO questions_answers (application_id, question, answer)
            VALUES (?, ?, ?)
            """, (app["applicationUID"],
                  qa["question"],
                  qa["answer"]))

    conn.commit()
    conn.close()
