# google-drive-backup
a python program for backing up a selected folder on a windows machine into Google Drive

## requirements

- Use `pip install pywin32 google-api-python-client google-auth-httplib2 google-auth-oauthlib` to install dependencies.

## use

- add a `dir_path` value to the config.ini file equal to the full path of the folder you would like to backup
- In the [Google Developers Console](https://console.developers.google.com) open **API & SERVICES** -> **Dashboard** and click **CREATE PROJECT**.
- once your project is created, open **Oauth consent screen** and configure your applications consent screen.
- you will need to create a **client_secrets.json** file from Google, by clicking **CREATE CREDENTIALS** and then choosing **OAuth Client ID**.
- choose web appication for your application type, and then add `http://localhost:8080` to **Authorized JavaScript Origins** and `https://localhost:8080/` to **Authorized redirect URIs**
- run **main.py** using `python3 main.py`
- upon first run you will need to sign into your Google account, but after that the sign in token is refreshed if it expires so you should not need to sign in again.
