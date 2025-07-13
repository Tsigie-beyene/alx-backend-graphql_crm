from celery import shared_task
from crm.schema import schema
from datetime import datetime

@shared_task
def generate_crm_report():
    query = """
        query {
            report {
                totalCustomers
                totalOrders
                totalRevenue
            }
        }
    """
    result = schema.execute(query)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("/tmp/crmreportlog.txt", "a") as log_file:
        if result.errors:
            log_file.write(f"{timestamp} - Error: {result.errors}\n")
        else:
            data = result.data["report"]
            log_file.write(
                f"{timestamp} - Report: {data['totalCustomers']} customers, "
                f"{data['totalOrders']} orders, {data['totalRevenue']} revenue\n"
            )
