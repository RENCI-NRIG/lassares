SELECT SETVAL('meas_web_mscnt_id_seq', 99);
UPDATE meas_web_mscnt SET id = DEFAULT;
CREATE VIEW drf_mscnt AS 
  SELECT id AS id, job_id, bore_id, instrument, chemical_id, measurement_value, units, (date + time)::timestamp AS timestamp, status, comment, geom FROM meas_web_mscnt;
CREATE VIEW drf_mscnt_timestamp AS 
  SELECT (date + time)::timestamp AS id, (date + time)::timestamp AS label FROM meas_web_mscnt;
CREATE VIEW drf_mscnt_jobid AS 
  SELECT DISTINCT job_id as id, job_id as label FROM meas_web_mscnt;
SELECT SETVAL('meas_web_gcmv_id_seq', 99);\nUPDATE meas_web_gcmv SET id = DEFAULT;
CREATE VIEW drf_gcmv AS 
  SELECT id AS id, job_id, bore_id, instrument, chemical_id, measurement_value, units, (date + time)::timestamp AS timestamp, status, comment, geom FROM meas_web_gcmv;
CREATE VIEW drf_gcmv_timestamp AS 
  SELECT (date + time)::timestamp AS id, (date + time)::timestamp AS label FROM meas_web_gcmv;
CREATE VIEW drf_gcmv_jobid AS SELECT DISTINCT job_id as id, job_id as label FROM meas_web_gcmv;
