-- Skip COPY statements since data was already loaded manually

-- Populate Dimension Tables

-- dim_student
INSERT INTO student_analytics_dw.dim_student (student_id, gender, age_cate, partner)
SELECT DISTINCT student_id, gender, age_cate, partner
FROM staging_students;

-- dim_health (adjusted to use real columns)
INSERT INTO student_analytics_dw.dim_health (student_id, mental_health_score, physical_health_score)
SELECT DISTINCT student_id, intimate, japanese
FROM staging_students;

-- dim_support (adjusted to use real columns)
INSERT INTO student_analytics_dw.dim_support (student_id, support_group, access_to_counseling, academic_advisor)
SELECT DISTINCT student_id, partner_bi, friends_bi, parents_bi
FROM staging_students;

-- fact_student_performance (add type casts for join)
INSERT INTO student_analytics_dw.fact_student_performance (
    student_id, health_id, support_id,
    hours_studied, attendance, parental_involvement, access_to_resources,
    extracurricular_activities, sleep_hours, previous_scores, motivation_level,
    internet_access, tutoring_sessions, family_income, teacher_quality,
    school_type, peer_influence, physical_activity, learning_disabilities,
    parental_education_level, distance_from_home, gender, exam_score
)
SELECT
    p.student_id::INT,
    h.health_id,
    sp.support_id,
    p.Hours_Studied, p.Attendance, p.Parental_Involvement, p.Access_to_Resources,
    p.Extracurricular_Activities, p.Sleep_Hours, p.Previous_Scores, p.Motivation_Level,
    p.Internet_Access, p.Tutoring_Sessions, p.Family_Income, p.Teacher_Quality,
    p.School_Type, p.Peer_Influence, p.Physical_Activity, p.Learning_Disabilities,
    p.Parental_Education_Level, p.Distance_from_Home, p.Gender, p.Exam_Score
FROM staging_performance p
JOIN student_analytics_dw.dim_student s ON p.student_id::INT = s.student_id
JOIN student_analytics_dw.dim_health h ON p.student_id::INT = h.student_id
JOIN student_analytics_dw.dim_support sp ON p.student_id::INT = sp.student_id;
