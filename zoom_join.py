from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

#4 digits code for the subjects
subject_code_dict = {'photoshop':'3881','plusscience': '3879', 'computer':'3356','music':'3833','art':'3831','social':'3784','moviepedia':'4765',
'heathed':'3798','engskills':'3911','artandcraft':'3851','math':'3342','history':'3791','PE':'3809','thai':'3336','science':'3349','eng':'3862','homeroom':'3119',
'scout':'3927','guide':'3920','plusmath':'3873','อ่านคิด':'4859','cream':'4785'}
#declare variable
course_code = str(subject_code_dict[input('next course code is: ')])

def wait_for_element_to_be_clickable(xpath):
    return WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#create webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
#create action chain (to run chain of actions like move to element and click)
actions = ActionChains(driver)
driver.get("https://www.mycourseville.com/api/login")
Username = driver.find_element_by_id("username")
#make selenium to type 'cudplus63007' to the username field
Username.send_keys('cudplus63007')
password = driver.find_element_by_id("password")
#make selenium to type 'dampfarm51' to the password field
password.send_keys('dampfarm51')
#click on submit
submit = driver.find_element_by_id("cv-login-cvecologinbutton")
submit.click()
#click on cud+
cudplus = driver.find_elements_by_class_name("cv-userhome-apptitle")
cudplus[1].click()
#click on courses
courses = driver.find_elements_by_xpath('//a[contains(@href,"/curriculum/getJoinedCourses?type=other")]')
courses[1].click()
#click on subject
subject = wait_for_element_to_be_clickable(f'//a[contains(@href,"/lms/courseHome?course={course_code}")]')
actions.move_to_element(subject).click().perform()
#click on all meetings
all_meetings = wait_for_element_to_be_clickable(f'//a[contains(@href,"/lms/courseonlinemeetings/{course_code}/index")]')
driver.execute_script("arguments[0].scrollIntoView();", all_meetings)
driver.execute_script("arguments[0].click();", all_meetings) 
sleep(2)
#find all the meeting links
meeting = driver.find_elements_by_tag_name('a')

def find_date():
    day_dict = {0:'จ',1:'อ',2:'พ',3:'พฤ',4:'ศ',5:'ส',6:'อา'}
    #return todays shorten weekday in thai (จ-อา) . date of to day (1-31) ex. จ.7
    return day_dict[datetime.datetime.today().weekday()] + '.' + str(datetime.datetime.today().day)

def find_month():
    return datetime.datetime.today().month
month_dict = {'ม.ค.':1,'ก.พ.':2,'มี.ค.':3,'เม.ย.':4,'พ.ค.':5,'มิ.ย.':6,'ก.ค.':7,'ส.ค.':8,'ก.ย.':9,'ต.ค.':10,'พ.ย.':11,'ธ.ค.':12}
this_month = find_month()
months = driver.find_elements_by_class_name("ss-month.ss-color-1")
meetings = driver.find_elements_by_class_name("ss-dow-date")
today_date = find_date()
add = 0
#loop on all of the dates of the meetings
for i, element in enumerate(meetings):
    #if the date is today
    if month_dict[months[i].text] > this_month:
        add += 1
        break
    if int(element.text[2:]) >= int(today_date[2:]):
        add += 1
        break
    if element.text == today_date and month_dict[months[i].text] == this_month:
        #click that meeting link
        #Add more index for upcoming meetings
        meeting[25+i+add].click()
        break
    if len(meetings) - i == 1:
        driver.quit()
meeting_link = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ml-2'))) 
meeting_link.click()
sleep(2)
#click to always launch meetings pop up using an actual click on position
pyautogui.click(800,300)
sleep(0.0000000000000000000000000000000000000000000000000000000001)
#close chrome driver
driver.quit()