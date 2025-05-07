-- Create student_analytics_dw schema
DROP SCHEMA IF EXISTS student_analytics_dw CASCADE;
CREATE SCHEMA student_analytics_dw;

-- Create Dimension and Fact Tables in student_analytics_dw

CREATE TABLE student_analytics_dw.dim_student (
    student_id INT PRIMARY KEY,
    gender TEXT,
    age_cate TEXT,
    partner TEXT
);

CREATE TABLE student_analytics_dw.dim_health (
    health_id SERIAL PRIMARY KEY,
    student_id INT,
    mental_health_score TEXT,
    physical_health_score TEXT
);

CREATE TABLE student_analytics_dw.dim_support (
    support_id SERIAL PRIMARY KEY,
    student_id INT,
    support_group TEXT,
    access_to_counseling TEXT,
    academic_advisor TEXT
);

CREATE TABLE student_analytics_dw.fact_student_performance (
    fact_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student_analytics_dw.dim_student(student_id),
    health_id INT REFERENCES student_analytics_dw.dim_health(health_id),
    support_id INT REFERENCES student_analytics_dw.dim_support(support_id),
    hours_studied TEXT,
    attendance TEXT,
    parental_involvement TEXT,
    access_to_resources TEXT,
    extracurricular_activities TEXT,
    sleep_hours TEXT,
    previous_scores TEXT,
    motivation_level TEXT,
    internet_access TEXT,
    tutoring_sessions TEXT,
    family_income TEXT,
    teacher_quality TEXT,
    school_type TEXT,
    peer_influence TEXT,
    physical_activity TEXT,
    learning_disabilities TEXT,
    parental_education_level TEXT,
    distance_from_home TEXT,
    gender TEXT,
    exam_score TEXT
);
