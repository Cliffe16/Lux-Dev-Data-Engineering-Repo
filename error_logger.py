import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError, OperationalError 
import logging
from datetime import datetime
import os


engine = create_engine('postgresql://cliffe:BLOOMberg411**@localhost/bike_store')

#Setup file
log_file = 'error_logs.txt'

#Configure logging to write to a file
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_errors():    
    #faulty query for testing
    query = """
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
        ORDER BY total_revenue DESC;
    """
    
    try:
        print("Connecting...")
        result = pd.read_sql(query, con=engine)
        print(f"Query ran successfully. {len(result)} rows found")
        
    except ProgrammingError as e:
        error_msg = f"SQL Programming Error in query: Check syntax/schema. Details: {e.__cause__}"
        
        logging.error(error_msg)
        print(f"Handled SQL Error. Check {log_file} for details.")
        
    except OperationalError as e:
        error_msg = f"Database Connection Error: Check server status or credentials. Details: {e.__cause__}"
        
        logging.critical(error_msg)
        print(f"Handled Connection Error. Check {log_file} for details.")
        
    except Exception as e:
        error_msg = f"Unexpected Python Error: {e}"
        logging.critical(error_msg)
        print(f"Handled Unexpected Error. Check {log_file} for details.")
        
if __name__ == '__main__':
    log_errors()   

