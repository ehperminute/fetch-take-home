# Data Engineering Take Home: ETL off a SQS Queue
This project focuses on creating a small application that can read from an AWS
SQS Queue, transform that data, then write to a Postgres database.
Objectives:
1. read JSON data containing user login behavior from an AWS SQS Queue.
2. The fields `device_id` and `ip` should be masked, but in a way where it is easy for data analysts to identify duplicate
values in those fields.
3. Once the JSON data is flattened and those two fields are masked, write each
record to a Postgres database that is made available via a custom postgres image that
has the tables pre created.
 target table's DDL is:
-- Creation of user_logins table  
CREATE TABLE IF NOT EXISTS user_logins
  (  
    user_id varchar(128),  
    device_type varchar(32),  
    masked_ip varchar(256),  
    masked_device_id varchar(256),  
    locale varchar(32),  
    app_version integer,  
    create_date date  
  );  

# Project setup
# Requirements:
- Python 3.9+  
- Docker  
- Docker Compose  
- pip  
- AWS CLI (for local testing)

# Installation:

1. Clone the repository.

2. Install the required Python packages using pip:
```
pip install -r requirements.txt
```
3. Set up the local development environment using Docker Compose:
```
docker compose up
```
4. Test local access:

- Read a message from the queue using awslocal:

```
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
```
- Connect to the PostgreSQL database and verify the table is created:
```
psql -d postgres -U postgres -p 5432 -h localhost -W
```
Postgres creds:  
a. Password: postgres  
b. Username: postgres

- Then, run the SQL SELECT statement in the psql console:

```sql
SELECT * FROM user_logins;
```

# Running the ETL Pipeline:
To run the ETL pipeline, execute the following command from the root of the project directory:

```
python -m main.py
```
This command will run mainloop within which the app polls the SQS queue, reads and process the messages to extract and masks the necessary data and insert the records into the PostgreSQL database after.
# Assimptions:
- The PII data can be masked using a one-way hashing algorithm to ensure the original data cannot be restored, while saving ability of keeping track of identical entries
- The PostgreSQL database is set up with the correct table schema to store the processed records. (Which was not true, and we had to change the datatype of one of the columns)
- The provided Docker Compose file sets up the local development environment, and no additional configuration is required for local testing.
- All the messages from the message queue contain data for all the columns of the given table (was wrong, occasional nulls appear)
# PII recover
Impossible in case of using a hash function.
# Ways to improve:
1. Widen functionality to make it more omnipurposal and useful for other tables or databases
2. Add error handling and stability and performance tests
3. Optimize data processing and improve error preventing logic by collating the tables schemas with the actual data coming from the SQS queue
4. Consider using encryption algorithms instead of hashing ones in order to provide revirsibility of the masked data, in case if needed.
5. Consider using another hash funstion to reduce probability of collisions.
6. Add a jupyter notebook for a more convenient demonstration

# Deployment
To deploy this application we could use a container orchestration server like Kubernetes or run on our own dedicated server integrating it to the Airflow pipeline and using it for monitoring some databases.

# Scaling

In case of a significant dataset growth we could implement some performance tweaks including utilizing distributed computing frameworks, such as Apache Hadoop or Apache Spark, could make manipulation the data more efficient. Or implementing indexing could enhance query performance by creating indexes on frequently queried attributes by quickly locating the required data without scanning the entire dataset. 
