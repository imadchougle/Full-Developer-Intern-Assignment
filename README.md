# Full-Developer-Intern-Assignment

## Technolgies used

1. Frontend - Html, Css, Javascript
2. Backend - Flask
3. Database - MYSql


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
```

## Usage Guide

1. First Home Page
  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/119697d8-29a9-443b-a4fd-41874f0ef1b0)

2. Registration Form

  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/a0b6542c-29c4-4f7a-bdc9-cac2af278d82)

IF USER ALREADY EXISTS THEN ERROR

  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/2de8713d-131b-438a-a44d-5a77b92c3fb9)



3. Verify OTP

  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/44a22c9c-8a68-4977-b3d2-bf1244398bf7)

If Wrong otp then popup

  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/536a3df8-5577-406a-9b65-4de5c9c8b3f9)

If Success 

  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/723214e8-60cc-4597-81c4-b464fe69831a)

4. Login


   If password is wrong or account not verified

   ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/384623c0-2440-4498-8ef3-17e05993c7de)


   If Login Success

   ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/fb999d70-0fab-4336-ab94-36327fd85dca)


5. User HomePage

  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/f6d91659-25da-4ba2-b2f0-5df2731b583f)


6. Search Function

  searching for the name "Ali"

  ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/98363498-f20c-4545-b2ab-b6f2f458b1f0)


7. Marking Spam feature

   ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/38094f26-950e-46c6-948e-cbec7d963b0a)

   This number is of Alicia Brown and it will add 1 spam to it


8. Email ID special seach function when the User is logged in and the user is the their personal contacts List then only the email id will be shown;
   In this case Imad Chougle has added Raju in his personal account, and Raju is registered user and has Imad Chougle in his personal contact,
   now Imad Chougle is logged in and searches for number. in this case the condition is satisfied and the email is shown

   ![image](https://github.com/imadchougle/Full-Developer-Intern-Assignment/assets/54437743/a7f4bea6-ebc1-40cc-9be7-c2ca7311494c)













