-- remove the £ from price column
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');

-- Adjusting a boolean column to more logical values
UPDATE dim_products
SET still_available = REPLACE(still_available,'Removed','False')
SET still_available = REPLACE(still_available,'still_available','True');

-- casting all datatypes correctly 
ALTER TABLE dim_products ALTER COLUMN product_price TYPE FLOAT USING product_price::float;
ALTER TABLE dim_products ALTER COLUMN weight TYPE FLOAT USING product_price::float;
ALTER TABLE dim_products ALTER COLUMN "EAN" TYPE VARCHAR(255);
ALTER TABLE dim_products ALTER COLUMN product_code TYPE VARCHAR(255);
ALTER TABLE dim_products ALTER COLUMN date_added TYPE DATE USING date_added::date;
ALTER TABLE dim_products ALTER COLUMN uuid TYPE uuid USING uuid::uuid;
ALTER TABLE dim_products ALTER COLUMN still_available TYPE BOOL USING still_available::boolean;
ALTER TABLE dim_products ALTER COLUMN weight_class TYPE VARCHAR(255);

ALTER TABLE dim_products RENAME COLUMN removed TO still_available;