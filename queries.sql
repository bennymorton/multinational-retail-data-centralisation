-- How many stores does the business have and in which countries?
SELECT country_code, COUNT(country_code) AS total_no_stores
FROM dim_store_details
GROUP BY country_code;

-- Which locations currently have the most stores?
SELECT locality, COUNT(locality) AS total_no_stores
FROM dim_store_details
GROUP BY locality;

-- Which months produce the most sales typically
SELECT SUM(product_price) AS total_no_sales, dim_date_times.month
FROM dim_products
JOIN orders_table
ON dim_products.product_code = orders_table.product_code
JOIN dim_date_times
ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY month;

-- What percentage of sales come through each type of store?
SELECT 
	store_type,
	SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales,
	COUNT(store_type)*100/(SELECT COUNT(*) FROM orders_table) AS percentage_total
FROM orders_table
JOIN dim_store_details
ON orders_table.store_code = dim_store_details.store_code
JOIN dim_products
ON orders_table.product_code = dim_products.product_code
GROUP BY store_type;

-- Which month in each year produced the most sales?
SELECT 
	SUM(product_price*product_quantity) AS total_sales,
	year,
	month
FROM orders_table
JOIN dim_products
ON orders_table.product_code = dim_products.product_code
JOIN dim_date_times
ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY year, month
ORDER BY total_sales DESC
LIMIT 5;

-- What is the staff headcount?
SELECT SUM(staff_numbers) AS total_staff_numbers,
country_code
FROM dim_store_details
GROUP BY country_code;

-- Which German store type is selling the most?
SELECT 
	SUM(product_price*product_quantity) AS total_sales,
	store_type
FROM orders_table
JOIN dim_products
ON orders_table.product_code = dim_products.product_code
JOIN dim_store_details
ON orders_table.store_code = dim_store_details.store_code
WHERE country_code = 'DE'
GROUP BY store_type;

-- How quickly is the company making sales?
SELECT
	year, 
	AVG(next_sale_time - full_datetime) AS avg_difference
FROM (
	WITH cte AS (
		SELECT
			year,
			year || '-' || month || '-' || day || ' ' || timestamp 
			AS full_datetime
		FROM dim_date_times
		ORDER BY full_datetime
	)
	SELECT 
		year, 
		TO_TIMESTAMP(full_datetime, 'YYYY-MM-DD HH24:MI:SS:MS') AS full_datetime,
		TO_TIMESTAMP(
			LEAD(full_datetime,1) OVER (
				ORDER BY full_datetime
			), 'YYYY-MM-DD HH24:MI:SS:MS') AS next_sale_time
	FROM cte
) AS differences
GROUP BY year
ORDER BY year DESC
LIMIT 5;

