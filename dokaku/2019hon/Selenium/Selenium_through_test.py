# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re
import datetime
from datetime import datetime
import get_gmail
from get_gmail import GmailClient


# In[2]:

# ----------------------
# 環境設定
# ----------------------
for line in open("config.txt"):
   itemlist = line.strip().split(",")
   mail_name = itemlist[0]
   password = itemlist[1]
   file = itemlist[2]
   base_url = itemlist[3]
# Webdriverの設定 (Firefox)
driver = webdriver.Firefox()
driver.implicitly_wait(10)


# In[ ]:

# スクロール実行メソッド
def scroll(time):
    driver.execute_script('jQuery("html, body").animate({ scrollTop: jQuery(document).height() }, ' + str(time) + ');')


def email_get():
    count = 1
    if not messages:
        print('No messages found.')
    else:
        for message in messages:
            title.append(message.subject)
            body.append(message.body)
            date.append(message.date)
            count += 1
            if count == 4:
                break

def email_check():
    if (len(title) != 3) or (len(body) != 3):
        print('Messages did not get enough')
    else:
        if (title[2].endswith("ご登録ありがとうございます＜要保存＞")) and (body[2].find(email_address)):
            print("基本登録完了メールOK")
            print(title[2], date[2])
            if (title[1].endswith("登録内容の変更を受け付けました")) and (body[1].find("志望情報の登録内容が変更されました")):
                print("志望情報変更メールOK")
                print(title[1], date[1])
                if (title[0].endswith("登録内容の変更を受け付けました")) and (body[0].find("語学・資格情報の登録内容が変更されました")):
                    print("語学・資格変更メールOK")
                    print(title[0], date[0])
                else:
                    print("語学・資格変更メールNG")
            else:
                print("志望情報変更メールNG")
        else:
            print("基本登録完了メールNG")


# In[ ]:

def test_check_top_page():
    """"
    1. ログイン前topページ確認
    共通：表示崩れがないこと (目視)
    18本：フッターまで表示されていること
    """
    driver.get(base_url+"top/")
    scroll(10000)
    time.sleep(7)
    print("ログイン前トップ完了")


# In[ ]:

def test_create_profile():
    """
    2. 会員登録確認
    で会員登録を行い、正常に完了画面まで到達できること
    ＊追加情報入力画面後の完了画面
    """
    def test_start_registration():
        driver.find_element_by_link_text("会員登録").click()
        time.sleep(2)

    def test_name_and_address_page():
        # fill out 氏名・メールアドレス page

        driver.find_element_by_id("lastNm").click()
        driver.find_element_by_id("lastNm").clear()
        driver.find_element_by_id("lastNm").send_keys(u"テスト")
        driver.find_element_by_id("firstNm").clear()
        driver.find_element_by_id("firstNm").send_keys(u"太郎")

        driver.find_element_by_id("lastNmKana").clear()
        driver.find_element_by_id("lastNmKana").send_keys(u"テスト")

        driver.find_element_by_id("firstNmKana").clear()
        driver.find_element_by_id("firstNmKana").send_keys(u"タロウ")

        driver.find_element_by_id("eMail").click()
        driver.find_element_by_id("eMail").clear()
        driver.find_element_by_id("eMail").send_keys(email_address)
        driver.find_element_by_id("eMailConfirm").clear()
        driver.find_element_by_id("eMailConfirm").send_keys(email_address)
        driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("passwordConfirm").clear()
        driver.find_element_by_id("passwordConfirm").send_keys(password)
        scroll(2000)
        time.sleep(2)
        driver.find_element_by_id("FormAssist_submit").click()
        driver.implicitly_wait(5)

    def test_school_info_page():
        # fill out 学校情報 page

        driver.find_element_by_css_selector("label[for=schoolKndCd1]").click()

        driver.find_element_by_id("schoolNm").click()

        driver.find_element_by_id("schoolNm").send_keys(u"テスト大学"+Keys.TAB)

        driver.find_element_by_id("facultyNm").send_keys(u"テスト学部"+Keys.TAB)

        time.sleep(.3)
        driver.find_element_by_id("subjectNm").send_keys(u"テスト学科"+Keys.TAB)
        
        driver.find_element_by_css_selector("label[for=liberalScienceCls0]").click()
        time.sleep(1)
        driver.find_element_by_css_selector("ul.register-school__list.mb > li.is_active > label").click()
        driver.find_element_by_css_selector("label[for=regularGrdYear]").click()
        scroll(2000)
        time.sleep(1.5)
        driver.find_element_by_css_selector("li.mb10.is_active > label").click()
        time.sleep(1.5)
        driver.find_element_by_id("FormAssist_submit").click()
        driver.implicitly_wait(5)
        
    def test_contact_info_page():
        # fill out 連絡先 page

        driver.find_element_by_id("postCd").clear()
        driver.find_element_by_id("postCd").send_keys("1120004")

        driver.find_element_by_id("municipality").click()
        driver.find_element_by_id("municipality").clear()
        driver.find_element_by_id("municipality").send_keys(u"テストテスト")
        time.sleep(1)
        
        driver.find_element_by_id("telHand").click()
        driver.find_element_by_id("telHand").clear()
        driver.find_element_by_id("telHand").send_keys("555-5555-5555")
        driver.find_element_by_id("tel").click()
        driver.find_element_by_id("tel").clear()
        driver.find_element_by_id("tel").send_keys("55-5555-5555")
        scroll(2000)
        time.sleep(2)
        driver.find_element_by_css_selector("label[for=radio2-1]").click()
        
        time.sleep(1.5)
        driver.find_element_by_name("nextButton").click()
        
    def test_go_to_optional_profile_pages():
        scroll(3000)
        time.sleep(3)
        driver.find_element_by_css_selector("input.btnS-register[value=次へ]").click()
        
    def test_shibou_info_page():
        """
        志望情報画面
        """
        scroll(8000)
        time.sleep(6)
        driver.find_element_by_css_selector("input.btnS-register[value=保存して次へ]").click()
        
    def test_languages_and_certifications_page():
        scroll(8000)
        time.sleep(6)
        driver.find_element_by_css_selector("input.btnS-register[value=保存して次へ]").click() 
        
    def test_go_to_profile_sheet():
        scroll(5000)
        time.sleep(3)
        driver.find_element_by_css_selector("input[value=プロフィールシートを確認、入力する]").click()
        
    def test_profile_sheet_page():
        #assert that school name is right
        #assert that department and division names are right
        #assert that graduation date is correct
        scroll(10000)
        time.sleep(8)
        driver.find_element_by_css_selector("input[value=保存して編集を完了する]").click()
        
    def test_profile_complete_page():
        scroll(2000)
        time.sleep(2)
        driver.find_element_by_css_selector("input[value=マイページを見てみる]").click()
        
    def test_logged_in_to_my_page():
        scroll(10000)
        time.sleep(4)

    # Call subtests (PLEASE UNCOMMENT ME!)
    #########################################
    test_start_registration()
    test_name_and_address_page()
    test_school_info_page()
    test_contact_info_page()
    test_go_to_optional_profile_pages()
    
    test_shibou_info_page()
    
    test_languages_and_certifications_page()
    
    test_go_to_profile_sheet()
    test_profile_sheet_page()
    test_profile_complete_page()
    print("会員登録完了")
    test_logged_in_to_my_page()
    print("メール確認中")
    time.sleep(10)
    email_get()
    email_check()

    print("マイページ確認完了")
    # print(body)


