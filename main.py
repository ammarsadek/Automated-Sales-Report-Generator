import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Load & Combine CSV Files
files = glob.glob("data/*.csv")
df_list = [pd.read_csv(f) for f in files]
df = pd.concat(df_list, ignore_index=True)


# Clean the dataset
df.columns = df.columns.str.strip().str.lower()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.drop_duplicates()
df = df.dropna(subset=["date", "quantity"])

# Save Cleaned dataset
df.to_csv("Clean_sales.csv", index=False)

# Build Summary
summary = df.groupby(df["date"].dt.month)["quantity"].sum()
summary.to_csv("sales_summary.csv")

# Generate Charts
plt.figure(figsize=(10,5))
summary.plot(kind="line")
plt.title("Monthly Sales Overview")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid(True)
plt.savefig("sales_chart.png")
plt.close()

product_summary = df.groupby("product")["quantity"].sum()

plt.figure(figsize=(8,5))
product_summary.plot(kind="bar")
plt.title("Sales by Product")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("sales_by_product.png")
plt.close()

print("Sales report generated successfully!")