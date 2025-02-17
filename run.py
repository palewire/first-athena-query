import athena

sql = "SELECT * FROM database"
q_id = athena.query(sql, verbose=True)
print(q_id)