# In[ ]:

def log_out():
    driver.find_element_by_css_selector("a.header__logout[href='/2019/top/login/logout/']").click()
    
def test_log_out():
    log_out()
    error_text = ""
    try:
        error_text = driver.find_element_by_id("login_target").text
    finally:
        assert error_text == "ログイン"
    print("ログアウト完了")

def log_in():
    email_address = "000000@disc.co.jp"
    password = "000000"
    time.sleep(1)
    driver.find_element_by_id("login_target").click()
    driver.find_element_by_id("iNamLoginId").send_keys(email_address)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(1)
    driver.find_element_by_id("login-blockD-2__form__submit").click()
    
def assert_logged_in():
    assert driver.find_element_by_css_selector("a.header__logout[href='/2019/top/login/logout/']").text == "ログアウト"
    
def test_log_in():
    log_in()
    assert_logged_in()
    print("ログイン完了")


# In[ ]:

def test_check_login_top_page():
    """
    3-2. ログイン後topページ確認
    共通：表示崩れがないこと、フッターまで表示されていること
    """
    scroll(10000)
    time.sleep(6)
    print("ログイン後トップ完了")
    
def test_company_search():
    """
    4. 企業検索
    企業検索 (採用年/search/condition/)の業種・エリアなどのラジオボタンをonにして、該当社数表示が正常かを確認
    """
    driver.get(base_url + "search/condition/")
    scroll(6000)
    time.sleep(6)
    driver.find_element_by_css_selector("a[href='#js-popup-corp']").click()
    time.sleep(1.5)
    driver.find_element_by_id("categoryC1_3").click()
    time.sleep(1.5)
    driver.find_element_by_css_selector("label[for=itemC1_3_1_all]").click()
    time.sleep(1.5)
    driver.find_element_by_id("tab_C2").click()
    time.sleep(1.5)
    driver.find_element_by_css_selector("label[for=itemC2_1_all]").click()
    time.sleep(1.5)
    search_before = driver.find_element_by_css_selector("div.refine_bottom > p > span").text
    driver.find_element_by_css_selector("input.btn-search[value=この条件で検索する]").click()
    search_after = driver.find_element_by_class_name("pager__count__num").text
    search_pager = driver.find_elements_by_class_name("pager__num")
    scroll(12000)
    time.sleep(6)
    search_pager[-1].click()
    try:
        assert search_before == search_after, "/search/condition/画面取得件数[{0}], /search/corp/type/画面取得件数[{1}]".format(search_before, search_after)
    except AssertionError as err:
        print("AssertionError : ", err)
    print("/search/condition/画面取得件数[{0}], /search/corp/type/画面取得件数[{1}]".format(search_before, search_after))
    print("企業検索完了、件数確認完了")
    
