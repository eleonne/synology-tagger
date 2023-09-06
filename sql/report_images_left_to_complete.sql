DO $$
DECLARE images_total int;
BEGIN
  	images_total := (SELECT count(*)
	FROM public.unit u
	WHERE u.type = 0 AND u.is_major = true);
	
	CREATE TEMP TABLE report_images_left_to_complete (total int, percentage_left decimal, _total int) ON COMMIT DROP;
	
	INSERT INTO report_images_left_to_complete
	SELECT count(*), count(*) * 100 / images_total, images_total
	FROM public.unit u
	LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
	WHERE mgt.id_unit IS null AND u.type = 0 AND u.is_major = true;
	
END $$;

SELECT * FROM report_images_left_to_complete