-- Courses with ≥ 50 students
CREATE VIEW PopularCourses AS
SELECT course_id, COUNT(user_id) AS student_count
FROM Enrollment
GROUP BY course_id
HAVING COUNT(user_id) >= 50;

-- Students enrolled in ≥ 5 courses
CREATE VIEW ActiveStudents AS
SELECT user_id, COUNT(course_id) AS course_count
FROM Enrollment
GROUP BY user_id
HAVING COUNT(course_id) >= 5;

-- Lecturers teaching ≥ 3 courses
CREATE VIEW TopLecturers AS
SELECT user_id, COUNT(course_id) AS course_count
FROM Teaching
GROUP BY user_id
HAVING COUNT(course_id) >= 3;

-- Top 10 enrolled courses
CREATE VIEW TopEnrolledCourses AS
SELECT course_id, COUNT(user_id) AS enrollment_count
FROM Enrollment
GROUP BY course_id
ORDER BY enrollment_count DESC
LIMIT 10;

-- Top 10 students by average grade
CREATE VIEW TopStudentsByGrade AS
SELECT ss.user_id, AVG(g.grade) AS avg_grade
FROM Grade g
JOIN StudentSubmission ss ON g.submission_id = ss.submission_id
GROUP BY ss.user_id
ORDER BY avg_grade DESC
LIMIT 10;

-- Minimun for lectuer
SELECT uc.user_id, u.role, COUNT(*) AS course_count 
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 2
GROUP BY uc.user_id, u.role
order by COUNT(*) ASC
limit 1 
;

-- minimum course for student
SELECT uc.user_id, u.role, COUNT(*) AS course_count 
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 3
GROUP BY uc.user_id, u.role
order by COUNT(*) ASC
limit 1 
;

-- Maximum for lectuer
SELECT uc.user_id, u.role, COUNT(*) AS course_count 
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 2
GROUP BY uc.user_id, u.role
order by COUNT(*) DESC
limit 1 
;

-- maximum course for student
SELECT uc.user_id, u.role, COUNT(*) AS course_count 
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 3
GROUP BY uc.user_id, u.role
order by COUNT(*) DESC
limit 1 
;

SELECT uc.course_id, COUNT(*) AS student_count
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 2
GROUP BY uc.course_id
order by COUNT(*) DESC
limit 1 ;

SELECT uc.course_id, COUNT(*) AS student_count
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 2
GROUP BY uc.course_id
order by COUNT(*) ASC
limit 1 ;

SELECT uc.course_id, COUNT(*) AS student_count
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 3
GROUP BY uc.course_id
order by COUNT(*) DESC
limit 1 ;

SELECT uc.course_id, COUNT(*) AS student_count
FROM user_course uc
JOIN user u ON uc.user_id = u.user_id
WHERE u.role = 3
GROUP BY uc.course_id
order by COUNT(*) ASC
limit 1 ;