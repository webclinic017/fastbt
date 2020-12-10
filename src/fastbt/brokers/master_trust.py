import pandas as pd
import os
from fastbt.Meta import Broker,Status,pre,post
from requests_oauthlib import OAuth2Session

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_authorization_url():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, _state = oauth.authorization_url(authorization_base_url, access_type="authorization_code")
    print(_state)
    return authorization_url

class MasterTrust(Broker):
    """
    Automated Trading class
    """
    def __init__(self, client_id, password,
                PIN, secret, exchange='NSE',
                product='MIS'):
        self._client_id = client_id 
        self._password = password
        self._pin = PIN
        self._secret = secret
        self.exchange = exchange
        self.product = product
        self._store_access_token = True        
        self._access_token = None
        self.base_url = 'https://masterswift-beta.mastertrust.co.in'
        self.authorization_base_url = f"{self.base_url}/oauth2/auth"
        self.token_url = f"{self.base_url}/oauth2/token"
        super(MasterTrust, self).__init__()

    def get_authorization_url(self, client_id='APIUSER', redirect_uri='http://127.0.0.1/',
            scope=['orders']):
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        authorization_url, _state = oauth.authorization_url(self.authorization_base_url,
                access_type="authorization_code")
        return authorization_url

    def get_access_token(self, url, redirect_uri='http://127.0.0.1/',
            scope=['orders']):
        # to make oauth2 work with http
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        oauth = OAuth2Session('APIUSER',redirect_uri=redirect_uri, scope=scope)
        token = oauth.fetch_token(self.token_url, authorization_response=url, client_secret=self._secret)
        access_token = token['access_token']
        self._access_token = token
        return token
            
    def _shortcuts(self):
        """
        Provides shortcuts to master trust function
        """
        pass

    def authenticate(self):
        """
        Authenticates a session if access token is already
        available by looking at the token.tok file.
        In case authentication fails, try a fresh login
        """
        login_url = self._login() 
        print('LOGIN URL')
        print(login_url)
        token = self.get_access_token(login_url)
        print(token)

    
    def _login(self):
        import time
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        url = self.get_authorization_url()
        driver.get(url)
        time.sleep(2)
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-container")))
        driver.find_element_by_name('login_id').send_keys(self._client_id)
        driver.find_element_by_name('password').send_keys(self._password)
        driver.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(2)
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-container")))
        driver.find_element_by_xpath('//input[@type="password"]').send_keys(self._pin)
        driver.find_element_by_xpath('//button[@type="submit"]').click() 
        time.sleep(2)
        current_url = driver.current_url
        driver.close()
        return current_url 
