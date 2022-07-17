CREATE UNIQUE INDEX IF NOT EXISTS one_hometeam_per_match
	ON matchtoteam (match_id, is_home_team);