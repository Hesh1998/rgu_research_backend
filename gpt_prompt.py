content_system = """
You are a Databricks SQL generator.

Your task:
Given a data warehouse schema and a natural language question, generate a single valid Databricks SQL query that correctly answers it.

Rules:
- Use only fields and joins defined in the schema.
- Follow Databricks SQL (Delta Lake) syntax.
- Output only valid JSON in this exact format:
  {"query": "SELECT ..."}
- Do not include comments, explanations, or any other text.
"""


content_user = """
Data warehouse: Sales DWH (Snowflake schema)
Fact table: dwh.gold.sales_fact(order_number INT, line_item INT, order_date DATE, delivery_date DATE, customer_sk INT, store_sk INT, product_sk INT, quantity INT, currency_sk BIGINT)
Primary key: (order_number, line_item)

Dimensions:
- dwh.gold.customer_dim(customer_sk INT, gender STRING, name STRING, country_state_sk BIGINT)
- dwh.gold.store_dim(store_sk INT, country_state_sk BIGINT, square_meters INT, open_date DATE)
- dwh.gold.product_dim(product_sk INT, product_name STRING, brand STRING, color STRING, unit_cost_usd DECIMAL(10,2), unit_price_usd DECIMAL(10,2), category_sk BIGINT)
- dwh.gold.currency_dim(currency_sk BIGINT, date DATE, currency STRING, exchange DECIMAL(8,5))
- dwh.gold.country_state_dim(country_state_sk BIGINT, country STRING, state STRING)
- dwh.gold.category_dim(category_sk BIGINT, category STRING, subcategory STRING)

Joins:
sales_fact.customer_sk = customer_dim.customer_sk
sales_fact.store_sk = store_dim.store_sk
sales_fact.product_sk = product_dim.product_sk
sales_fact.currency_sk = currency_dim.currency_sk
customer_dim.country_state_sk = country_state_dim.country_state_sk
store_dim.country_state_sk = country_state_dim.country_state_sk
product_dim.category_sk = category_dim.category_sk

Question:
"""