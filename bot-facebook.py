from selenium import webdriver
import hashlib
import csv
import time
import os.path

#url, ilk ve son elementlerin div sıraları ve html elementleri

urls=["https://www.facebook.com/Hülya-Erdem-111751313846537","https://www.facebook.com/Keles-Belediyesi-1522353218086722","https://www.facebook.com/besiktasbelediyesi","https://www.facebook.com/SultanbeyliBel","https://www.facebook.com/Arnavutkoybelediyesi","https://www.facebook.com/EsenyurtBLDYS","https://www.facebook.com/Buyukcekmecebld","https://www.facebook.com/KaracabeyBel"]
divNum=[43,106,105,153,45,123,55,146,96,221,61,152,114,273,34,70]
htmls=['/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div[{x}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[{x}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[{x}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div/div/div/div[{x}]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[{x}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[{x}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div/div/div/div[{x}]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div[{x}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]',
]

def function(url,divNumFirst,divNumLast,htmlNum):

    #url'yi md5'e çevirme

    textUtf8=url.encode("utf-8")
    md5=hashlib.md5(textUtf8)

    #bağlantı ve ekran görüntüsü

    browser = webdriver.Chrome(executable_path='C:/Users/admin/Downloads/chromedriver_win32/chromedriver.exe')
    browser.get(url)
    print("Baglanti kuruluyor...")
    time.sleep(3)
    print("Ekran goruntusu aliniyor...")
    browser.get_screenshot_as_file('bot-facebook_{}.png'.format(md5.hexdigest()))
    time.sleep(3)

    #veriye ulaşma ve ekran kaydırma

    total=[]

    print("Verilere erisiliyor...")

    def scroll(browser, timeout, tota):
        scroll_pause_time = timeout

        last_height = browser.execute_script("return document.body.scrollHeight")
        
        for j in range(55):

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(scroll_pause_time)
            
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:      
                break

            last_height = new_height
            
            for num in range (divNumFirst,divNumLast):
                try:
                    path = browser.find_element("xpath",htmlNum.format(x=num))               
                    if(path.text!=""):
                        tota.append(str(path.text))
                        print(path.text)
                except:
                    pass    
                 
    scroll(browser, 3 , total)
    time.sleep(3)

    #verileri düzenleme ve ekleme

    for i in range(len(total)):
        total[i] = total[i].replace('\n'," , ")
        total[i] = total[i].replace("Beğen , Yorum Yap , Paylaş", "")
        total[i] = total[i].replace("124 B , 3,3 B Yorum , 3,9 B Paylaşım","")
        
    while("" in total) :
        total.remove("")    

    totB=[]
    totY=[]
    totP=[]
    for i in range(len(total)):
        if(type(total[i]) == str):
            a=list(int(s) for s in total[i].split() if s.isdigit())
            a[0]=int(a[0])
            totB.append(a[0])
            if ("Yorum" in total[i]) and ("Paylaşım" not in total[i]):
                a[1]=int(a[1])
                totY.append(a[1])
                a.append(int(0))
                totP.append(a[2])
            elif("Paylaşım" in total[i]) and ("Yorum" not in total[i]):
                a.append(int(0))
                a[2]=int(a[1])
                a[1]=int(0)
                totY.append(a[1])
                totP.append(a[2])
            elif("Paylaşım" in total[i]) and ("Yorum" in total[i]):
                a[1]=int(a[1])
                totY.append(a[1])
                a[2]=int(a[2])
                totP.append(a[2])
            else:
                a.append(int(0))
                a.append(int(0))
                totY.append(a[1])
                totP.append(a[2])

    #csv'ye yazdırma

    print("csv olusturuluyor...")
    with open('bot-facebook_{}.csv'.format(md5.hexdigest()),'a',newline='')as f:
        fileEmpty = os.stat('bot-facebook_{}.csv'.format(md5.hexdigest())).st_size == 0
        field=['begeni','yorum', 'paylasim']
        writer=csv.DictWriter(f,fieldnames=field)
        if fileEmpty:
            writer.writeheader()
        for i in range(len(totB)):
            writer.writerow({'begeni':totB[i],'yorum':totY[i],'paylasim':totP[i]})

    #csv'den toplama

    print("csv olusturuluyor...")
    with open('bot-facebook_202206.csv','a',newline='')as f:
        fileEmpty = os.stat('bot-facebook_202206.csv').st_size == 0
        field=['url','Md5','begeni','yorum', 'paylasim']
        writer=csv.DictWriter(f,fieldnames=field)
        if fileEmpty:
            writer.writeheader()
        writer.writerow({'url':url ,'Md5':md5.hexdigest() , 'begeni':sum(totB), 'yorum':sum(totY) , 'paylasim':sum(totP)})

    browser.quit()

#siteleri çağırma

function(urls[0],divNum[0],divNum[1],htmls[0])
function(urls[1],divNum[2],divNum[3],htmls[1])
function(urls[2],divNum[4],divNum[5],htmls[2])
function(urls[3],divNum[6],divNum[7],htmls[3])
function(urls[4],divNum[8],divNum[9],htmls[4])
function(urls[5],divNum[10],divNum[11],htmls[5])
function(urls[6],divNum[12],divNum[13],htmls[6])
function(urls[7],divNum[14],divNum[15],htmls[7])