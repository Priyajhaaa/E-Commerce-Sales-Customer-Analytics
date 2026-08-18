import pandas as pd

customers = pd.read_csv("customers.csv")

print(customers.head())

print(customers.shape)

print(customers.columns)

print(customers.info())

print(customers.isnull().sum())

print(customers.duplicated().sum())

print(customers["gender"].value_counts())

print(customers["age"].describe())

customers["city"] = customers["city"].fillna("Unknown")
customers["state"] = customers["state"].fillna("Unknown")

print(customers.isnull().sum())

products = pd.read_csv("products.csv")

print(products.head())

print(products.shape)

print(products.info())

print(products.isnull().sum())

print(products.duplicated().sum())

products["sub_category"] = products["sub_category"].fillna("Unknown")

print(products.isnull().sum())

orders = pd.read_csv("orders.csv")

print(orders.head())

print(orders.shape)

print(orders.info())

print(orders.isnull().sum())

print(orders.duplicated().sum())

# Remove duplicate rows
orders = orders.drop_duplicates()

# Handle missing payment methods
orders["payment_method"] = orders["payment_method"].fillna("Unknown")

# Check again
print(orders.isnull().sum())
print(orders.duplicated().sum())
print(orders.shape)

order_items = pd.read_csv("order_items.csv")

print(order_items.head())

print(order_items.shape)

print(order_items.info())

print(order_items.isnull().sum())

print(order_items.duplicated().sum())

payments = pd.read_csv("payments.csv")

print(payments.head())

print(payments.shape)

print(payments.info())

print(payments.isnull().sum())

print(payments.duplicated().sum())

customers["signup_date"] = pd.to_datetime(customers["signup_date"])

orders["order_date"] = pd.to_datetime(orders["order_date"])

payments["payment_date"] = pd.to_datetime(payments["payment_date"])

print(customers.dtypes)
print(orders.dtypes)
print(payments.dtypes)

customers.to_csv("cleaned_data/customers_cleaned.csv", index=False)

products.to_csv("cleaned_data/products_cleaned.csv", index=False)

orders.to_csv("cleaned_data/orders_cleaned.csv", index=False)

order_items.to_csv("cleaned_data/order_items_cleaned.csv", index=False)

payments.to_csv("cleaned_data/payments_cleaned.csv", index=False)

print("All cleaned files saved successfully!")

# =========================
# PYTHON EDA
# STEP 1: LOAD CLEANED DATA
# =========================

customers = pd.read_csv("cleaned_data/customers_cleaned.csv")
products = pd.read_csv("cleaned_data/products_cleaned.csv")
orders = pd.read_csv("cleaned_data/orders_cleaned.csv")
order_items = pd.read_csv("cleaned_data/order_items_cleaned.csv")
payments = pd.read_csv("cleaned_data/payments_cleaned.csv")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)

# =========================
# STEP 2: DESCRIPTIVE STATISTICS
# =========================

print("\n--- Customers Summary ---")
print(customers.describe())

print("\n--- Products Summary ---")
print(products.describe())

print("\n--- Orders Summary ---")
print(orders.describe())

print("\n--- Order Items Summary ---")
print(order_items.describe())

print("\n--- Payments Summary ---")
print(payments.describe())

# =========================
# STEP 3: MISSING VALUES CHECK
# =========================

print("\n--- Missing Values ---")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())

print("\nPayments:")
print(payments.isnull().sum())

# =========================
# STEP 4: DUPLICATE CHECK
# =========================

print("\n--- Duplicate Rows ---")

print("Customers:", customers.duplicated().sum())
print("Products:", products.duplicated().sum())
print("Orders:", orders.duplicated().sum())
print("Order Items:", order_items.duplicated().sum())
print("Payments:", payments.duplicated().sum())

# =========================
# STEP 5: ORDERS & REVENUE OVERVIEW
# =========================

total_orders = len(orders)

completed_orders = len(
    orders[orders["order_status"] == "Completed"]
)

completed_order_items = order_items[
    order_items["order_id"].isin(
        orders.loc[
            orders["order_status"] == "Completed",
            "order_id"
        ]
    )
]

total_revenue = (
    completed_order_items["quantity"]
    * completed_order_items["unit_price"]
    * (1 - completed_order_items["discount"])
).sum()

print("\n--- Orders & Revenue Overview ---")
print("Total Orders:", total_orders)
print("Completed Orders:", completed_orders)
print("Total Revenue:", round(total_revenue, 2))

# =========================
# STEP 6: ORDER STATUS DISTRIBUTION
# =========================

status_counts = orders["order_status"].value_counts()

print("\n--- Order Status Distribution ---")
print(status_counts)

# =========================
# STEP 7: REVENUE BY CATEGORY
# =========================

completed_order_ids = orders.loc[
    orders["order_status"] == "Completed",
    "order_id"
]

