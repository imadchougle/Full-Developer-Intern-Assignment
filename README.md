# Full-Developer-Intern-Assignment


## Prerequisites
- Python 3.11
  
- Install dependencies using `pip install -r requirements.txt`

  
```bash
   git clone https://github.com/imadchougle/Full-Developer-Intern-Assignment.git
   cd my_flask_app
```

## MYSql Database Setup 

```bash

CREATE DATABASE FORM_DB;

use form_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    password VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE global_contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(20),
    name VARCHAR(100),
    spam_likelihood INT DEFAULT 0
);

