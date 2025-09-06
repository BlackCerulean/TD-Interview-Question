-- CREATE OR REPLACE VIEW `my_project.my_dataset.top2_sales_per_class` AS
-- Product Class
WITH product_class AS (
  SELECT 1 AS product_class_id, 'Electronics' AS product_class_name UNION ALL
  SELECT 2, 'Clothing' UNION ALL
  SELECT 3, 'Home Appliances' UNION ALL
  SELECT 4, 'Groceries'
),

-- Product
product AS (
  SELECT 101 AS product_id, 'Smartphone' AS product_name, 699.99 AS retail_price, 1 AS product_class_id UNION ALL
  SELECT 102, 'Laptop', 1199.99, 1 UNION ALL
  SELECT 103, 'T-Shirt', 19.99, 2 UNION ALL
  SELECT 104, 'Jeans', 49.99, 2 UNION ALL
  SELECT 105, 'Microwave Oven', 149.99, 3 UNION ALL
  SELECT 106, 'Vacuum Cleaner', 199.99, 3 UNION ALL
  SELECT 107, 'Rice (5kg)', 12.50, 4 UNION ALL
  SELECT 108, 'Olive Oil (1L)', 8.99, 4 UNION ALL
  SELECT 109, 'Headphones', 79.99, 1 UNION ALL
  SELECT 110, 'Refrigerator', 899.99, 3
),

-- Sales Transaction
sales_transaction AS (
  SELECT 1001 AS transaction_id, 101 AS product_id, 2 AS quantity UNION ALL
  SELECT 1002, 102, 1 UNION ALL
  SELECT 1003, 103, 5 UNION ALL
  SELECT 1004, 104, 3 UNION ALL
  SELECT 1005, 105, 1 UNION ALL
  SELECT 1006, 106, 2 UNION ALL
  SELECT 1007, 107, 10 UNION ALL
  SELECT 1008, 108, 6 UNION ALL
  SELECT 1009, 109, 4 UNION ALL
  SELECT 1010, 110, 1
),

-- Summarize the sales of this store
sales_summary AS (
  SELECT 
    pc.product_class_name,
    p.product_id,
    p.product_name,
    SUM(st.quantity) as total_sold,
    SUM(st.quantity) * p.retail_price AS sales_value
  FROM sales_transaction st
  JOIN product p 
    ON st.product_id = p.product_id
  JOIN product_class pc 
    ON p.product_class_id = pc.product_class_id
  GROUP BY pc.product_class_name, p.product_id, p.product_name, p.retail_price
),

-- Product Ranking 
ranked AS (
  SELECT 
    product_class_name,
    product_id,
    product_name,
    sales_value,
    ROW_NUMBER() OVER (
      PARTITION BY product_class_name 
      ORDER BY sales_value DESC, total_sold ASC
    ) AS rank
  FROM sales_summary
)

SELECT product_class_name, rank, product_name, sales_value
FROM ranked
WHERE rank <= 2
ORDER BY product_class_name, sales_value DESC;