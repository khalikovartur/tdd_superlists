from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
        
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
                
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy peacock feathers')
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('make a spot')
        inputbox.send_keys(Keys.ENTER)
               
        self.wait_for_row_in_list_table('2: make a spot')
        self.wait_for_row_in_list_table('1: buy peacock feathers')
        
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: buy peacock feathers', [row.text for row in rows])
        self.assertIn('2: make a spot', [row.text for row in rows])
        
        
    def test_multiple_users_can_start_lists_at_diffrent_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy peacock feathers')
        
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')        

        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #New user2 come to home page
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('buy peacock feathers', page_text)
        self.assertNotIn('make a spot', page_text)
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy milk')
        
        #New user2 get unique url
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)
        
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('buy peacock feathers', page_text)
        self.assertIn('buy milk', page_text)
        
                
        
        
        

