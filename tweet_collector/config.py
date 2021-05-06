import os

'''
The 4 required authentication tokens:
       1. API_KEY
       2. API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET
Are imported from the OS environment. 
The values have been saved in .bashrc
To access the values docker-compose needs to be invoked with sudo -E 
sudo -E docker-compose build
sudo -E docker-compose up
because the root does not know the current user .bashrc file.
'''

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')