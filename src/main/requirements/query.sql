SELECT 
	AUU.id 'ID'
	,AUU.username 'USER'
	,AUU.email 'EMAIL'
	,AUU.is_verified 'VERIFY'
	,AUU.date_joined 'CREATED'
	,AUU.first_name 'NAME'
	,AUT.key 'TOKEN'
	,AUU.acc_hash 'HASH'
	,AUU.acc_hash_expiration 'HASH DATE'
	,AUU.pass_token 'PASS'
	,AUU.pass_token_expiration 'PASS DATE'
	,AUU.is_superuser 'SUPER'
	,CASE
		WHEN AUU.is_active = 1 THEN 'ACTIVE'
		WHEN AUU.is_active = 2 THEN 'BANNED'
	END 'STATUS'
	,AUU.is_staff 'STAFF'

FROM
	authentication_user AUU

LEFT JOIN
	authtoken_token AUT
ON
	AUU.ID = AUT.user_id