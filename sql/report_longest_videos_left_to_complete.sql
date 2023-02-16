-- Total Duration 186202000

DO $$
DECLARE longest_videos_total int;
BEGIN
  	longest_videos_total := (SELECT sum(duration)
	FROM public.unit u
	JOIN video_additional va on u.id = va.id_unit
	WHERE 
	u.type = 1 
	AND u.is_major = true 
	AND duration > 300000);
	
	CREATE TEMP TABLE report_longest_videos_left_to_complete (duration_left text, percentage_left text) ON COMMIT DROP;
	
	INSERT INTO report_longest_videos_left_to_complete
	SELECT TO_CHAR(((sum(duration) / 1000) || ' second')::interval, 'HH24:MI:SS'),
	concat(round(sum(duration)*100 / longest_videos_total), '%')
	FROM public.unit u
	LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
	JOIN video_additional va on u.id = va.id_unit
	WHERE 
	mgt.id_unit IS null AND 
	u.type = 1 
	AND u.is_major = true 
	AND duration > 300000;
	
END $$;

SELECT * FROM report_longest_videos_left_to_complete