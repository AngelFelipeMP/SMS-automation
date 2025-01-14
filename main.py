from __future__ import print_function
import clicksend_client
from clicksend_client import Contact, ContactList, ContactListApi, ContactApi, SmsCampaignApi, SmsCampaign
from clicksend_client.rest import ApiException
from icecream import ic
import os
from dotenv import load_dotenv
import ast
import json

# Load environment variables from .env file
load_dotenv()

# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = os.environ.get('USERNAME')
configuration.password = os.environ.get('PASSWORD')

# Create an instance of the ContactListApi API class
contact_list_api = ContactListApi(clicksend_client.ApiClient(configuration))

# Create a new contact list
new_contact_list = ContactList(list_name='My Contact List TEST')

# Send the list throught the contact Api response
contact_list_response = contact_list_api.lists_post(new_contact_list)

# Get contact list ID
contact_list_response_dictionary = ast.literal_eval(contact_list_response)
contact_list_id = contact_list_response_dictionary['data']['list_id']

# Create a python list of contacts
contacts = [
    Contact(first_name='Angel', last_name='Magnossao', phone_number='+61431386743', custom_1='custom_value_1')
]

# Add contacts to the contact list
for contact in contacts:
    contact_list_api.lists_by_list_id_put(contact_list_id, contact)


# Create an instance of the SmsCampaignApi API class
sms_campaign_api = SmsCampaignApi(clicksend_client.ApiClient(configuration))


# Create an SMS campaign
sms_campaign = SmsCampaign(
    name='My SMS Campaign',
    list_id=contact_list_id,
    _from = '+61447056520',
    schedule = 0,
    body='Hello, this is a test message!'
)

# Send the SMS campaign
api_response = sms_campaign_api.sms_campaigns_send_post(sms_campaign)
ic(api_response)


    
# if __name__ == '__main__':