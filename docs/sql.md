# Running SQL with Athena

```sql
SELECT *
FROM hmda.hmda
LIMIT 10
```

```sql
SELECT COUNT(*)
FROM hmda.hmda
```

![Count All](_static/count-all.png)

```
SELECT activity_year, COUNT(*)
FROM hmda.hmda
GROUP BY activity_year
```