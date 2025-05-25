import pandas as pd

def read_and_clean(include_returns=False):

    orders_df = pd.read_csv('SuperStoreUS-2015_Orders.csv', encoding='latin1', on_bad_lines='skip', sep=';')

    # Convert numeric strings with commas to floats
    cols_to_float = ['Discount', 'Unit Price', 'Shipping Cost', 'Product Base Margin', 'Profit', 'Sales']
    for col in cols_to_float:
        orders_df[col] = orders_df[col].str.replace(',', '.', regex=False)
        orders_df[col] = pd.to_numeric(orders_df[col], errors='coerce')

    # Convert date columns to datetime
    orders_df['Order Date'] = pd.to_datetime(orders_df['Order Date'], format='%d.%m.%Y', errors='coerce')
    orders_df['Ship Date'] = pd.to_datetime(orders_df['Ship Date'], format='%d.%m.%Y', errors='coerce')

    # Work with orders only by default
    df = orders_df.copy()

    # Optional: merge with returns if requested
    if include_returns:
        returns_df = pd.read_csv('SuperStoreUS-2015(Returns).csv', encoding='latin1', on_bad_lines='skip', sep=';')
        df = df.merge(returns_df, on='Order ID', how='left')

    # Drop rows missing essential numeric or time information
    df = df.dropna()

    # Create year and month columns
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month

    return df