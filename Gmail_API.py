from __future__ import print_function

import re
import base64
import os.path
import email

import requests
from email.parser import BytesParser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/5nip3r/Downloads/jitender-Desktop.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        def execute_api_call(message):

            # Get the raw message data
            raw_message = message['raw']

            # Decode the raw message data
            decoded_message = base64.urlsafe_b64decode(raw_message.encode())

            # Parse the message using the email library
            parsed_message = email.message_from_bytes(decoded_message)
            print(parsed_message)

            # Get the subject of the message
            subject = parsed_message['Subject']
            replaced_subject = subject.replace("=?UTF-8?B?4oCT?=", "-")

            print(type(replaced_subject))

            print("Subject :"+replaced_subject)

            # execute the API call using the message data
            myList = ['Database', 'Throughput', 'Improving']

            str = replaced_subject
            # print(replaced_subject)

            if replaced_subject.startswith('Redis Email Alert') & replaced_subject.endswith('of your memory limit'):
                print("Here")
                print("The string contains 'world'.")
                api_response = requests.post('https://example.com/api/send_message', data={'subject': subject, 'body': "{}"})
                print(api_response)
            else:
                print("not here")

        result = service.users().watch(userId='me', body={
            'topicName': 'projects/central-beach-194106/topics/jitender-scaleup-automation',
            'labelIds': ['Label_4749487990734074908'],
            'labelFilterAction': 'include'
        }).execute()
        # print("Results Are: ")
        # print(result)
        print("New Results Are: ")
        # email_message1 = service.users().messages().get(userId='me', id=attributes[result.get(historyId)]).execute()
        response = service.users().messages().list(userId='me',labelIds=['Label_4749487990734074908']).execute()

        print(response)

        # labels = service.users().labels().list(userId='me').execute()
        # for label in labels['labels']:
        #     print(label)

        # get the list of messages in the user's INBOX
        messages = service.users().messages().list(userId='me', labelIds=['Label_4749487990734074908']).execute()

        # get the first message in the list
        message = messages['messages'][1] #TO DO - Need to change it to 0
        # print(message)

        message_from_id = service.users().messages().get(userId='me', id=message.get('id'), format='raw').execute()

        # execute the API call function
        execute_api_call(message_from_id)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        # print(f'An error occurred: {error}')
        pass


if __name__ == '__main__':
    main()
