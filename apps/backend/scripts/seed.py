"""Seed script to create demo data for development."""
import asyncio
import os
import sys
import random
from datetime import datetime, timedelta
from uuid import uuid4

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from edulafia.config import settings
from edulafia.core.security import hash_password


async def seed():
    print(f"Connecting to database at: {settings.DATABASE_URL.replace(':' + settings.DATABASE_URL.split(':')[2].split('@')[0], ':***')}")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # 1. SCHOOL
        res = await session.execute(text("SELECT id FROM schools LIMIT 1"))
        school_id = res.scalar()

        if not school_id:
            school_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO schools (id, name, code, state, lga, phone, email, status)
                VALUES (:id, 'EduLafia International Academy', 'EDULAFIA', 'Lagos', 'Ikeja', '+2348000000000', 'admin@edulafia.edu.ng', 'active')
            """), {"id": school_id})

        pwd = hash_password("Password123!")

        # 2. ADMIN USER
        res = await session.execute(text("SELECT id FROM users WHERE email = 'admin@demo.com'"))
        admin_id = res.scalar()
        if not admin_id:
            admin_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO users (id, school_id, email, password_hash, first_name, last_name, role, status, phone)
                VALUES (:id, :school_id, 'admin@demo.com', :pwd, 'Demo', 'Admin', 'school_admin', 'active', '+2348000000001')
            """), {"id": admin_id, "school_id": school_id, "pwd": pwd})

        # 2b. TEACHER USER
        res = await session.execute(text("SELECT id FROM users WHERE email = 'teacher@demo.com'"))
        teacher_id = res.scalar()
        if not teacher_id:
            teacher_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO users (id, school_id, email, password_hash, first_name, last_name, role, status, phone)
                VALUES (:id, :school_id, 'teacher@demo.com', :pwd, 'Demo', 'Teacher', 'teacher', 'active', '+2348000000002')
            """), {"id": teacher_id, "school_id": school_id, "pwd": pwd})

        # 2c. NURSE USER
        res = await session.execute(text("SELECT id FROM users WHERE email = 'nurse@demo.com'"))
        nurse_id = res.scalar()
        if not nurse_id:
            nurse_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO users (id, school_id, email, password_hash, first_name, last_name, role, status, phone)
                VALUES (:id, :school_id, 'nurse@demo.com', :pwd, 'Demo', 'Nurse', 'nurse', 'active', '+2348000000003')
            """), {"id": nurse_id, "school_id": school_id, "pwd": pwd})

        # 2d. PROPRIETOR USER
        res = await session.execute(text("SELECT id FROM users WHERE email = 'proprietor@demo.com'"))
        proprietor_id = res.scalar()
        if not proprietor_id:
            proprietor_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO users (id, school_id, email, password_hash, first_name, last_name, role, status, phone)
                VALUES (:id, :school_id, 'proprietor@demo.com', :pwd, 'Demo', 'Proprietor', 'proprietor', 'active', '+2348000000004')
            """), {"id": proprietor_id, "school_id": school_id, "pwd": pwd})

        # 2e. PARENT USER
        res = await session.execute(text("SELECT id FROM users WHERE email = 'parent@demo.com'"))
        parent_id = res.scalar()
        if not parent_id:
            parent_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO users (id, school_id, email, password_hash, first_name, last_name, role, status, phone)
                VALUES (:id, :school_id, 'parent@demo.com', :pwd, 'Demo', 'Parent', 'parent', 'active', '+2348000000005')
            """), {"id": parent_id, "school_id": school_id, "pwd": pwd})

        # 3. ACADEMIC YEAR
        res = await session.execute(text("SELECT id FROM academic_years WHERE school_id = :school_id LIMIT 1"), {"school_id": school_id})
        academic_year_id = res.scalar()
        if not academic_year_id:
            academic_year_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO academic_years (id, school_id, name, start_date, end_date, is_active)
                VALUES (:id, :school_id, '2023/2024', :start_date, :end_date, true)
            """), {
                "id": academic_year_id,
                "school_id": school_id,
                "start_date": datetime.now().date() - timedelta(days=200),
                "end_date": datetime.now().date() + timedelta(days=165)
            })

        # 3b. TERM
        res = await session.execute(text("SELECT id FROM terms WHERE school_id = :school_id LIMIT 1"), {"school_id": school_id})
        term_id = res.scalar()
        if not term_id:
            term_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO terms (id, academic_year_id, school_id, name, start_date, end_date, is_active)
                VALUES (:id, :ay_id, :school_id, 'First Term', :start_date, :end_date, true)
            """), {
                "id": term_id,
                "ay_id": academic_year_id,
                "school_id": school_id,
                "start_date": datetime.now().date() - timedelta(days=200),
                "end_date": datetime.now().date() + timedelta(days=165)
            })

        # 4. CLASSES
        classes = ['JSS 1', 'JSS 2', 'JSS 3', 'SS 1', 'SS 2', 'SS 3']
        class_ids = []
        for c in classes:
            res = await session.execute(text("SELECT id FROM classes WHERE name = :name AND school_id = :school_id LIMIT 1"), {"name": c, "school_id": school_id})
            cid = res.scalar()
            if not cid:
                cid = str(uuid4())
                await session.execute(text("""
                    INSERT INTO classes (id, school_id, name, level, capacity)
                    VALUES (:id, :school_id, :name, :name, 40)
                """), {"id": cid, "school_id": school_id, "name": c})
            class_ids.append(cid)

        # 5. STUDENTS
        student_ids = []
        first_names = ['Ade', 'Olu', 'Chioma', 'Ngozi', 'Ibrahim', 'Fatima', 'Musa', 'Aisha', 'Emeka', 'Zainab']
        last_names = ['Okafor', 'Adeyemi', 'Balogun', 'Abubakar', 'Nwosu', 'Lawal', 'Kalu', 'Mustapha', 'Okoro', 'Umar']

        res = await session.execute(text("SELECT count(*) FROM students WHERE school_id = :school_id"), {"school_id": school_id})
        if res.scalar() < 50:
            for i in range(50):
                sid = str(uuid4())
                student_ids.append(sid)
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                gender = random.choice(['male', 'female'])
                dob = datetime.now().date() - timedelta(days=random.randint(365*10, 365*16))
                cid = random.choice(class_ids)

                await session.execute(text("""
                    INSERT INTO students (id, school_id, first_name, last_name, admission_number, date_of_birth, gender, class_id, status, admission_date, nationality)
                    VALUES (:id, :school_id, :fname, :lname, :adm, :dob, :gender, :cid, 'active', :adm_date, 'Nigerian')
                """), {
                    "id": sid, "school_id": school_id, "fname": fname, "lname": lname,
                    "adm": f"ED-{2024}-{i:03d}", "dob": dob, "gender": gender, "cid": cid,
                    "adm_date": datetime.now().date() - timedelta(days=200)
                })
        else:
            res = await session.execute(text("SELECT id FROM students WHERE school_id = :school_id"), {"school_id": school_id})
            student_ids = [r[0] for r in res.fetchall()]

        # 6. ATTENDANCE (Last 30 days)
        res = await session.execute(text("SELECT count(*) FROM attendance_records WHERE school_id = :school_id"), {"school_id": school_id})
        if res.scalar() == 0:
            for i in range(30):
                date = datetime.now().date() - timedelta(days=i)
                if date.weekday() >= 5: continue # Skip weekends

                for sid in student_ids:
                    status = random.choices(['present', 'absent', 'late'], weights=[0.85, 0.05, 0.10])[0]
                    await session.execute(text("""
                        INSERT INTO attendance_records (id, school_id, student_id, class_id, date, status, recorded_by, sync_status)
                        VALUES (:id, :school_id, :sid, :cid, :date, :status, :rec_by, 'synced')
                    """), {
                        "id": str(uuid4()), "school_id": school_id, "sid": sid, "cid": random.choice(class_ids),
                        "date": date, "status": status, "rec_by": admin_id
                    })

        # 7. SICK BAY VISITS
        res = await session.execute(text("SELECT count(*) FROM sick_bay_visits WHERE school_id = :school_id"), {"school_id": school_id})
        if res.scalar() == 0:
            import json
            for _ in range(20):
                await session.execute(text("""
                    INSERT INTO sick_bay_visits (id, school_id, student_id, visit_date, visit_time, presenting_complaint_codes, temperature, outcome, parent_notified, is_sentinel_relevant, recorded_by)
                VALUES (:id, :school_id, :sid, :date, :time, :codes, :temp, 'completed', false, false, :rec_by)
                """), {
                    "id": str(uuid4()), "school_id": school_id, "sid": random.choice(student_ids),
                    "date": datetime.now().date() - timedelta(days=random.randint(1, 30)),
                    "time": (datetime.now() - timedelta(hours=random.randint(1,8))).time(),
                    "codes": ["fever", "headache"],
                    "temp": round(random.uniform(36.5, 39.0), 1),
                    "rec_by": admin_id
                })

        # 8. FEE SCHEDULE
        res = await session.execute(text("SELECT id FROM fee_schedules WHERE school_id = :school_id LIMIT 1"), {"school_id": school_id})
        if not res.scalar():
            fs_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO fee_schedules (id, school_id, academic_year_id, name, description, is_active, created_by)
                VALUES (:id, :school_id, :ay_id, 'First Term Tuition 2023/2024', 'Standard tuition fees for all classes', true, :admin)
            """), {
                "id": fs_id, "school_id": school_id, "ay_id": academic_year_id, "admin": admin_id
            })

        # 9. GUARDIAN & LINKING
        res = await session.execute(text("SELECT id FROM guardians WHERE email = 'parent@demo.com'"))
        guardian_id = res.scalar()
        if not guardian_id:
            guardian_id = str(uuid4())
            await session.execute(text("""
                INSERT INTO guardians (id, school_id, first_name, last_name, phone_number, relationship_type, email, portal_access, user_id)
                VALUES (:id, :school_id, 'Demo', 'Parent', '+2348011111111', 'father', 'parent@demo.com', true, :user_id)
            """), {"id": guardian_id, "school_id": school_id, "user_id": parent_id})

            # Link to first 2 students
            for sid in student_ids[:2]:
                await session.execute(text("""
                    INSERT INTO student_guardians (id, student_id, guardian_id, is_primary, is_emergency_contact, can_pickup)
                    VALUES (:id, :student_id, :guardian_id, true, true, true)
                """), {"id": str(uuid4()), "student_id": sid, "guardian_id": guardian_id})

        # 10. MESSAGING & NOTIFICATIONS
        message_data = [
            (admin_id, teacher_id, "Welcome to the new term. Please submit your lesson plans by Friday."),
            (teacher_id, admin_id, "Thank you, lesson plans have been uploaded to the portal."),
            (teacher_id, parent_id, "Hello Demo Parent, your child has been doing great in class this week."),
            (parent_id, teacher_id, "Thank you for the update! I will make sure they keep up the good work.")
        ]

        for sender, receiver, content in message_data:
            res = await session.execute(text("SELECT id FROM messages WHERE sender_id = :sender AND receiver_id = :receiver AND content = :content"), {"sender": sender, "receiver": receiver, "content": content})
            if not res.scalar():
                await session.execute(text("""
                    INSERT INTO messages (id, sender_id, receiver_id, content, read_at)
                    VALUES (:id, :sender, :receiver, :content, NOW())
                """), {"id": str(uuid4()), "sender": sender, "receiver": receiver, "content": content})

        notification_data = [
            ("attendance", "Student Absent", "Your child was marked absent today.", "in_app"),
            ("academic", "Result Published", "First term results are now available on the portal.", "email"),
            ("finance", "Fee Reminder", "Please note that tuition for the next term is due in 2 weeks.", "in_app")
        ]

        for n_type, title, msg, channel in notification_data:
            res = await session.execute(text("SELECT id FROM parent_notifications WHERE guardian_id = :guardian_id AND title = :title"), {"guardian_id": guardian_id, "title": title})
            if not res.scalar():
                await session.execute(text("""
                    INSERT INTO parent_notifications (id, guardian_id, student_id, notification_type, title, message, channel, priority, status, sent_at)
                    VALUES (:id, :guardian_id, :student_id, :n_type, :title, :msg, :channel, 'normal', 'sent', NOW())
                """), {
                    "id": str(uuid4()), "guardian_id": guardian_id, "student_id": student_ids[0],
                    "n_type": n_type, "title": title, "msg": msg, "channel": channel
                })

        await session.commit()
        print("Successfully seeded comprehensive demo data!")
        print()
        print("Login Credentials:")
        print("  Admin:       admin@demo.com / Password123!")
        print("  Teacher:     teacher@demo.com / Password123!")
        print("  Nurse:       nurse@demo.com / Password123!")
        print("  Proprietor:  proprietor@demo.com / Password123!")
        print("  Parent:      parent@demo.com / Password123!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
