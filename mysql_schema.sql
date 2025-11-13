-- ======================================================
-- MOVIE / THEATRE PRODUCTION MANAGEMENT SYSTEM - SQL FILE
-- DBMS MINI PROJECT
-- ======================================================

CREATE DATABASE IF NOT EXISTS film_db;
USE film_db;

CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE,
    role VARCHAR(30)
);

CREATE TABLE production (
    prod_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    genre VARCHAR(50),
    language VARCHAR(50),
    director VARCHAR(100)
);

CREATE TABLE crew (
    crew_id INT AUTO_INCREMENT PRIMARY KEY,
    prod_id INT,
    name VARCHAR(100),
    role VARCHAR(100),
    FOREIGN KEY (prod_id) REFERENCES production(prod_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE casting (
    cast_id INT AUTO_INCREMENT PRIMARY KEY,
    prod_id INT,
    actor_name VARCHAR(100),
    character_name VARCHAR(100),
    FOREIGN KEY (prod_id) REFERENCES production(prod_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE budget (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    prod_id INT UNIQUE,
    estimated_cost FLOAT,
    actual_cost FLOAT,
    FOREIGN KEY (prod_id) REFERENCES production(prod_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE award (
    award_id INT AUTO_INCREMENT PRIMARY KEY,
    prod_id INT,
    name VARCHAR(200),
    category VARCHAR(100),
    year INT,
    FOREIGN KEY (prod_id) REFERENCES production(prod_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    prod_id INT,
    user_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 10),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prod_id) REFERENCES production(prod_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

DELIMITER //
CREATE TRIGGER auto_award_after_review
AFTER INSERT ON review
FOR EACH ROW
BEGIN
    IF NEW.rating >= 9 THEN
        INSERT INTO award(prod_id, name, category, year)
        VALUES (NEW.prod_id, 'Critics Choice', 'High Rating', YEAR(CURDATE()));
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_production_summary(IN p_id INT)
BEGIN
    SELECT 
        p.title,
        COUNT(r.review_id) AS total_reviews,
        AVG(r.rating) AS avg_rating,
        b.estimated_cost,
        b.actual_cost
    FROM production p
    LEFT JOIN review r ON p.prod_id = r.prod_id
    LEFT JOIN budget b ON p.prod_id = b.prod_id
    WHERE p.prod_id = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION rating_label(r INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    IF r >= 9 THEN RETURN 'Excellent';
    ELSEIF r >= 7 THEN RETURN 'Good';
    ELSEIF r >= 5 THEN RETURN 'Average';
    ELSE RETURN 'Poor';
    END IF;
END //
DELIMITER ;
