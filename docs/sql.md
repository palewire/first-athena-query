# Running SQL with Athena

```sql
SELECT *
FROM hmda.loans
LIMIT 10
```

![Select All](_static/limit.png)

![Select All](_static/limit-result.png)

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