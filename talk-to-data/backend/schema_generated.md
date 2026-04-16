# 📘 Auto‑Generated Database Schema

This file is generated automatically every time the server starts.

## Table: `authors`

### Columns:
- **author_id**: int
- **first_name**: varchar(100)
- **last_name**: varchar(100)
- **birth_date**: date
- **nationality**: varchar(100)
- **created_at**: timestamp

---

## Table: `book_authors`

### Columns:
- **book_id**: int
- **author_id**: int

---

## Table: `book_categories`

### Columns:
- **book_id**: int
- **category_id**: int

---

## Table: `book_copies`

### Columns:
- **copy_id**: int
- **book_id**: int
- **barcode**: varchar(50)
- **status**: enum('available','issued','lost','damaged')

---

## Table: `books`

### Columns:
- **book_id**: int
- **title**: varchar(255)
- **isbn**: varchar(20)
- **publish_year**: smallint
- **edition**: varchar(50)
- **publisher_id**: int
- **pages**: int
- **language**: varchar(50)
- **created_at**: timestamp

---

## Table: `borrow_transactions`

### Columns:
- **transaction_id**: int
- **copy_id**: int
- **member_id**: int
- **borrow_date**: date
- **due_date**: date
- **return_date**: date
- **fine_amount**: decimal(10,2)

---

## Table: `categories`

### Columns:
- **category_id**: int
- **category_name**: varchar(100)

---

## Table: `members`

### Columns:
- **member_id**: int
- **full_name**: varchar(150)
- **email**: varchar(150)
- **phone**: varchar(20)
- **address**: text
- **membership_date**: date
- **status**: enum('active','inactive')

---

## Table: `publishers`

### Columns:
- **publisher_id**: int
- **publisher_name**: varchar(255)
- **address**: varchar(255)
- **contact_email**: varchar(150)
- **contact_phone**: varchar(50)
- **created_at**: timestamp

---

## Table: `staff`

### Columns:
- **staff_id**: int
- **full_name**: varchar(150)
- **role**: varchar(100)
- **email**: varchar(150)
- **phone**: varchar(20)
- **joined_date**: date

---

