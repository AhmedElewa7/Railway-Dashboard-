# Import necessary libraries
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Load the dataset
df = pd.read_csv("railway.csv")
df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"])
df["Date of Journey"] = pd.to_datetime(df["Date of Journey"])

# Sidebar
st.sidebar.title("Railway revenue Dashboard")
st.sidebar.image("images.jpg")

st.sidebar.write("This dashboard analyze revenue from different ticket types & classes and payment methods.")


# Sidebar Filters
st.sidebar.header("Filters")

# Filter by Ticket Class
classes = st.sidebar.multiselect("Select Ticket Class", options=df["Ticket Class"].unique(), default=df["Ticket Class"].unique())
df = df[df["Ticket Class"].isin(classes)]


# Filter by Ticket Type
types = st.sidebar.multiselect("Select Ticket Type", options=df["Ticket Type"].unique(), default=df["Ticket Type"].unique())
df = df[df["Ticket Type"].isin(types)]


st.sidebar.markdown("---")
st.sidebar.write("Made by Ahmed Elewa 😎 [Linkedin](https://www.linkedin.com/in/ahmed-elewa-b4a0491b7?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BiywfpnqtQlixfWoaDOcr%2FA%3D%3D)" )
st.sidebar.write("GitHub: AhmedElewa7")
st.sidebar.write("Email: ahmedelewa300@gmail.com")


# Body

# Row 1

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"{df['Price'].sum():,.0f}")
col2.metric("Average Total revenue", f"{df['Price'].mean().round(2)}")
col3.metric("Number of Transactions", f"{len(df):,}")

# Row 2

st.subheader("Revenue Over Time by Ticket Class")
daily_class_sales = df.groupby(["Date of Purchase", "Ticket Class"])["Price"].sum().reset_index()
fig = px.area(daily_class_sales, x="Date of Purchase", y="Price", color="Ticket Class")
st.plotly_chart(fig)


c1,c3 = st.columns(2)


c1.subheader("Revenue by Payment Method")
payment_data = df.groupby("Payment Method")["Price"].sum().reset_index()
fig = px.pie(payment_data, names="Payment Method", values="Price", hole=0.4)
c1.plotly_chart(fig)

c3.subheader("Ticket Price Distribution by Class")
fig, ax = plt.subplots()
sns.boxplot(x="Ticket Class", y="Price", data=df, ax=ax)
ax.set_title("Price Distribution by Ticket Class")
c3.pyplot(fig)



# Row 3

c2,c4 = st.columns(2)


c2.subheader("Avg Price by Payment Method and Ticket Type")
pivot_table = df.pivot_table(index="Payment Method", columns="Ticket Type", values="Price", aggfunc="mean")
fig, ax = plt.subplots(figsize=(8,5))
sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
ax.set_title("Average Ticket Price by Payment Method and Type")
c2.pyplot(fig)

c4.subheader("Revenue by Purchase Type")
revenue_purchase = df.groupby("Purchase Type")["Price"].sum()
fig, ax = plt.subplots()
revenue_purchase.plot(kind="bar", ax=ax)
ax.set_ylabel("Revenue")
ax.set_title("Revenue by Purchase Channel")
c4.pyplot(fig)


# Row 5
st.subheader("Top 10 Departure Stations by Revenue")
top_stations = df.groupby("Departure Station")["Price"].sum().nlargest(10)
fig, ax = plt.subplots()
top_stations.plot(kind="barh", ax=ax)
ax.set_xlabel("Revenue")
ax.set_ylabel("Station")
ax.set_title("Top 10 Stations by Sales")
plt.gca().invert_yaxis()
st.pyplot(fig)

