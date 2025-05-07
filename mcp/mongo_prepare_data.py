from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB (adjust host/port as needed)
client = MongoClient("mongodb://localhost:27017/")

# Create or access database and collection
db = client["studentManagement"]
students_collection = db["students"]

# Sample data to randomize
names = ["马军军", "李杰", "张伟", "王磊", "刘强", "陈涛", "赵磊", "孙浩", "周勇", "吴凡"]
addresses = [
    "FeiFortHyatt Mountains 2栋102室",
    "East WillaLavonne Burg 3栋103室",
    "Ocean Park Tower 5栋501室",
    "Sunset View Plaza 1栋201室"
]
emails = ["school.edu.cn", "campus.cn", "edu.org"]
health_statuses = ["合格", "良好", "一般"]

def generate_student(i):
    base_id = f"S202301{str(i).zfill(2)}"
    name = random.choice(names)
    gender = random.choice(["男", "女"])
    birth_year = random.randint(2004, 2007)
    birth_date = datetime(birth_year, random.randint(1, 12), random.randint(1, 28))
    enroll_date = datetime(2023, 8, 31, 16)
    email_domain = random.choice(emails)
    
    student = {
        "_id": base_id,
        "name": name,
        "gender": gender,
        "birthDate": birth_date,
        "enrollmentDate": enroll_date,
        "classId": "202301",
        "contact": {
            "phone": f"13{random.randint(100000000, 999999999)}",
            "email": f"{base_id.lower()}@{email_domain}",
            "emergencyContact": f"{random.choice(['l3xke6zx7a', 'x9we8nml'])}",
            "address": random.choice(addresses)
        },
        "profile": {
            "height": random.randint(150, 180),
            "weight": round(random.uniform(45, 75), 2),
            "healthStatus": random.choice(health_statuses)
        }
    }
    return student

# Clear existing data (optional)
students_collection.delete_many({})

# Insert 180 students
students = [generate_student(i + 1) for i in range(180)]
students_collection.insert_many(students)

print("Inserted 180 student documents into 'studentManagement.students'")

