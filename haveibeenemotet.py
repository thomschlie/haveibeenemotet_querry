#!/usr/bin/env python3
"""Program to querry lots of emails at http://www.haveibeenemotet.com

Author: Thomas Schlieter
Date created: 2021/10/02
Date last modified: 2021/10/02

Copyright (C) 2020 Thomas Schlieter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sys
import re
from collections import namedtuple
import fileinput

#construct the regex
#https://regex101.com/r/ORKB02/1
"""0 times as REAL SENDER, 0 times as FAKE SENDER and 4 times as RECIPIENT."""
REGEX = r"^(?P<real_sender>[0-9]+) times as REAL SENDER, (?P<fake_sender>[0-9]+) times as FAKE SENDER and (?P<recipents>[0-9]+) times as RECIPIENT.$"

#named tuple for easy data keeping
DomainFound = namedtuple('DomainFound',['real_sender', 'fake_sender', 'recipents'])

class HaveIBeenEmotetManager():
    """Context-Manager for querry on 
    http://www.haveibeenemotet.com
    """
    def __init__(self):
        self.SITE='http://www.haveibeenemotet.com'
        self.maxwait = 10 #sec
        self.driver = None
        self.headless = True
    
    def __enter__(self):
        options = Options()
        options.headless = self.headless
        self.driver = webdriver.Firefox(options=options)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.close()

    def emotet(self, email):
        #load site
        self.driver.get(self.SITE) 

        #enter email address
        elem = self.driver.find_element_by_xpath('//input[@name="email-input"]')
        elem.send_keys(email)
        elem.send_keys(Keys.RETURN)

        #wait for loading
        answer = WebDriverWait(self.driver, self.maxwait).until(EC.visibility_of_element_located((By.ID, 'result')))

        #find regex
        m = re.search(REGEX, answer.text,flags=re.MULTILINE)

        # if "NOT found" in answer.text:
        if not m and "NOT found" in answer.text:
            return False, DomainFound(0,0,0)
        elif m and "FOUND!!!" in answer.text:
            findings = DomainFound(int(m.group('real_sender')), \
                                   int(m.group('fake_sender')), \
                                   int(m.group('recipents')))
            return True, findings
        else:
            raise(ValueError(f"No valid answer for Address {email} returned: {answer.text}"))

if __name__ == "__main__":
    #TODO use argpare to
    # to set outputfile
    # toggle output True/False
    # only output Findings (True)
    # input should be on domain/email or newline separated list or file
    # TODO Clean Code


    """Read from file or stdin"""

    email_list = []
    with fileinput.input() as f:    
        for line in f:
            email_list.append(line.strip())


    with HaveIBeenEmotetManager() as HaveIBeen:
        for email in email_list:
            result, findings = HaveIBeen.emotet(email)
            output_string = f"{email}\t{result}\t{findings.real_sender}\t{findings.fake_sender}\t{findings.recipents}"
            print(output_string, file = sys.stdout, flush=True)