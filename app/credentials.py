import os

USERNAME = os.getenv('CREDENTIALS_USERNAME')
PASSWORD = os.getenv('CREDENTIALS_PASSWORD')

if USERNAME and PASSWORD:
    print(f'Found username and passwords in .env file.')

def verify_credentials(user, pwd):
    return user == USERNAME and pwd == PASSWORD