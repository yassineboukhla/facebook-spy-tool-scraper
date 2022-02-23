from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys
from bs4 import BeautifulSoup

import unittest, time, re

class Sel(unittest.TestCase):
    def setUp(self):
        #Change the path below to your chromedriver's location
        path = r"C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.facebook.com/ads/library"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        driver = self.driver
        delay = 3
        #You can change multiple things in the link below such as the country,media_type(image,video,all)... or you can bring the link from Facebook ad library with the desired options
        driver.get(self.base_url + "/?active_status=active&ad_type=all&country=DE&q=mode&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=ALL")
        #driver.find_element_by_link_text("All").click()
        #Scroll for an amount of time
        current_time = time.time()
        
        #You can change the scroll pause time, which represents the time to wait for new data to be loaded
        SCROLL_PAUSE_TIME = 7
        
        finished = False
        time.sleep(2)
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        html_source = driver.page_source
        while True:
            
            html_source = driver.page_source
            time.sleep(1)
            #You can change 1800 to the amount of time you want to keep fetching data
            if time.time() >= current_time+1800:
                finished = True
                break
            html_source = driver.page_source
            time.sleep(1)
            print("Current time: ")
            print(time.time())
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            html_source = driver.page_source
            time.sleep(1)
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            html_source = driver.page_source
            time.sleep(1)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            html_source = driver.page_source
        
        #driver.close()
        time.sleep(5)
        """
        for i in range(1,100):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        """
        
        if(finished):
            print("Yes it finished after the specified time")
        else:
            print("It didn't finish by respecting the specified time\n")
        
        soup = BeautifulSoup(html_source, "lxml")
        #data = html_source.encode('utf-8')
        #print(data)
        
        
        
        
       
        
        
        #data = html_source.encode('utf-8')
        #print(data)
        
        
        post = soup.find_all("div", class_="_9b9p")
        post_as_string = str(post)
        post_as_html = BeautifulSoup(post_as_string, "lxml");
        
        count = 0
        ppp= 0
        pre_list = []
        for i in post:
            count = count +1
            elem = str(i)
            
            if((elem.find("<hr class"))==-1):
                pre_list.append(" - ")
            else:
                pre_list.append(" - 1 publicités")
            
        file = open("pre_liste.txt", "w", encoding='utf-8')
        for lll in pre_list:
            file.write("\n")
            file.write(lll)

        file.close()            
        ###################################################################
        ############Extract name of the page###############################
        post = soup.find_all("div",class_="_99s5")
        post_as_string = str(post)
        
        
        ############Extracting number of ads###############################
        div_as_html = BeautifulSoup(post_as_string, "lxml")
        specific_div = div_as_html.find_all("div", class_="_9b9y")
        specific_div_as_text = str(specific_div)
        strong_as_html = BeautifulSoup(specific_div_as_text, "lxml")
        strong = strong_as_html.find_all("strong")
        
        ad_list= []
        for st in strong:
            ad_list.append(st.get_text())
            
        file = open("ad_list.txt", "w", encoding='utf-8')
        k = 0
        while(k<len(ad_list)):
            ad_list[k] = ad_list[k]+"*"
            file.write("\n")
            file.write(ad_list[k])
            k=k+1
        file.close()            
       # print(ad_list)
        
        page_name = div_as_html.select('span.l61y9joe.j8otv06s.a1itoznt.te7ihjl9.svz86pwt.cu1gti5y.a53abz89')
        file = open("liste.txt", "w", encoding='utf-8')
        liste = []
        for div in page_name:
            liste.append(div.get_text())
            
        for llll in liste:
            file.write("\n")
            file.write(llll)
            
        file.close()
        
        
            #list.append(object)
        #Correcting error
        liste.pop(-1)
        liste.pop(-2)
        #####################
        lc = 0
        file = open("discover.txt","w", encoding='utf-8')

        for l in liste:
            try:
                liste[lc] = liste[lc] + pre_list[lc]
                file.write("\n")
                file.write(liste[lc])
                file.write("\n========================")
                lc = lc + 1
            except:
                continue
            
        file.close()
        
        count = 0  
        j = 0
        i=0
        number_ads = ""
        nbrs = ["0","1","2","3","4","5","6","7","8","9"]
        file = open("liste.txt","w", encoding='utf-8')
        save= 0
        for l in liste:
            j=0
            number_ads = ""
            #"1 publicités" is subject to change, if you are using ad library in English you can change it to "1 ads"
            if("1 publicités" in l):
                continue
            else:
                try:
                    cc_data = ad_list[i]#strong[i].get_text()
                except:
                    continue
                while(cc_data[j] in nbrs ):
                    number_ads = number_ads+cc_data[j]
                    j = j +1
                
               # print(number_ads)
                plus = "Plus"                                
                if((cc_data.find(plus)==-1) and int(number_ads)>20):
                    save = save+1
                    l = l+ad_list[i]
                    file.write("\n")
                    file.write(l)
                    file.write("\n====================")
                elif(cc_data.find(plus)!=-1):
                    l = l+ad_list[i]
                    file.write("\n")
                    file.write(l)
                    file.write("\n====================")
                    save=save+1    
                            
                    
                i = i +1
            count = count + 1
            
        print(count," were checked and ",save," were saved!")
        file.close()
        driver.close()
        """
        i = 0
        for tag in strong:
            
            #Getting number of ads "X publicités"
            while((liste[i].find("1 publicités"))!=-1):
               i = i+1
            
            liste[i] = liste[i] + tag.get_text()
        """  
            
        #file = open("liste.txt","w", encoding='utf-8')
        
        #file.close()
        #driver.close()
        #print(strong, type(strong))
        
        """
        counter = 0
        nbr = "0,1,2,3,4,5,6,7,8,9"
        
        for ad in strong:
            #current_ad = str(soup.find("div", class_="_9b9y"))
            
            print("\n===================================================================")
            counter = counter+1
            
            pos = ad.text.find('publicités')
            if(pos!=-1):
                pos=pos-2
                string = ""
                while((ad.text[pos] in nbr) or ad.text[pos]==" "):
                    pos=pos-1
                
                newpos = pos+1
                while((ad.text[newpos] in nbr) or ad.text[newpos]==" "):
                    if(ad.text[newpos]!=" "):
                        string=string+ad.text[newpos]
                        #print(ad.text[newpos], end="")
                    newpos=newpos+1
                if(int(string)>2):
                    print(ad.text)
                    #file.write(ad.text)
                    #file.write("\n===================================================")
                    #file.write("\n===================================================")
                    print("\n===================================")
         
            #file.write("true")
                #file.write("\n==========================================================")
            #print("Inserted.\n")
            #print("\n==========================================================")
            
        #file.close()
        print(counter," were checked")
        """
if __name__ == "__main__":
    unittest.main()