completed_items = order_items[
    order_items["order_id"].isin(completed_order_ids)
].copy()

completed_items["revenue"] = (
    completed_items["quantity"]
    * completed_items["unit_price"]
    * (1 - completed_items["discount"])
)

category_revenue = (
    completed_items
    .merge(products[["product_id", "category"]], on="product_id")
    .groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Revenue by Category ---")
print(category_revenue.round(2))

# =========================
# STEP 8: TOP 10 PRODUCTS BY REVENUE
# =========================

product_revenue = (
    completed_items
    .merge(
        products[["product_id", "product_name", "category"]],
        on="product_id"
    )
    .groupby(
        ["product_id", "product_name", "category"]
    )["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- Top 10 Products by Revenue ---")
print(product_revenue.round(2))

# =========================
# STEP 9: STATE-WISE REVENUE
# =========================

state_revenue = (
    completed_items
    .merge(
        orders[["order_id", "shipping_state"]],
        on="order_id"
    )
    .groupby("shipping_state")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- State-wise Revenue ---")
print(state_revenue.round(2))

# =========================
# STEP 10: TOP 10 CUSTOMERS BY REVENUE
# =========================

customer_revenue = (
    completed_items
    .merge(
        orders[["order_id", "customer_id"]],
        on="order_id"
    )
    .merge(
        customers[["customer_id", "customer_name", "city", "state"]],
        on="customer_id"
    )
    .groupby(
        ["customer_id", "customer_name", "city", "state"]
    )["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- Top 10 Customers by Revenue ---")
print(customer_revenue.round(2))

# =========================
# STEP 11: CUSTOMER SEGMENTATION
# =========================

customer_revenue_all = (
    completed_items
    .merge(
        orders[["order_id", "customer_id"]],
        on="order_id"
    )
    .groupby("customer_id")["revenue"]
    .sum()
)

def customer_segment(revenue):
    if revenue < 50000:
        return "Low Value"
    elif revenue < 200000:
        return "Medium Value"
    else:
        return "High Value"

customer_segments = customer_revenue_all.apply(customer_segment)

segment_counts = customer_segments.value_counts()

print("\n--- Customer Segmentation ---")
print(segment_counts)

# =========================
# STEP 12: MONTHLY REVENUE
# =========================

completed_orders = orders[
    orders["order_status"] == "Completed"
][["order_id", "order_date"]].copy()

# Convert order_date to datetime
completed_orders["order_date"] = pd.to_datetime(
    completed_orders["order_date"]
)

monthly_revenue = (
    completed_items
    .merge(completed_orders, on="order_id")
)

monthly_revenue["month"] = (
    monthly_revenue["order_date"]
    .dt.to_period("M")
)

monthly_revenue = (
    monthly_revenue
    .groupby("month")["revenue"]
    .sum()
    .sort_index()
)

print("\n--- Monthly Revenue ---")
print(monthly_revenue.round(2))

# =========================
# STEP 13: MONTH-OVER-MONTH GROWTH
# =========================

monthly_growth = monthly_revenue.to_frame(name="revenue")

monthly_growth["previous_month_revenue"] = (
    monthly_growth["revenue"].shift(1)
)

monthly_growth["mom_growth_percentage"] = (
    (
        monthly_growth["revenue"]
        - monthly_growth["previous_month_revenue"]
    )
    / monthly_growth["previous_month_revenue"]
) * 100

print("\n--- Monthly Revenue Growth ---")
print(monthly_growth.round(2))

# =========================
# STEP 14: YEARLY REVENUE & YOY GROWTH
# =========================

yearly_revenue = (
    completed_orders.copy()
)

yearly_revenue["year"] = (
    yearly_revenue["order_date"].dt.year
)

yearly_revenue = (
    completed_items
    .merge(
        yearly_revenue[["order_id", "year"]],
        on="order_id"
    )
    .groupby("year")["revenue"]
    .sum()
    .sort_index()
)

yearly_analysis = yearly_revenue.to_frame(name="revenue")

yearly_analysis["previous_year_revenue"] = (
    yearly_analysis["revenue"].shift(1)
)

yearly_analysis["yoy_growth_percentage"] = (
    (
        yearly_analysis["revenue"]
        - yearly_analysis["previous_year_revenue"]
    )
    / yearly_analysis["previous_year_revenue"]
) * 100

print("\n--- Yearly Revenue & YoY Growth ---")
print(yearly_analysis.round(2))

# =========================
# STEP 15: PAYMENT METHOD ANALYSIS
# =========================

successful_payments = payments[
    payments["payment_status"] == "Success"
].copy()

payment_analysis = (
    successful_payments
    .groupby("payment_method")
    .agg(
        total_payment_amount=("amount", "sum"),
        successful_payments=("payment_id", "count")
    )
    .sort_values(
        "total_payment_amount",
        ascending=False
    )
)

payment_analysis["total_payment_amount"] = (
    payment_analysis["total_payment_amount"].round(2)
)

print("\n--- Payment Method Analysis ---")
print(payment_analysis)

# =========================
# STEP 16: PAYMENT SUCCESS RATE
# =========================

payment_success_rate = (
    payments
    .groupby("payment_method")
    .agg(
        total_attempts=("payment_id", "count"),
        successful_payments=("payment_status", lambda x: (x == "Success").sum())
    )
)

payment_success_rate["success_rate_percentage"] = (
    payment_success_rate["successful_payments"]
    / payment_success_rate["total_attempts"]
    * 100
)

payment_success_rate["success_rate_percentage"] = (
    payment_success_rate["success_rate_percentage"].round(2)
)

payment_success_rate = payment_success_rate.sort_values(
    "success_rate_percentage",
    ascending=False
)

print("\n--- Payment Success Rate ---")
print(payment_success_rate)

# =========================
# STEP 17: REFUND ANALYSIS
# =========================

refunded_payments = payments[
    payments["payment_status"] == "Refunded"
].copy()

total_refunds = len(refunded_payments)

affected_orders = refunded_payments["order_id"].nunique()

total_refund_amount = refunded_payments["amount"].sum()

print("\n--- Refund Analysis ---")
print("Total Refunds:", total_refunds)
print("Affected Orders:", affected_orders)
print("Total Refund Amount:", round(total_refund_amount, 2))

# =========================
# STEP 18: RETURN / REFUND RATE
# =========================

total_orders = len(orders)

returned_orders = (
    orders["order_status"] == "Returned"
).sum()

return_rate = (
    returned_orders / total_orders
) * 100

print("\n--- Return / Refund Rate ---")
print("Total Orders:", total_orders)
print("Returned Orders:", returned_orders)
print("Return Rate:", round(return_rate, 2), "%")

# =========================
# STEP 19: RETURN RATE BY CATEGORY
# =========================

category_orders = (
    completed_items
    .merge(
        orders[["order_id", "order_status"]],
        on="order_id"
    )
    .merge(
        products[["product_id", "category"]],
        on="product_id"
    )
)

category_return_rate = (
    category_orders
    .groupby("category")
    .agg(
        total_orders=("order_id", "nunique"),
        returned_orders=(
            "order_id",
            lambda x: x[
                category_orders.loc[
                    x.index, "order_status"
                ] == "Returned"
            ].nunique()
        )
    )
)

category_return_rate["return_rate_percentage"] = (
    category_return_rate["returned_orders"]
    / category_return_rate["total_orders"]
    * 100
)

category_return_rate["return_rate_percentage"] = (
    category_return_rate["return_rate_percentage"].round(2)
)

category_return_rate = category_return_rate.sort_values(
    "return_rate_percentage",
    ascending=False
)

print("\n--- Return Rate by Category ---")
print(category_return_rate)

# =========================
# STEP 19: CORRELATION ANALYSIS
# =========================

print("\n--- Order Items Correlation ---")

correlation = order_items[
    ["quantity", "unit_price", "discount"]
].corr()

print(correlation.round(2))

# =========================
# STEP 20: CORRELATION HEATMAP
# =========================

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 5))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap - Order Items")
plt.tight_layout()
plt.show()

# =========================
# STEP 21: REVENUE DISTRIBUTION
# =========================

plt.figure(figsize=(8, 5))

plt.hist(
    completed_items["revenue"],
    bins=30
)

plt.title("Revenue Distribution")
plt.xlabel("Revenue")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

# =========================
# STEP 22: OUTLIER DETECTION
# =========================

Q1 = completed_items["revenue"].quantile(0.25)
Q3 = completed_items["revenue"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = completed_items[
    (completed_items["revenue"] < lower_limit) |
    (completed_items["revenue"] > upper_limit)
]

print("\n--- Outlier Detection ---")
print("Q1:", round(Q1, 2))
print("Q3:", round(Q3, 2))
print("IQR:", round(IQR, 2))
print("Lower Limit:", round(lower_limit, 2))
print("Upper Limit:", round(upper_limit, 2))
print("Number of Outliers:", len(outliers))

# =========================
# STEP 23: KEY EDA VISUALIZATIONS
# =========================

# 1. Revenue by Category
category_revenue.sort_values().plot(
    kind="barh",
    figsize=(8, 5),
    title="Revenue by Category"
)

plt.xlabel("Revenue")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# 2. Monthly Revenue Trend
monthly_revenue.plot(
    figsize=(10, 5),
    title="Monthly Revenue Trend"
)

plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# 3. Top 10 Products by Revenue
product_revenue.sort_values().plot(
    kind="barh",
    figsize=(8, 6),
    title="Top 10 Products by Revenue"
)

plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.show()