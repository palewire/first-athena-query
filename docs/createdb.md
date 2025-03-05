# Creating an Athena database

Once your data and S3 are ready, search for "Athena" in the bar at the top of the Amazon's console. Click on the first option it returns.

That will take you to the Athena control panel, where you will be see a box at the top of the page prompting you to configure the location of query results. Hit the "Edit settings" button it presents.

![Athena welcome](_static/athena-welcome.png)

That will take your to a form. Click on "Browse S3."

![Athena output form](_static/athena-output-form.png)

Then navigate to the query output folder you created and select it.

![Select output folder](_static/select-output-folder.png)

Submit that without any additional configuration and your Athena panel should show that it's ready to work. You should then click on the "Editor" tab near the top left of the page to return to Athena's query panel.

![Ready output folder](_static/output-folder-is-ready.png)

Now we finally start in with SQL. The first step is to create a database in Athena's system that will store your data tables. You can name it whatever you like, but you should try to keep it clear and short. Then you draft the classic `CREATE DATABASE` statement and submit it by hitting the "Run" button.

In our example, this will be:

```sql
CREATE DATABASE hmda
```

![Create db](_static/create-db.png)

```sql
CREATE EXTERNAL TABLE hmda (
  activity_year int,
  lei string,
  state_code string,
  county_code string,
  census_tract string,
  derived_loan_product_type string,
  derived_dwelling_category string,
  derived_ethnicity string,
  derived_race string,
  derived_sex string,
  action_taken int,
  purchaser_type int,
  preapproval int,
  loan_type int,
  loan_purpose int,
  lien_status int,
  reverse_mortgage int,
  open_end_line_of_credit int,
  business_or_commercial_purpose int,
  debt_to_income_ratio string,
  applicant_credit_score_type string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://first-athena-query/example-data/'
TBLPROPERTIES ('skip.header.line.count'='1')
```