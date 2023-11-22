import json
import os
import time
import glob
from sanitize_filename import sanitize
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.keys import Keys
import linkPy 

issue_created = False

#######################################################################################################

counties = [
    'Barnstable County Probate and Family Court',
    'Berkshire County Probate and Family Court',
    'Bristol County Probate and Family Court',
    'Dukes County Probate and Family Court',
    'Essex County Probate and Family Court',
    'Franklin County Probate and Family Court',
    'Hampden County Probate and Family Court',
    'Hampshire County Probate and Family Court',
    'Middlesex County Probate and Family Court',
    'Nantucket County Probate and Family Court',
    'Norfolk County Probate and Family Court',
    'Plymouth Probate and Family Court',
    'Suffolk County Probate and Family Court',
    'Worcester County Probate and Family Court' ]
case_no_pfx = [ 'BA', 'BE', 'BR', 'DU', 'ES', 'FR', 'HD', 'HS', 'MI', 'NA', 'NO', 'PL', 'SU', 'WO' ]
county_list = [ 
    'Barnstable',
    'Berkshire',
    'Bristol',
    'Dukes',
    'Essex',
    'Franklin',
    'Hampden',
    'Hampshire',
    'Middlesex',
    'Nantucket',
    'Norfolk',
    'Plymouth',
    'Suffolk',
    'Worcester'
]

# Check download directory

download_path = r'D:\Courts'

files = glob.glob(download_path + r'\search*.pdf')
# Iterate over the list of filepaths & remove each file.
for file in files:
    try:
        os.remove(file)
    except:
        print("Error while deleting file : ", file)
        exit()

#######################################################################################################

# Set the desired filename
file_name = 'searchresults.pdf'

issue_file_path = os.path.join(download_path, 'issue.txt')
start_no = 0 # county no
if not os.path.exists(issue_file_path):
    start_date = input("Enter the date (MM/DD/YYYY): ")
    end_date = input("Enter the end date (MM/DD/YYYY): ")
else:
    issue_file = open(issue_file_path, 'rt')
    issue_list = issue_file.read().split('\n')
    issue_list = [x for x in issue_list if x != '']
    start_no = int(issue_list[0])
    start_date = issue_list[1]
    end_date = issue_list[2]
    issue_file.close()

print('start at:', counties[start_no])

chrome_options = webdriver.ChromeOptions()
download_path = r'D:\Courts'
cache_path=download_path+r'\cache'
download_path_keer = r'D:\Courts'
chrome_options.add_experimental_option('prefs', {
"download.default_directory": download_path, # change default directory for downloads
"download.prompt_for_download": False, # to auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True # it will not show PDF directly in chrome
})
chrome_options.add_argument(f"user-data-dir={cache_path}")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://www.masscourts.org/eservices/home.page.2")

# Wait for the page to load completely
wait = WebDriverWait(driver, 20)

try:
    wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))

    recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

    # Solve reCAPTCHA
    solver = RecaptchaSolver(driver=driver)
    solver.click_recaptcha_v2(iframe=recaptcha_iframe)
except:
    driver.quit()
    exit()


#######################################################################################################

# Click on elements using WebDriverWait
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[1]/div[2]/form/div[4]/div[3]/a'))).click()

wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[1]/select'))).click()
Select(driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[1]/select")).select_by_visible_text("Probate and Family Court")
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[2]/select"))).click()
Select(driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[2]/select")).select_by_visible_text(counties[start_no])

#######################################################################################################

for i in range(start_no, len(counties)):

    # load case list
    case_list = [] # CASE LIST

    download_path = r'D:\Courts'
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    try:
        case_file = open(download_path + r'\case.txt', 'rt')
        case_list = case_file.read().split('\n')
        case_list = [x for x in case_list if x != '']
        case_file.close()
    except:
        case_file = open(download_path + r'\case.txt', 'wt')
        case_file.close()

    try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tab1'))).click()

        # Fill out date fields
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[4]/div/div[2]/form/div[2]/div[1]/div/div[1]/input"))).clear()
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[4]/div/div[2]/form/div[2]/div[1]/div/div[2]/input"))).clear()
        time.sleep(3)

        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[4]/div/div[2]/form/div[2]/div[1]/div/div[1]/input"))).send_keys(start_date)
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[4]/div/div[2]/form/div[2]/div[1]/div/div[2]/input"))).send_keys(end_date)
        time.sleep(3)

        # Click on an option in a dropdown10
        select = Select(driver.find_element(By.XPATH, "/html/body/div[5]/div[4]/div/div[2]/form/div[2]/div[1]/select[1]"))
        select.select_by_index(7)

        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[4]/div/div[2]/form/div[4]/input'))).click()

        # Get page count
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'navigatorLabel')))
        except:
            if i == len(counties) - 1:
                break

            print('\nLoading next county ...')

            driver.find_elements(By.CSS_SELECTOR, '#navigationSectionLeft>li')[1].click() # Search button

            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[2]/select"))).click()
            Select(driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[2]/select")).select_by_visible_text(counties[i + 1])
            time.sleep(2)
            continue

        result = driver.find_element(By.CSS_SELECTOR, '.navigatorLabel>span').text
        total_count = int(result.split(' ')[-1])
        total_pages = (total_count - 1) // 25 + 1
        if total_pages > 4:
            total_pages = 4
        print('total_pages: ', total_pages)

        # Navigate to each page
        for page in range(1, total_pages + 1):
            print('page: ', page)

            if page != 1:
                navigator=driver.find_element(By.CLASS_NAME,'navigator')
                elements=navigator.find_elements(By.TAG_NAME,'a')
                for element in elements:
                    if "Go to next page" in element.get_attribute('title'):
                        element.click()
                        time.sleep(3)
                        break

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tableResults')))
            my_table=driver.find_element(By.CLASS_NAME,'tableResults')
            rows = my_table.find_elements(By.TAG_NAME,'tr')
            row_count = len(rows)
            print('row_count:', row_count)
            for row_num in range(1, row_count):
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tableResults')))
                my_table=driver.find_element(By.CLASS_NAME,'tableResults')
                rows = my_table.find_elements(By.TAG_NAME,'tr')

                # print('row_num:', row_num)
                case_no = rows[row_num].find_elements(By.TAG_NAME, 'td')[3].find_element(By.CSS_SELECTOR, 'span>a>span').text
                if case_no not in case_list:
                    case_list.append(case_no)
                else:
                    continue

                # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#grid\~row-{row_num}\~cell-7')))
                # case_type=driver.find_element(By.CSS_SELECTOR, f'#grid\~row-{row_num}\~cell-7')
                # case_type=case_type.find_element(By.CSS_SELECTOR,f'#grid\~row-{row_num}\~cell-7\$link > span').text
                case_type = rows[row_num].find_elements(By.TAG_NAME, 'td')[6].find_element(By.CSS_SELECTOR, 'span>a>span').text
                print('Case Number:', case_no)
                print('Case Type:  ', case_type)
                if case_type =='Filing of will of deceased no petition':
                    continue

                rows[row_num].find_elements(By.TAG_NAME, 'td')[3].find_element(By.CSS_SELECTOR, 'span>a').click()

                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#titleBar > h1 > ul > li')))

                download_path = r'D:\Courts'
                new_path=driver.find_element(By.CSS_SELECTOR,'#titleBar > h1 > ul > li').text

                # get information
                name = new_path[new_path.index(':') + 2:]
                county_name = ''
                if case_no[:2] in case_no_pfx:
                    for idx in range(0, len(case_no_pfx)):
                        if case_no_pfx[idx] == case_no[:2]:
                            county_name = county_list[idx]
                            break
                probateDate = ''
                dateOfDeath = ''

                try:
                    probateDate = driver.find_element(By.CSS_SELECTOR, '#caseHeader').find_elements(By.TAG_NAME, 'div')[0].find_elements(By.TAG_NAME, 'div')[2].find_elements(By.CSS_SELECTOR, 'ul>li')[1].text
                except:
                    probateDate = ''

                try:
                    dateOfDeath = driver.find_elements(By.CSS_SELECTOR, 'li.ptyPersInfo')[0].text
                except:
                    dateOfDeath = ''

                # output information
                print('Name:        ', name)
                print('DocketNumber:', case_no)
                print('County:      ', county_name)
                print('ProbateDate: ', probateDate)
                print('DateOfDeath: ', dateOfDeath)
                print('')

                # download_path=download_path+'\\'+case_no
                # if not os.path.exists(download_path):
                #     os.mkdir(download_path)

                # Click on other elements as needed
                try:
                    wait.until(EC.presence_of_element_located((By.ID, 'docketInfo')))

                    pdf_table=driver.find_element(By.ID,'docketInfo')
                    for pdfs in pdf_table.find_elements(By.TAG_NAME,'tr'):
                        try:
                            typefile=pdfs.find_element(By.CLASS_NAME,'formattedText').text
                            if typefile=='Petition for Formal Probate' or typefile=='Petition for Informal Probate' or typefile=='Statement of Voluntary Administration':
                                file_name=case_no+'.pdf'
                                file_name=sanitize(file_name)
                                pdfs.find_element(By.CLASS_NAME,'nowrap').click()
                                time.sleep(5)
                                driver.switch_to.window(driver.window_handles[-1])
                                new_file_name = file_name
                                destination_path = os.path.join(download_path, new_file_name)
                                counter = 1
                                while os.path.exists(destination_path):
                                # If the file already exists, add a number to the new filename
                                    file_name, file_extension = os.path.splitext(file_name)
                                    new_file_name = f"{file_name}_{counter}{file_extension}"
                                    destination_path = os.path.join(download_path, new_file_name)
                                    counter += 1

                                os.rename(os.path.join(download_path_keer, 'searchresults.pdf'), destination_path)

                                # save information
                                file_name=case_no+'.txt'
                                file_name=sanitize(file_name)
                                new_file_name = file_name
                                destination_path = os.path.join(download_path, new_file_name)

                                # print('info_file: ', destination_path)
                                info_file = open(destination_path, 'wt')
                                info_file.write(case_no + '\n')
                                info_file.write(county_name + '\n')
                                info_file.write(name + '\n')
                                info_file.write(probateDate + '\n')
                                info_file.write(dateOfDeath)
                                info_file.close()

                                # save case no
                                case_file = open(download_path + r'\case.txt', 'at')
                                case_file.write(case_no + '\n')
                                case_file.close()

                        except:
                            continue
                except:
                    print('Could not find docketInfo. Skip ...')

                driver.back()

                if page != 1:
                    for _ in range(1, page):
                        navigator=driver.find_element(By.CLASS_NAME,'navigator')
                        elements=navigator.find_elements(By.TAG_NAME,'a')
                        for element in elements:
                            if "Go to next page" in element.get_attribute('title'):
                                element.click()
                                time.sleep(3)
                                break

            print("Done for this page... going next page")

        if i == len(counties) - 1:
            break

        print('\nLoading next county ...')

        driver.find_elements(By.CSS_SELECTOR, '#navigationSectionLeft>li')[1].click() # Search button

        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[2]/select"))).click()
        Select(driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div[2]/form/div[2]/div[1]/div[2]/select")).select_by_visible_text(counties[i + 1])
        time.sleep(2)
    except:
        print('ChromeDriver does not work well. Please restart this program.')

        issue_file = open(os.path.join(download_path, 'issue.txt'), 'wt')
        issue_file.write(str(i) + '\n')
        issue_file.write(start_date + '\n')
        issue_file.write(end_date + '\n')
        issue_file.close()

        issue_created = True
        break

driver.close()

print('Done')

# clean the directory
# duplicated files
files = glob.glob(download_path + r'\*_*.pdf')
for file in files:
    try:
        os.remove(file)
    except:
        print("Error while deleting file : ", file)
        exit()

# issue file
if issue_created == False:
    if os.path.exists(issue_file_path):
        try:
            os.remove(issue_file_path)
        except:
            print("Error while deleting file : ", file)
            exit()
else:
    exit()

linkPy.save_data()