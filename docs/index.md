# First Athena Query

How to analyze millions of records in seconds with Amazon Web Services and SQL

## What you will learn

We’ve all been there. Excel locks up. Your dataframe can’t hang. And that damn SQL query has been running for two days now.

There’s no way around it. The database you're working on is just too big for your laptop to handle.

This tutorial offers a solution: Amazon Athena. Follow along and you will learn how to rip through records with the power of SQL.

## Who can take it

This course is free. Previous experience working with Amazon Web Services and SQL will come in handy, but anyone with good attitude is qualified to take the class. You will be charged for the AWS resources you use, so a credit card is required.

## Table of contents

* [What is Athena?](#what-is-athena)
* [How do newsrooms use it?](#how-do-newsrooms-use-it)
* [Setting up an AWS account](#setting-up-an-aws-account)
* [Creating an s3 bucket to store data](#creating-an-s3-bucket-to-store-data)
* [Creating a database table in Athena](#creating-a-database-table-in-athena)
* [Running your first query](#running-your-first-query)
* [Automating queries with Python](#automating-queries-with-python)

## What is Athena?

Athena is the name of cloud-computing tool offered by Amazon Web Services that allows you to query static data files using SQL. It can analyze extremely large datasets in seconds without a traditional server or database; You only pay for the data you store and the queries you run.

## How do newsrooms use it?

TK TK TK

## Setting up an AWS account

The first step is to create an Amazon Web Services account, if you don't already have. Go to [aws.amazon.com](https://aws.amazon.com/) and click the button that says "Create an AWS account" in the upper right corner.

![AWS splash page](_static/aws-splash.png)

You'll provide a root email address and a name for the account. And then you'll be asked to verify your email. Then you'll enter a password, contact information and a payment method. You'll also have to verify your phone number. Once that's completed, you'll be congratulated for your wherewithal.

![AWS congrats](_static/aws-congrats.png)

Now you're ready to sign into the AWS Management Console, where you can access all of the services it offers.

![AWS console](_static/aws-console.png)


## Creating an s3 bucket to store data

Now that you have an AWS account, you need to create a place to store your data. Amazon S3 is a cloud storage service that allows you to store static files in a folder known as a bucket. Our next step is to create a bucket to hold the dataset we'll be using in this tutorial.

You should go to the search bar at the top of the console and search "S3". Then click on the link it offers.

![AWS S3 search](_static/search-s3.png)

That will take you to a landing page for the service that will offer a large button that says "Create bucket." Click it.

![Bucket button](_static/bucket-button.png)

You can create a general purpose bucket with all of the default settings. Just make sure to give it a unique name. Then click "Create bucket" at the bottom of the form.

![Create bucket](_static/create-bucket.png)

Now you have a bucket. Click on its name to open it up.

![Bucket list](_static/bucket-list.png)

Now it's time to upload the data we'll be using in this tutorial, which is TK TK TK

## Creating a database table in Athena

TK TK TK

## Running your first query

TK TK TK

## Automating queries with Python

Running queries in Athena is great, but automating them in Python is even better. It could allow you run queries on a schedule, or to loop through a list of queries and run them without having to click buttons in the console.

Accessing Amazon Web Services with Python requires that you first establish an API key with permission to access the services you want to use. You can do that by clicking on the pulldown menu in the far upper right corner of the console and selecting "Security Credentials."

![Settings pulldown](_static/account-menu.png)

Then scroll down to the "Access keys" section and click the button that says "Create access key."

![Keys section](_static/keys-section.png)

Now you can create a root key pair by checking the box and clicking the button that says "Create access key."

![Keys section](_static/keys-consent.png)

The final screen will show you the key's ID and secret. I've redacted my pair in the example below.

![Keys screen](_static/redacted-keys.png)

Copy and paste them into a text file for safekeeping. You will not be able to see the secret key again. They are what Python will use to gain access to AWS from outside the console.

## About this class

This guide was prepared by [Ben Welsh](https://palewi.re/who-is-ben-welsh/) and [Katlyn Alo](https://www.linkedin.com/in/katalo/) for [a training session](https://schedules.ire.org/nicar-2025/index.html#2080) at the National Institute for Computer-Assisted Reporting’s 2025 conference in Minnapolis. Some of the copy was written with the assistance of GitHub’s Copilot, an AI-powered text generator. The materials are available as free and [open source on GitHub](https://github.com/palewire/first-athena-query).
