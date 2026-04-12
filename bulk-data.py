import mysql.connector
from faker import Faker
import random
import time

fake = Faker()

# ---------------------------------------
# ✅ MySQL Connection
# ---------------------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="dhl123",
        database="library_db"
    )

db = get_db()
cursor = db.cursor()

# ---------------------------------------
# ✅ Utility: Fetch IDs From Table
# ---------------------------------------
def fetch_ids(table, pk):
    cursor.execute(f"SELECT {pk} FROM {table}")
    return [row[0] for row in cursor.fetchall()]

# ---------------------------------------
# ✅ BULK INSERT (NO DUPLICATES)
# ---------------------------------------
def insert_ignore(query, values):
    if not values:
        return
    cursor.executemany(query, values)
    db.commit()

# ---------------------------------------
# ✅ STEP 1 — Insert MASTER TABLE Data (No duplicates)
# ---------------------------------------

NUM_AUTHORS = 80000
NUM_PUBLISHERS = 10000
NUM_BOOKS = 800000
NUM_MEMBERS = 50000

# ✅ Insert Authors
authors = [
    (
        fake.first_name(),
        fake.last_name(),
        fake.date_of_birth(minimum_age=25, maximum_age=90),
        fake.country()
    )
    for _ in range(NUM_AUTHORS)
]

insert_ignore("""
    INSERT IGNORE INTO authors (first_name, last_name, birth_date, nationality)
    VALUES (%s, %s, %s, %s)
""", authors)
print("✅ Inserted authors")

# ✅ Insert Publishers
publishers = [
    (
        fake.company(),
        fake.address().replace("\n", ", "),
        fake.company_email(),
        fake.phone_number()[:20]
    )
    for _ in range(NUM_PUBLISHERS)
]

insert_ignore("""
    INSERT IGNORE INTO publishers (publisher_name, address, contact_email, contact_phone)
    VALUES (%s, %s, %s, %s)
""", publishers)
print("✅ Inserted publishers")

# ✅ Ensure categories exist before generating relations
cursor.execute("SELECT COUNT(*) FROM categories")
(cat_count,) = cursor.fetchone()

if cat_count == 0:
    default_cats = [
        ("Fiction",), ("Science",), ("History",),
        ("Adventure",), ("Romance",), ("Mystery",)
    ]
    insert_ignore("INSERT IGNORE INTO categories (category_name) VALUES (%s)", default_cats)
    print("✅ Default categories inserted")

# ✅ Insert Books
publisher_ids = fetch_ids("publishers", "publisher_id")

books = [
    (
        fake.sentence(nb_words=4).replace("'", ""),
        fake.isbn13(),
        random.randint(1901, 2024),
        f"{random.randint(1,10)}th",
        random.choice(publisher_ids),
        random.randint(100, 900),
        random.choice(["English", "French", "German", "Hindi"])
    )
    for _ in range(NUM_BOOKS)
]

insert_ignore("""
    INSERT IGNORE INTO books (title, isbn, publish_year, edition, publisher_id, pages, language)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", books)
print("✅ Inserted books")

# ✅ Insert Members
members = [
    (
        fake.name(),
        fake.email(),
        fake.phone_number()[:20],
        fake.address().replace("\n", ", "),
        fake.date_between(start_date="-10y", end_date="today")
    )
    for _ in range(NUM_MEMBERS)
]

insert_ignore("""
    INSERT IGNORE INTO members (full_name, email, phone, address, membership_date)
    VALUES (%s, %s, %s, %s, %s)
""", members)
print("✅ Inserted members")

# ---------------------------------------
# ✅ STEP 2 — Re-fetch table primary keys
# ---------------------------------------

book_ids = fetch_ids("books", "book_id")
author_ids = fetch_ids("authors", "author_id")
category_ids = fetch_ids("categories", "category_id")

print("✅ Loaded all real PKs")

# ---------------------------------------
# ✅ STEP 3 — Insert RELATIONSHIP TABLES
# ---------------------------------------

# ✅ Book–Author Relationships
book_authors = []
for b in book_ids:
    max_auth = min(3, len(author_ids))
    k = random.randint(1, max_auth)
    for a in random.sample(author_ids, k):
        book_authors.append((b, a))

insert_ignore("""
    INSERT IGNORE INTO book_authors (book_id, author_id)
    VALUES (%s, %s)
""", book_authors)
print("✅ Inserted book-author relations")

# ✅ Book–Category Relationships
book_categories = []
for b in book_ids:
    max_cat = min(3, len(category_ids))
    k = random.randint(1, max_cat)
    for c in random.sample(category_ids, k):
        book_categories.append((b, c))

insert_ignore("""
    INSERT IGNORE INTO book_categories (book_id, category_id)
    VALUES (%s, %s)
""", book_categories)
print("✅ Inserted book-category relations")

# ✅ Book Copies
NUM_COPIES = 1500

book_copies = [
    (
        random.choice(book_ids),
        fake.ean(length=13),
        random.choice(["available", "issued", "lost", "damaged"])
    )
    for _ in range(NUM_COPIES)
]

insert_ignore("""
    INSERT IGNORE INTO book_copies (book_id, barcode, status)
    VALUES (%s, %s, %s)
""", book_copies)
print("✅ Inserted book copies")

# ---------------------------------------
# ✅ Close connection
# ---------------------------------------
cursor.close()
db.close()

print("\n🎉 ALL MASTER + RELATION DATA INSERTED — SAFE FOR MULTIPLE RUNS ✅")