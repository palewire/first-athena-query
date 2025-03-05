import athena

sql = "SELECT * FROM hmda.loans LIMIT 10"
df = athena.get_dataframe(sql, verbose=True)
print(df.head())