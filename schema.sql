-- SQL schema for Skill Navigator project

-- User Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    full_name VARCHAR(100),
    bio TEXT,
    role VARCHAR(20) DEFAULT 'user',
    profile_picture VARCHAR(200),
    education VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    phone_number VARCHAR(20) UNIQUE,
    email_updates BOOLEAN DEFAULT TRUE,
    email_newsletter BOOLEAN DEFAULT TRUE,
    email_marketing BOOLEAN DEFAULT FALSE,
    skill_recommendations BOOLEAN DEFAULT TRUE,
    career_suggestions BOOLEAN DEFAULT TRUE,
    profile_visibility BOOLEAN DEFAULT TRUE,
    show_skills BOOLEAN DEFAULT TRUE
);

-- Skill Table
CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level INT,
    experience_years FLOAT,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Activity Table
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Interlist Table
CREATE TABLE interlist (
    S_NO INT PRIMARY KEY,
    College_Name VARCHAR(75),
    State_name VARCHAR(13),
    District_Name VARCHAR(27),
    College_Address VARCHAR(238),
    College_Nature_Type VARCHAR(27),
    Stream VARCHAR(18),
    Email_Id VARCHAR(43)
);

-- College Table
CREATE TABLE college (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    website VARCHAR(200) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
); 