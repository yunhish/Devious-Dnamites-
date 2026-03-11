CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_code INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    department_id INT,
    
    FOREIGN KEY (department_id) 
    REFERENCES departments(id)
    ON DELETE SET NULL
) ENGINE=InnoDB;
