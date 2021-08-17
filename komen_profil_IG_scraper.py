from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
from selenium.webdriver.common.action_chains import ActionChains
import datetime

class InstaCrawl:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome("C:/Users/acer/Downloads/chromedriver.exe")

    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        email = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(5)

    def scrape_profil(self,profil):
        bot = self.bot
        bot.get('https://www.instagram.com/'+ profil +'/')
        time.sleep(2)
        
        # buat variabel untuk perulangannya
        total_post = bot.find_element_by_class_name('g47SY')
        rawpost = total_post.text

        # cek apakah ada koma pada total postnya
        if ',' in rawpost:
            rawpost = rawpost.replace(',','')
            post = int(rawpost)
        else:
            post = int(rawpost)

        print('Terdapat '+str(post)+ ' total post.')
        
        # cek kondisi untuk perulangan
        if post > 2:
            print('Melakukan perulangan sebanyak '+str(post))
        elif post > 1:
            print('Melakukan perulangan sebanyak '+str(post))
        else:
            print('Melakukan perulangan sebanyak '+str(post))

        print('MEMULAI PROSES SCRAPING...')
        u = 0

        # cek kondisi bila post lebih dari 2 atau tidak
        # kalau post lebih dari 3
        
        url_list = []

        if post > 2:
            fcard = bot.find_element_by_css_selector('.v1Nh3.kIKUG._bz0w')
            acard = fcard.find_element_by_tag_name('a')
            acard.click()
            time.sleep(1)
            
            # masukan url ke txt
            url_list.append(bot.current_url)

            # tambahkan variabel u
            u+= 1

            # lanjut ke post selanjutnya
            button_next = bot.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a')
            button_next.click()
            time.sleep(1)

            # masukan url ke txt
            url_list.append(bot.current_url)

            # tambahkan variabel u
            u+= 1

            # u = 2
            while ( u < post ):
                # lanjut ke post selanjutnya
                button_next = bot.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]')
                button_next.click()
                time.sleep(1)

                # masukan url ke txt
                url_list.append(bot.current_url)

                u+=1

            # simpan kumpulan url ke txt
            f = open('data_kotor/url_txt/txt_'+ str(profil) +'.txt', 'a', encoding="utf-8")
            for lu in url_list:
                f.write(str(lu) +'\n')
        

        # kondisi kalau post ada 2
        elif post == 2:
            fcard = bot.find_element_by_css_selector('.v1Nh3.kIKUG._bz0w')
            acard = fcard.find_element_by_tag_name('a')
            acard.click()
            time.sleep(1)

            # masukan url ke txt
            url_list.append(bot.current_url)

            # tambahkan variabel u
            u+= 1

            # lanjut ke post selanjutnya
            button_next = bot.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
            button_next.click()
            time.sleep(1)

            # masukan url ke txt
            url_list.append(bot.current_url)

            # simpan kumpulan url ke txt
            f = open('data_kotor/url_txt/txt_'+ str(profil) +'.txt', 'a', encoding="utf-8")
            for lu in url_list:
                f.write(str(lu) +'\n')

        # post = 1
        else:
            fcard = bot.find_element_by_css_selector('.v1Nh3.kIKUG._bz0w')
            acard = fcard.find_element_by_tag_name('a')
            acard.click()
            time.sleep(1)

            # masukan url ke txt
            url_list.append(bot.current_url)

            # simpan kumpulan url ke txt
            f = open('data_kotor/url_txt/txt_'+ str(profil) +'.txt', 'a', encoding="utf-8")
            for lu in url_list:
                f.write(str(lu) +'\n')

        time.sleep(2)

        url = open('data_kotor/url_txt/txt_'+ str(profil) +'.txt', 'r')

        for u in url:
            # pergi ke URL Postingan
            bot.get(u)

            try:
                time.sleep(2)

                # buat variabel untuk menyimpan tombol 'komentar lebih banyak'
                load_more_comments = bot.find_element_by_css_selector('#react-root > section > main > div > div.ltEKP > article > div.eo2As > div.EtaWk > ul > li > div > button')
                
                # lakukan perulangan sampai tombol 'komentar lebih banyak' tidak muncul
                total_komen = 0
                while load_more_comments.is_displayed():
                    load_more_comments.click()
                    time.sleep(4)
                    total_komen += 1

                    # buat variabel untuk menyimpan tombol 'komentar lebih banyak'
                    time.sleep(1.5)
                    load_more_comments = bot.find_element_by_css_selector('#react-root > section > main > div > div.ltEKP > article > div.eo2As > div.EtaWk > ul > li > div > button')

            except Exception as e:
                # Jalankan fungsi scrape_id_comment()
                # buat array username dan user_komen
                usernames = []
                user_komen = []

                # mengambil seluruh kolom komen
                kolom_komen = bot.find_elements_by_class_name('Mr508')

                # untuk xpath pada komen
                kontainer_komen = 1
                for kk in kolom_komen:
                    kontener = kk.find_element_by_class_name('C4VMK')

                    # nama akun
                    nama_akun = kontener.find_element_by_class_name('_6lAjh').text
                    
                    # Komen
                    komen = kontener.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul['+str(kontainer_komen)+']/div/li/div/div[1]/div[2]/span').text
                    komen = komen.replace('\n', ' ').strip().rstrip()
                    
                    # tanggal postingan
                    tp = bot.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time')
                    tp = tp.get_attribute('title')

                    # tanggal komen
                    class_tanggal = kk.find_element_by_class_name('FH9sR')
                    tanggal = class_tanggal.get_attribute('title')

                    # url post
                    up = bot.current_url

                    # love post
                    # love = bot.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span').text
                    
                    # masukan usernam & user_komen yang telah dikumpulkan ke array username & user_komen yang telah dibuat sebelumnya
                    usernames.append(nama_akun)
                    user_komen.append(komen)

                    print('=======================================')
                    print(kontainer_komen)
                    print('URL : '+up)
                    print('Tanggal postingan : '+tp)
                    print(nama_akun)
                    print('Memberikan komentar : '+komen)
                    print('Pada tanggal : '+tanggal)

                    # buka file csv yang telah dibuat sebelumnya
                    bukacsv = open('data_kotor/url_txt/hasil/dataset_'+ str(profil) +'.csv', 'a', encoding='utf-8', newline='\n')
                    save = csv.writer(bukacsv)
                    save.writerow(['=HYPERLINK("'+up+'")', tp, nama_akun, komen, tanggal]) 

                    kontainer_komen += 1
                    pass
        
    def menu(self):          
        bot = self.bot
        # Menu Awal
        print('=============================================')
        print('[1]. Scrape data berdasarkan nama profil akun')
        print('[2]. Keluar')
        print('=============================================')

        bot.quit()
        time.sleep(2)
        # Pilih menu
        pilihan = input('Masukan pilihan menu ke : ')

        # pengkondisian menu pilihan
        if pilihan == '1':
            # menu scrape data berdasarkan nama IG akun
            print('=============================================')
            key = input('Masukkan nama akun : ')
            insta = InstaCrawl(usr,password)
            insta.login()
            insta.scrape_profil(key)
        elif pilihan == '2':
            # menu Keluar
            print('=============================================')
            quit('Keluar dari program')
        else:
            print('Pilihan tidak diketahui!!')
            quit('Keluar dari program')

# ambil pw dan user pada file .txt
pw = open('F:/Kuliah/KerjaPraktek/Selenium/tascraper/login/pw.txt', "r", encoding="utf-8")
password = str(pw.read())
user = open('F:/Kuliah/KerjaPraktek/Selenium/tascraper/login/usr.txt', "r", encoding="utf-8")
usr = str(user.read())

# Halaman Awal
insta = InstaCrawl(usr,password)
insta.login()
insta.menu()