import pandas as pd
import settings as s

def fill_database(data_objects):
    for table_name, data_object in data_objects.items():
        data_object.to_sql(
            table_name,
            s.connection,
            if_exists='replace'
        )
