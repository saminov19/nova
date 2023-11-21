import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.http import MediaFileUpload
from django.http import HttpResponse

def create_google_doc(request):
    if request.method == 'POST':
        data = request.POST['data']
        name = request.POST['name']

        # get credentials
        credentials_path = 'credentials.json'
        token_path = 'token.json'
        creds = None

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    'https://www.googleapis.com/auth/drive')
                creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        # create new document
        doc_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.document'
        }

        new_doc = service.files().create(body=doc_metadata).execute()
        doc_id = new_doc['id']

        # add text to our document
        media_body = MediaFileUpload(data, mimetype='text/plain', resumable=True)
        request_body = {'description': 'Created by API'}
        request = service.files().update(
            fileId=doc_id,
            body=request_body,
            media_body=media_body,
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'Uploaded {int(status.progress() * 100)}%')

        return HttpResponse('Google Doc created successfully')
    else:
        return HttpResponse('Method not allowed')