def test_seminar_search():
    """
    5. セミナー検索 (18本)
    フリーワード検索で (IVIS・銀行)の2種類を検索し、検索結果が正常か、表示エラーがないかを確認
    """
    driver.get(base_url + "search/condition/")
    time.sleep(2)
    driver.find_element_by_id("seminarFreeWord").click()
    driver.find_element_by_id("seminarFreeWord").clear()
    driver.find_element_by_id("seminarFreeWord").send_keys(u"IVIS")
    time.sleep(1)
    driver.execute_script("searchSeminarFreeWordBtn();")
    time.sleep(3)
    scroll(5000)
    time.sleep(5)
    print("フリーワード検索「IVIS」完了")
    
    driver.get(base_url + "search/condition/")
    time.sleep(2)
    driver.find_element_by_id("seminarFreeWord").click()
    driver.find_element_by_id("seminarFreeWord").clear()
    driver.find_element_by_id("seminarFreeWord").send_keys(u"銀行")
    time.sleep(1)
    driver.execute_script("searchSeminarFreeWordBtn();")
    time.sleep(3)
    driver.execute_script("changeTab('0');")
    time.sleep(3)
    scroll(5000)
    time.sleep(5)
    print("フリーワード検索「銀行」完了")
    
def test_view_company_details_page():
    """
    6. 企業ページ遷移後、表示エラーがないかを確認
    """
    driver.get(base_url + "search/corp/type/")
    c = driver.find_elements_by_class_name("btnS")
    count = 0
    for item in c:
        if item.text == "000000":
            break
        count += 1
    c[count].click()
    window = driver.window_handles
    driver.switch_to.window(window[1])
    time.sleep(3)
    scroll(5000)
    time.sleep(3)
    driver.close()
    print("オリタブ確認完了")
    driver.switch_to.window(window[0])
    scroll(5000)
    time.sleep(5)
    print("企業検索ONLOAD確認完了")
    
def test_view_my_page():
    """
    7. マイページへ遷移後、表示エラーがないかを確認
    """
    driver.get(base_url + "mypage/favorites/")
    

if __name__ == '__main__':
    title = list()
    body = list()
    date = list()
    Gmail = GmailClient()
    messages = Gmail.get_messages()
# # テスト手動実行
# 
# テストを１セルずつ実行して、指示通りの動作確認をしてください。

# ## 1. ログイン前topページ確認
# 下記を実行した上、表示崩れがないことのご確認ください。 
# - 18本：フッターまで表示されていること  
# - 19本：業界大手・トップクラスの企業から探す部品 (企業研究タブ)にIS企業と転載企業が入っていること

# In[ ]:

    test_check_top_page()


# ## 2. 会員登録確認
# 
# 下記の実行で会員登録を行います。  
# 登録完了通知メールなども自動的に行うため、実行が少し遅いですが、  
# 実行完了までお待ちください。
# 
# 軽く変なことがないようにご監視ください。

# In[ ]:

    today = datetime.now().strftime("%Y%m%d%H%M%S")
    email_address = mail_name + "+" + today + "@gmail.com"
    test_create_profile()



# ## 3.1. ログアウト・ログイン確認
# 
# 一度ログアウトして、作ったばかりのユーザでログインします。

# In[ ]:

    test_log_out()
    test_log_in()


# ## 3.2. ログイン後topページ確認
# 
# 共通：表示崩れがないこと、フッターまで表示されていること
# 
# 〇〇さんにおすすめの企業に企業が表示されていること

# In[ ]:

    test_check_login_top_page()


# ## 4. 企業検索
# 企業検索 (採用年/search/condition/)の業種・エリアなどのラジオボタンをonにして、該当社数表示が正常かを確認
# 
# サイト停止までに現在の結果をメモ
# 
# 
# (check that number is same before and after search

# In[ ]:

    test_company_search()


# ## 5. セミナー検索 (18本)
# フリーワード検索で (IVIS・銀行)の2種類を検索し、検索結果が正常か、表示エラーがないかを確認
# 
# サイト停止までに現在の結果をメモ

# In[ ]:

    test_seminar_search()


# ## 6. 株式会社アイヴィスの企業ページ遷移後、表示エラーがないかを確認

# In[ ]:

    test_view_company_details_page()


# ## 7. マイページへ遷移後、ログアウト

# In[ ]:

    test_view_my_page()
    test_log_out()


# In[ ]:

    input("Press 'Enter' to Exit")
    driver.close()
