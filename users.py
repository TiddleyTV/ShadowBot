def check_user_exists(cursor,guild,userid):
	query = "SELECT * FROM users WHERE discord_name = '" + str(userid) + "' AND discord_guild = '" + str(guild) + "'"
	cursor.execute(query)
	row = cursor.fetchone()
	if row is not None:
		return True
	return False



def add_user(cursor,guild,userid):
	# If user exists, leave their record alone
	if check_user_exists(cursor,guild,userid):
		return True

	# If they don't, add them
	query = "INSERT INTO users(discord_guild,discord_name) VALUES(%s,%s)"
	args = (str(guild),str(userid))

	cursor.execute(query, args)
	return True


def del_user(cursor,guild,userid):
	if check_user_exists(cursor,guild,userid):
		query = "DELETE FROM users WHERE discord_name = %s AND discord_guild = %s"
		args = (str(userid),str(guild))
		cursor.execute(query)
	return True


def set_wow_main(cursor,guild,userid,wowmain):
	if check_user_exists(cursor,guild,userid):
		query = "UPDATE users SET wow_main = %s WHERE discord_name = %s AND discord_guild = %s"
		args = (str(wowmain),str(userid),str(guild))
		cursor.execute(query, args)
		return True
	return False


def get_wow_main(cursor,guild,userid):
	if check_user_exists(cursor,guild,userid):
		query = "SELECT wow_main FROM users WHERE discord_name = %s AND discord_guild = %s"
		args = (str(userid),str(guild))
		cursor.execute(query, args)
		row = cursor.fetchone()
		wowmain = str(row[0])
		return wowmain
	return False


