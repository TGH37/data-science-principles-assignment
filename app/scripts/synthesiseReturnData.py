import pandas as pd
import numpy as np
from scipy.stats import skewnorm

# Load the returns data from Returns.csv
returns_data = pd.read_csv('app/raw-data/csvOutputs/Returns.csv')
print(f"Returns data: {returns_data.shape}")


# Load the orders data from Orders.csv
orders_data = pd.read_csv('app/raw-data/csvOutputs/Orders.csv')
print(f"Orders data: {orders_data.shape}")
order_ids_returns = orders_data['Order ID'].nunique()
print(f"Number of unique Order IDs: {order_ids_returns}")

orders_data['Order ID Processed'] = orders_data['Order ID'].str.split('-', n=2).str[2]

returns_data['Order ID Processed'] = returns_data['Order ID'].str.split('-', n=2).str[2]

common_values = returns_data['Order ID Processed'].isin(orders_data['Order ID Processed'])

# Create a dictionary mapping 'processed_order_id' to 'order_id' from orders_data
order_id_map = orders_data.set_index('Order ID Processed')['Order ID'].to_dict()

# Create a new column 'Matched_OrderID' in returns_data and populate it based on the mapping
returns_data['Matched_OrderID'] = returns_data['Order ID Processed'].map(order_id_map)

order_date_map = orders_data.set_index('Order ID')['Order Date'].to_dict()

returns_data = returns_data.dropna(subset=['Matched_OrderID'])

returns_data = returns_data.drop(['Order ID', 'Order ID Processed'], axis=1)
returns_data['Order ID'] = returns_data['Matched_OrderID']
returns_data = returns_data.drop(['Matched_OrderID'], axis=1)
returns_data['Return Date'] = returns_data['Order ID'].map(order_date_map)

print(returns_data)

# return_date_map = returns_data.set_index('Order ID')['Return Date'].to_dict()

# print(return_date_map)

# Create a new dictionary without duplicate keys
new_dict = {key: value for key, value in returns_data.drop_duplicates(subset='Order ID', keep='last').set_index('Order ID')['Return Date'].items()}
print(new_dict)

# Set the parameters for the skewed normal distribution
mean_days = 8
max_days = 30
skewness = -2  # Negative value for left skewness

for key in new_dict:
    # Generate a random number of days from the skewed normal distribution
    additional_days = int(skewnorm.rvs(a=skewness, loc=mean_days, scale=5))
    
    # Ensure the additional days are within the range of 0 to max_days
    additional_days = max(0, min(additional_days, max_days))
    
    # Add the additional days to the original date
    new_dict[key] = pd.to_datetime(new_dict[key]) + pd.Timedelta(days=additional_days)

print(new_dict)


returns_data['Return Date'] = returns_data['Order ID'].map(new_dict).fillna(returns_data['Return Date'])

order_ids_returns = returns_data['Order ID'].nunique()

# Save the resulting data into a new csv file named 'synthesised_returns.csv'
returns_data.to_csv('app/synthesised_returns.csv', index=False)