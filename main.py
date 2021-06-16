import pandas as pd
import sib_api_v3_sdk as sib


from utils import (
    set_database_connection,
    config_api,
    convert_data_object_to_sql
)

api_client = config_api()
api_instance = sib.EmailCampaignsApi(api_client)
email_campaigns = api_instance.get_email_campaigns().campaigns

set_database_connection()
convert_data_object_to_sql('email_campaigns', email_campaigns)
