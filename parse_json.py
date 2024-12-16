import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template

# File data is from https://www.estately.com/IN/North_Willow_Farms,_Indianapolis/sold
FILE_PATH = "response.json"

# Read JSON data from the file
with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract properties
properties = data.get("properties", [])

# Parse and print property details
for prop in properties:
    unit = prop.get("unit", {})
    address = prop.get("address", "N/A")
    beds = unit.get("bedrooms", "N/A")
    baths = unit.get("bathrooms", "N/A")
    sqft = unit.get("sqf", "N/A")
    lot_size = unit.get("lot_sqft", "N/A")
    price = unit.get("price", "N/A")
    sold_date = unit.get("sale_date", "N/A")

    print(f"Address: {address}")
    print(f"Beds: {beds}")
    print(f"Baths: {baths}")
    print(f"Square Footage: {sqft}")
    print(f"Lot Size: {lot_size} sqft")
    print(f"Price When Sold: ${price}")
    print(f"Date Sold: {sold_date}")
    print("-" * 50)

print("Total properties:", len(properties))

# Prepare data for analysis
df = pd.DataFrame([
    {
        "Address": property["address"],
        "Beds": property["unit"].get("bedrooms", None),
        "Baths": property["unit"].get("bathrooms", None),
        "Sqft": int(property["unit"].get("sqf", "0").replace(",", "")) if "sqf" in property["unit"] else None,
        "Lot Size": property["unit"].get("lot_sqft", None),
        "Price": property["unit"].get("price", None),
        "Date Sold": pd.to_datetime(property["unit"].get("sale_date", None)),
    }
    for property in properties if "unit" in property
])

# Create an output directory for images
output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)

# Visualization 1: Price Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["Price"], kde=True, bins=20)
plt.title("Price Distribution")
plt.xlabel("Price ($)")
plt.ylabel("Number of Properties")
plt.savefig(f"{output_dir}/price_distribution.png")
plt.close()

# Price Distribution since 2020
df_sold_since_2020 = df[df["Date Sold"] >= "2020-01-01"]
plt.figure(figsize=(10, 6))
sns.histplot(df_sold_since_2020["Price"], kde=True, bins=20)
plt.title("Price Distribution")
plt.xlabel("Price ($)")
plt.ylabel("Number of Properties")
plt.savefig(f"{output_dir}/price_distribution_2020.png")
plt.close()

# Visualization 2: Beds vs Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Beds", y="Price")
plt.title("Number of Beds vs Price")
plt.xlabel("Number of Beds")
plt.ylabel("Price ($)")
plt.savefig(f"{output_dir}/beds_vs_price.png")
plt.close()

# Visualization 3: Sqft vs Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Sqft", y="Price")
plt.title("Square Footage vs Price")
plt.xlabel("Square Footage")
plt.ylabel("Price ($)")
plt.savefig(f"{output_dir}/sqft_vs_price.png")
plt.close()

# Visualization 4: Lot Size Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["Lot Size"], kde=True, bins=20)
plt.title("Lot Size Distribution")
plt.xlabel("Lot Size (sqft)")
plt.ylabel("Number of Properties")
plt.savefig(f"{output_dir}/lot_size_distribution.png")
plt.close()

# Visualization 5: Sale Trends Over Time
plt.figure(figsize=(10, 6))
df_sorted = df.sort_values("Date Sold")
sns.lineplot(data=df_sorted, x="Date Sold", y="Price")
plt.title("Sale Price Trends Over Time")
plt.xlabel("Date Sold")
plt.ylabel("Price ($)")
plt.savefig(f"{output_dir}/sale_trends.png")
plt.close()

# Visualization 6: Correlation Matrix
plt.figure(figsize=(10, 6))
corr = df[["Beds", "Baths", "Sqft", "Lot Size", "Price"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig(f"{output_dir}/correlation_matrix.png")
plt.close()

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Property Data Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        img { max-width: 100%; height: auto; }
        .visualization { margin-bottom: 50px; }
    </style>
</head>
<body>
    <h1>Property Data Analysis</h1>
    <div class="visualization">
        <h2>1. Price Distribution since June 2008</h2>
        <img src="price_distribution.png" alt="Price Distribution">
    </div>
    <div class="visualization">
        <h2>2. Price Distribution since January 2020</h2>
        <img src="price_distribution_2020.png" alt="Price Distribution">
    </div>
    <div class="visualization">
        <h2>3. Number of Beds vs Price</h2>
        <img src="beds_vs_price.png" alt="Number of Beds vs Price">
    </div>
    <div class="visualization">
        <h2>4. Square Footage vs Price</h2>
        <img src="sqft_vs_price.png" alt="Square Footage vs Price">
    </div>
    <div class="visualization">
        <h2>5. Lot Size Distribution</h2>
        <img src="lot_size_distribution.png" alt="Lot Size Distribution">
    </div>
    <div class="visualization">
        <h2>6. Sale Price Trends Over Time</h2>
        <img src="sale_trends.png" alt="Sale Price Trends Over Time">
    </div>
    <div class="visualization">
        <h2>7. Correlation Matrix</h2>
        <img src="correlation_matrix.png" alt="Correlation Matrix">
    </div>
</body>
</html>
"""

# Save the HTML file
html_path = os.path.join(output_dir, "analysis.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Visualizations saved to {output_dir}")
print(f"Open {html_path} in your browser to view the analysis.")
