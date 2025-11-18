import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os

# Use the established connection engine
engine = create_engine('postgresql://cliffe:BLOOMberg411**@localhost/bike_store')

def generate_daily_report():
    report_dir = 'sql+python test/daily_reports'
    
    #Ensure reports directory exists
    os.makedirs(report_dir, exist_ok=True)
    
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
    
    result = pd.read_sql(query, con=engine)
    
    #Format date and file name
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    filename = os.path.join(report_dir, f"revenue_by_brand_{timestamp}.csv")
    
    #Save report in csv
    result.to_csv(filename, index=False)
    
    print("Daily report successfully saved in csv")
    
if __name__ == '__main__':
    generate_daily_report()    
    