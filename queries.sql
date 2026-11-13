INSERT INTO researchers (full_name, academic_degree, email)
SELECT 
    'Дослідник ' || id || ' ' || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
    (ARRAY['Магістр', 'Кандидат наук', 'Доктор наук', 'PhD'])[floor(random()*4 + 1)],
    'researcher_' || id || '_' || trunc(random()*100000) || '@lab.kpi.ua'
FROM generate_series(1, 100000) AS id;

SELECT r.full_name, e.title, e.start_date, e.status
FROM researchers r
JOIN experiments e ON r.researcher_id = e.lead_researcher_id
WHERE r.full_name LIKE '%Коваленко%' AND e.start_date >= '2026-01-01'
ORDER BY e.start_date DESC;

SELECT e.title, SUM(ee.usage_hours) as total_hours
FROM experiments e
JOIN experiment_equipment ee ON e.experiment_id = ee.experiment_id
GROUP BY e.experiment_id, e.title
HAVING SUM(ee.usage_hours) BETWEEN 10 AND 50
ORDER BY total_hours DESC;

SELECT eq.name, eq.manufacturer, e.title, e.status
FROM equipment eq
JOIN experiment_equipment ee ON eq.equipment_id = ee.equipment_id
JOIN experiments e ON ee.experiment_id = e.experiment_id
WHERE eq.manufacturer ILIKE '%FLIR%' AND e.status = 'Завершений';