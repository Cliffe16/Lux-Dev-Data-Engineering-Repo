import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://cliffe:BLOOMberg411**@localhost/bike_store')

query = f"""
    SELECT
        b.brand_name,
        SUM(i.quantity * i.list_price * (1.0 - i.discount)) AS total_revenue
    FROM orders o
        JOIN order_items i 
            ON o.order_id = i.order_id
                JOIN products p 
                    ON i.product_id = p.product_id
                        JOIN brands b 
                            ON p.brand_id = b.brand_id
    GROUP BY b.brand_name
    ORDER BY total_revenue DESC;
    """
    
#App Layout
st.set_page_config(layout="wide")

@st.cache_data
def get_revenue_data():
    """Fetches data from the database and caches the result."""
    df = pd.read_sql(query, con=engine)
    
    # Format the revenue column for better display in the app
    pd.options.display.float_format = '{:,.2f}'.format
    df['total_revenue'] = df['total_revenue'].apply(lambda x: f"${x:,.2f}")
    
    return df

st.title("Bike Store Revenue Dashboard")
st.markdown("---")

df_revenue = get_revenue_data()

# 1. Display the aggregated data table
st.header("Revenue Breakdown by Brand")
st.dataframe(df_revenue, use_container_width=True)

# 2. Display the visualization
st.subheader("Revenue Distribution Chart")

# Let's re-read the data without the string format for charting consistency
df_chart = pd.read_sql(query, con=engine) 

st.bar_chart(df_chart, x='brand_name', y='total_revenue')    