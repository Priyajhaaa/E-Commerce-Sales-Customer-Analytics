# 📊 E-Commerce Sales & Customer Analytics

An end-to-end **Data Analytics project** focused on analyzing e-commerce sales, customer behavior, product performance, orders, and payment trends using **Python, SQL, and Power BI**.

## 🎯 Project Objective

The objective of this project was to transform raw e-commerce transaction data into meaningful business insights and build an interactive Power BI dashboard for performance analysis.

## 🗂️ Dataset

The project contains 5 main tables:

* **Customers** — Customer information
* **Products** — Product details and categories
* **Orders** — Order information, dates, status, and shipping state
* **Order Items** — Quantity, price, discount, and item-level transactions
* **Payments** — Payment methods and payment amounts

## 🔍 Key Business Questions

* What is the total revenue and number of orders?
* What is the order completion and refund rate?
* Which product categories generate the highest revenue?
* Which products are the top performers?
* Which states generate the highest revenue?
* How does revenue change monthly and yearly?
* Which payment methods contribute the most revenue?
* Who are the highest-value customers?
* How can customers be segmented based on revenue?

## 🧹 Data Preparation

Python and Pandas were used for:

* Data inspection and quality checks
* Data type preparation
* Revenue calculation
* Merging related datasets
* Filtering relevant transactions
* Customer-level revenue analysis
* Customer segmentation

## 🗄️ SQL Analysis

PostgreSQL was used to perform business-oriented SQL analysis including:

* Aggregations and filtering
* JOIN operations
* GROUP BY analysis
* Revenue analysis
* Product and customer ranking
* Monthly and yearly trends
* Customer segmentation
* CTEs
* Window functions such as `RANK()` and `LAG()`

The complete SQL analysis is available in:

`ecommerce_sales_analysis.sql`

## 🐍 Python Analysis

Python and Pandas were used for exploratory analysis and customer/revenue analysis.

The Python analysis is available in:

`ecommerce_sales_analysis.py`

## 📊 Power BI Dashboard

An interactive Power BI dashboard was created to visualize:

* Revenue & Order KPIs
* Revenue trends
* Category performance
* State-wise revenue
* Payment method analysis
* Top products
* Top customers
* Customer segmentation

Power BI file:

`E-Commerce-Sales-Customer-Analytics.pbix`

## 💡 Key Insights

| Metric                         |         Result |
| ------------------------------ | -------------: |
| Total Revenue                  |       ₹289.20M |
| Total Orders                   |         15,000 |
| Completed Orders               |         12,325 |
| Completion Rate                |         82.17% |
| Refund Rate                    |          7.53% |
| Highest Revenue Category       | Home & Kitchen |
| Highest Revenue State          |    Maharashtra |
| Highest Revenue Payment Method |            UPI |

### Customer Segmentation

* **Low Value:** 2,384 customers
* **Medium Value:** 1,970 customers
* **High Value:** 189 customers

## 🛠️ Tools & Technologies

**Python | Pandas | SQL | PostgreSQL | Power BI | DAX**

## 📁 Project Structure

```text
E-Commerce-Sales-Customer-Analytics/
│
├── README.md
├── ecommerce_sales_analysis.py
├── ecommerce_sales_analysis.sql
├── E-Commerce-Sales-Customer-Analytics.pbix
├── dashboard.png
│
├── customers_cleaned.csv
├── products_cleaned.csv
├── orders_cleaned.csv
├── order_items_cleaned.csv
└── payments_cleaned.csv
```

## 🚀 Key Takeaway

This project helped me strengthen my skills in **data cleaning, SQL analysis, Python/Pandas, data modeling, DAX, data visualization, customer segmentation, and business storytelling**.

The project demonstrates an end-to-end approach to transforming raw transactional data into actionable business insights.

---

### 👩‍💻 Project by Priya

**Data Analyst | Python | SQL | Power BI**

Open to **Junior Data Analyst / Data Analyst opportunities**.
