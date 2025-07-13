from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    """
    Cron job to run every 12 hours.
    Executes GraphQL mutation to restock products with stock < 10.
    Logs result to /tmp/low_stock_updates_log.txt
    """

    # Define the GraphQL mutation
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    # Set up transport to the GraphQL endpoint
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql/',  # Make sure this matches your live server
        verify=False,  # For development; set to True in production
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Prepare log timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Execute the mutation
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]
        message = result["updateLowStockProducts"]["message"]

        # Log the result
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"[{timestamp}] Success: {message}\n")
            for product in updated_products:
                log_file.write(
                    f"[{timestamp}] Updated {product['name']} to stock {product['stock']}\n"
                )

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"[{timestamp}] ERROR: {str(e)}\n")
