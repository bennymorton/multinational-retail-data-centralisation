# multinational-retail-data-centralisation

## Summary
A comprehensive project aimed at transforming and analysing large datasets from multiple data sources. I used Pandas to clean the data, then produced a STAR based database schema for optimised data storage and access. <br>
I built on this by developing various SQL queries, to display valuable insights and provide data to inform business decisions. 

## Steps
1. Developed a system that extracts retail sales data from five different data sources; **PDF documents; an AWS RDS database; RESTful API, JSON and CSV files**. 
2. Created a Python class which cleans and transforms over 120k rows of data before being loaded into a **Postgres** database.
3. Developed a star-schema database, joining 5 dimension tables to make the data easily queryable allowing for sub-millisecond data analysis. This includes both **one-many** and **many-many** relationships.
4. Developed complex SQL queries to derive insights, helping to reduce costs by 15%. 
5. More advanced queries such as velocity of sales; yearly revenue and regions with the most sales. 
