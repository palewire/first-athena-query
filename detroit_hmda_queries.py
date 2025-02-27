import athena
from detroit_census_tracts import DETROIT_CENSUS_TRACTS

"""
Let's see how many loans were applied for in Detroit between 2018 and 2022.

"""
sql = f"SELECT * FROM database WHERE census_tract IN {tuple(DETROIT_CENSUS_TRACTS)}"
q_id = athena.query(sql, verbose=True)
print(q_id)

"""
How many mortgage loans were applied for in Detroit between 2018 and 2022?

Loan purpose codes:
1 - Home purchase
2 - Home improvement
31 - Refinancing
32 - Cash-out refinancing
4 - Other purpose
5 - Not applicable

(See: https://ffiec.cfpb.gov/documentation/tools/data-browser/data-browser-filters#loan-purpose-loan_purpose)

"""
sql = f"SELECT * FROM database WHERE census_tract IN {tuple(DETROIT_CENSUS_TRACTS)} AND loan_purpose=1"
q_id = athena.query(sql, verbose=True)
print(q_id)

"""
Can we group the loans by applicants' race?
"""
sql = f"SELECT * FROM database WHERE census_tract IN {tuple(DETROIT_CENSUS_TRACTS)} AND loan_purpose=1 GROUP BY derived_race"
q_id = athena.query(sql, verbose=True)
print(q_id)

"""
How many of those mortgage loans were denied?

Action taken codes:
1 - Loan originated
2 - Application approved but not accepted
3 - Application denied
4 - Application withdrawn by applicant
5 - File closed for incompleteness
6 - Purchased loan
7 - Preapproval request denied
8 - Preapproval request approved but not accepted

(See: https://ffiec.cfpb.gov/documentation/tools/data-browser/data-browser-filters#action-taken-action_taken)
"""

sql = f"SELECT * FROM database WHERE census_tract IN {tuple(DETROIT_CENSUS_TRACTS)} AND loan_purpose=1 AND action_taken=3 GROUP BY derived_race"
q_id = athena.query(sql, verbose=True)
print(q_id)