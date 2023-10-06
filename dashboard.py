import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load your dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_data = pd.read_csv("all_data.csv")
all_data[datetime_cols] = all_data[datetime_cols].apply(pd.to_datetime)
all_data.sort_values(by="order_approved_at", inplace=True)
all_data.reset_index(inplace=True)

# Page 1: Name and Email
st.title("Name: Armand Faris A Surbakti")
st.title("Gmail: actuallyarmand@gmail.com")

# Page 2: Most and Least Sold Product
st.title("Most and Least Sold Product")

sum_order_items_df = all_data.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
sum_order_items_df = sum_order_items_df.head(10)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#E17DAB", "#0097DF", "#0097DF", "#0097DF", "#0097DF"]

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most Sold Products", loc="center", fontsize=20)
ax[0].tick_params(axis='y', labelsize=15)

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least Sold Products", loc="center", fontsize=20)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Most and Least Sold Products", fontsize=20)

st.pyplot(fig)

# Page 3: Monthly Customer Expenditure in a 12-month span
st.title("Monthly Customer Expenditure in a 12-month span")

monthly_spend_df = all_data.resample(rule='M', on='order_approved_at').agg({
    "payment_value": "sum"
})
monthly_spend_df.index = monthly_spend_df.index.strftime('%B')
monthly_spend_df = monthly_spend_df.reset_index()
monthly_spend_df.rename(columns={"payment_value": "total_spend"}, inplace=True)
monthly_spend_df = monthly_spend_df.sort_values('total_spend').drop_duplicates('order_approved_at', keep='last')

plt.figure(figsize=(10, 5))
plt.plot(monthly_spend_df["order_approved_at"], monthly_spend_df["total_spend"], marker='o', linewidth=2, color="#068DA9")
plt.title("Total Customer Spend per Month (2018)", loc="center", fontsize=20)
plt.xticks(fontsize=10, rotation=25)
plt.yticks(fontsize=10)

st.pyplot()
