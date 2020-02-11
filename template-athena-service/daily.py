import json
import boto3
import logging
from datetime import date, timedelta

athena_client = boto3.client('athena')

# triggered at 5am every morning
def handle(event, context):
    # extract these from event
    storeName = 'store_name_1'  
    today = ( date.today() - timedelta(days=1) ).strftime('%Y-%m-%d')

    baseOutputLocation = f's3://jolt.capstone/athena-query-logs/{storeName}'

    response = uniquePerHour(today, baseOutputLocation)
    print(response)
    return response


def uniquePerHour(today, baseInputLocation):
    # WHERE clause is hard-coded with the only day we have data for
    athenaQuery = (
        "SELECT date_trunc('hour', first_seen) time, Count(*) visits "
		"FROM store_name_1 "
        f"WHERE DATE(first_seen)=DATE('2019-12-12') "
		"GROUP BY date_trunc('hour', first_seen) "
		"ORDER BY date_trunc('hour', first_seen)"
        )
    
    outputLocation = f'{baseInputLocation}/unique_per_hour/{today}'

    response = athena_client.start_query_execution(
        QueryString = athenaQuery,
        QueryExecutionContext = { 'Database': 'capstone' },
        ResultConfiguration = { 'OutputLocation': outputLocation }
    )
    return response 