import athena

sql = "SELECT * FROM database"
df = athena.get_dataframe(sql, verbose=True)
print(df.head())