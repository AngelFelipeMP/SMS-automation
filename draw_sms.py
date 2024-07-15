from __future__ import print_function
import clicksend_client
from clicksend_client import Contact, ContactList, ContactListApi, ContactApi, SmsCampaignApi, SmsCampaign
from clicksend_client.rest import ApiException
from icecream import ic
import os
from dotenv import load_dotenv
import ast
import pandas as pd
from datetime import datetime


class ClickSendSMS:
    def __init__(self, username, password, data_folder_path, participants_file,  winners_file):
        self.username = username
        self.password = password
        self.data_folder_path = data_folder_path
        self.participants_file = participants_file
        self.winners_file =  winners_file
    
    
    def authorization(self):
        try:
            # Configure HTTP basic authorization: BasicAuth
            self.configuration = clicksend_client.Configuration()
            self.configuration.username = self.username
            self.configuration.password = self.password
            print(f"Authorization successful.")
        except:
            print("Authorization failed.")
        
    
    def load_data(self):
        try:
            self.df_drow_participants = pd.read_csv(f'{self.data_folder_path}/{self.participants_file}.csv')
            self.df_drow_winners = pd.read_csv(f'{self.data_folder_path}/{self.participants_file}.csv')
            print(f"Data loaded successfully.")
        except:
            print("Failed to load data.")
            
    
    def build_sms_text(self):
        try:
            trail_type = self.participants_file.split('_')[1].split('.')[0]
            info_sms = self.df_drow_winners.loc[self.df_drow_winners['Trial'].str.contains(trail_type), ['Q4.6','Q4.7', 'Trial']].to_dict()
            self.text_sms = f"Hi from DrivePoints! This week's winner is a driver from {int(info_sms['Q4.7'][0])}. Enable location access on the app for your chance to win next week."
            print(f"SMS text successfully built.")
        except:
            print("Failed to build SMS text.")
        
        
    def create_contact_list(self):
        try:
            # Create an instance of the ContactListApi API class
            self.contact_list_api = ContactListApi(clicksend_client.ApiClient(self.configuration))

            # Create a new contact list
            self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_contact_list = ContactList(list_name=f'Contact list {self.current_time}')

            # Send the list throught the contact Api response
            self.contact_list_response = self.contact_list_api.lists_post(new_contact_list)
            print("Contact list created successfully.")
        except:
            print("Failed to create contact list.")

        
        
    def get_id_contact_list(self):
        # Get contact list ID
        contact_list_response_dictionary = ast.literal_eval(self.contact_list_response)
        self.contact_list_id = contact_list_response_dictionary['data']['list_id']


    def add_participants_to_contact_list(self):
        try:
            #contact API instance
            contact_api = ContactApi(clicksend_client.ApiClient(self.configuration))
            
            for index, row in self.df_drow_participants.iterrows():
                contact = Contact(phone_number=row['Mobile Number Int'], custom_1=row['Trial'])
                response = contact_api.lists_contacts_by_list_id_post(contact, self.contact_list_id)
            
            print(f"{len(self.df_drow_participants)} participants added to contact list successfully.")
        except:
            print("Failed to add participants to contact list.")
            
            
    def create_sms_campaign(self):
        try:
            # Now you can use the contact list to send SMS messages
            self.sms_campaign_api = SmsCampaignApi(clicksend_client.ApiClient(self.configuration))

            # Create an SMS campaign
            self.sms_campaign = SmsCampaign(
                name='Weekly Draw ' + self.current_time,
                list_id=self.contact_list_id,
                _from='SafeDrive',
                schedule=0,
                body=self.text_sms)
        except:
            print("Failed to create SMS campaign.")
        
        
    def send_sms_campaign(self):
        try:
            api_response = self.sms_campaign_api.sms_campaigns_send_post(self.sms_campaign)
            print("SMS campaign sent successfully.")
        except:
            print("Failed to send SMS campaign.")
    
    
    def main(self):
        self.authorization()
        self.load_data()
        self.build_sms_text()
        self.create_contact_list()
        self.get_id_contact_list()
        self.add_participants_to_contact_list()
        self.create_sms_campaign()
        self.send_sms_campaign()
    
    
if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    
    try:
        
        # for file_name in ['participants_feedback', 'participants_smart']: # TODO: uncomment line with actual file names
        for file_name in ['participants_test']: #TODO: delete line with test file name
            # Create an instance of the ClickSendSMS class
            clicksend_sms = ClickSendSMS(username = os.environ.get('USERNAME'), #TODO: replace with actual username and password
                                            password = os.environ.get('PASSWORD'),#TODO: replace with actual username and password
                                            data_folder_path= os.getcwd() + '/data', #TODO: replace with actual data folder path
                                            participants_file=file_name,
                                            winners_file='selected_participants')
            
            clicksend_sms.main()

    except ApiException as e:
        print(f"Exception when calling API: {e}")
    except Exception as e:
        print(f"General exception: {e}")