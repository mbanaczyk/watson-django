import sys
import os
import json
from watson_developer_cloud import DiscoveryV1
#sudo pip install watson-developer-cloud
# from .models import Environment, Collection

import httplib2

from apiclient.discovery import build
#sudo pip install --upgrade google-api-python-client
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow


WATSON_UN = "dba214e1-bf76-46b7-8d6e-8c5c1aa6b24c"
WATSON_PW = "e5xMPekLUhaN"
#WATSON_ENV = "7d2097c0-c1b8-43e7-9311-c555f72d1c4a"
#WATSON_COLLECT = ["775d2098-9b2d-4e67-9d95-324e85592815",]
#query = "What measures should be taken to reduce risk of fire in oxygen compressors?"

def query_environ(query_text,environ_id_string, collect_ids):
    discovery = DiscoveryV1(
        username=WATSON_UN,
        password=WATSON_PW,
        version="2016-12-01"
    )
    results = []
    for collection in collect_ids:
        qopts = {'query': query_text, 'return': 'id,score,text,html,extracted_metadata.filename'}
        my_query = discovery.query(environ_id_string, collection, qopts)
        sub_results = my_query.get("results", [])
        
        #iterate through each result
        for sub_result in sub_results:
            
            #add collection field
            sub_result['collection'] = collection
            
            #trim text to a preview
            json_field_text = sub_result.get("text")
            json_field_text = json_field_text[:249] + '...'
            sub_result['text'] = json_field_text
            
            #get filename
            json_field_filename = sub_result['extracted_metadata'].get['filename']
            json_field_filename = json_field_filename.rsplit('.', 1)
            
            #lookup contact in address book
            

            results.append(json.dumps(sub_result))
    return results
    
def get_contacts():
    SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
    CLIENT_SECRET_FILE = 'environment/credentials/client_secret.json'
    APPLICATION_NAME = 'People API Python Quickstart'

#    try:
#        import argparse
#        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#    except ImportError:
#        flags = None

    flags = tools.argparser.parse_args(args=['--noauth_local_webserver'])    
    # Set up a Flow object to be used if we need to authenticate. This
    # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
    # the information it needs to authenticate. Note that it is called
    # the Web Server Flow, but it can also handle the flow for
    # installed applications.
    #
    # Go to the Google API Console, open your application's
    # credentials page, and copy the client ID and client secret.
    # Then paste them into the following code.
    
    FLOW = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    FLOW.user_agent = APPLICATION_NAME
    
    # If the Credentials don't exist or are invalid, run through the
    # installed application flow. The Storage object will ensure that,
    # if successful, the good Credentials will get written back to a
    # file.
    storage = Storage('info.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
      credentials = tools.run_flow(FLOW, storage, flags)
    
    # Create an httplib2.Http object to handle our HTTP requests and
    # authorize it with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Build a service object for interacting with the API. To get an API key for
    # your application, visit the Google API Console
    # and look at your application's credentials page.
    people_service = build(serviceName='people', version='v1', http=http)
    
    # get a list of people in the user's contacts
    service_result = people_service.people().connections().list(resourceName='people/me', requestMask_includeField = 'person.names,person.emailAddresses,person.phoneNumbers').execute()
    
    connections = service_result.get('connections', [])

    return connections

