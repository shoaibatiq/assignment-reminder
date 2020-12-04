#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from airtable import Airtable
from Google import Create_Service, convert_to_RFC_datetime
airtable=Airtable(api_key='api_key',table_name='table_name',base_key='base_key')
from time import sleep


# In[100]:


driver=webdriver.Chrome("chromedriver.exe")
driver.set_window_size(1366, 768)


# In[101]:


driver.get("https://slate.uol.edu.pk")
auth_link= driver.find_element_by_xpath("//a[contains(@href,'oauth2')]").get_attribute('href')
driver.get(auth_link)
email_input=driver.find_element_by_xpath("//input[@type='email']")
email_input.send_keys("email_address@domain.com")

email_input.send_keys(Keys.RETURN)


sleep(4)
pwd_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
pwd_input.send_keys("pa$$word")
pwd_input.send_keys(Keys.RETURN)


# try:
#     driver.find_element_by_xpath('//a[@title="Google"]').click()
# except:
#     pass


# In[102]:


WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="notice"]//button[contains(text(),"Cancel")]'))).click()


# In[103]:


WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label,"activities per page")]'))).click()


# In[104]:


driver.find_element('xpath','//a[@data-limit="25"]').click()


# In[105]:


sleep(10)


# In[106]:


main_id= driver.find_element('xpath','//div[@class="tab-pane active show fade"]').get_attribute('id')


# In[107]:


h5 = [i.text.split(',')[-1].strip() for i in driver.find_elements('xpath',f'//div[@id="{main_id}"]//h5')]
tasks= driver.find_elements('xpath',f'//div[@id="{main_id}"]//h5//following::div[@class="pl-0 list-group list-group-flush"]')


# In[108]:


f'//div[@id="{main_id}"]//h5'


# In[109]:


s=""
d={h5[i]:[] for i in range(len(h5))}
for ind,task in enumerate(tasks):
    for i in task.text.split():
        if(len(i)==5 and ":" in i):
            d[h5[ind]].append([s.replace('"',''),i])
            s=""
            continue
        s+=i +" "
    


# In[110]:


driver.quit()


# In[122]:


d


# In[117]:


prev=[]
for i in airtable.get_all():
    prev.append(list(i['fields'].values()))


# In[118]:


for date,tasks in d.items():
    for task in tasks:
        if([date,task[1],task[0]] in prev):
            d[date][tasks.index(task)] = None


# In[119]:


service = Create_Service('client_secrets.json', 'calendar', 'v3', ['https://www.googleapis.com/auth/calendar'])


# In[120]:


def Event(t,D):
    return {
      'summary': t,
      'start': {
        'dateTime': D,
        'timeZone': 'GMT+05:00',
      },
      'end': {
        'dateTime': D ,
        'timeZone': 'GMT+05:00',
      },
    #   'attendees': [
    #     {'email': 'lpage@example.com'},
    #     {'email': 'sbrin@example.com'},
    #   ],
      'reminders': {
        'useDefault': False,
        'overrides': [
    #       {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 13*60},
        ],
      },
    }
months={"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8,
        "September":9, "October":10, "November":11, "December":12

}
for date,ts in d.items():
    for t in ts:
        if(t is None):
            continue
        print(t)
        dd=date.split(" ")
        D = convert_to_RFC_datetime(int(dd[-1]),months[dd[1]],int(dd[0]),int(t[1].split(':')[0]),int(t[1].split(':')[1]))
        service.events().insert(calendarId='calendar_id', body=Event(t[0],D)).execute()
        
    



# In[121]:


for date,tasks in d.items():
    for task in tasks:
        if(task is None):
            continue
        airtable.insert({"Date":date,"Time":task[1],"Assignment":task[0]})


# In[ ]:





# In[ ]:




