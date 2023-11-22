import os
import re
import pytesseract
from PIL import Image 
from pytesseract import pytesseract 
from pdf2image import convert_from_path
import preprocess
import personType
import toExcel
from difflib import SequenceMatcher


def save_data():
    img_dir_path = r'D:\Courts'
    entries = preprocess.load_pdf_list(img_dir_path)
    img_list = preprocess.get_all_img_files(img_dir_path)
    for index in entries:
        preprocess.convert_pdf2img(index)

    col = 1

    my_sheet = toExcel.MyXlsheet('./data.xlsx', 'test')
    header =['DecdKey', 'DecdNamePulled', 'ProbateCounty', 
            'ProbateState', 'DocketNumber', 'ProbateDate', 
            'DateOfDeath', 'DecdPrefix', 'DecdFirstName', 
            'DecdMiddleName', 'DecdLastName',
            'DecdSuffix', 'DecdLastAddress', 'DecdLastCity', 
            'DecdLastState', 'DecdLastZip', 'PRPrefix',
            'PRFirstName', 'PRMiddleName', 'PRLastName',
            'PRSuffix', 'PRAddress', 'PRCity',
            'PRState', 'PRZip', 'PRPhone1', 'PREmail']

    for i in range(0, 27):
        my_sheet.Write(0, i, header[i])

    
    for img_item_path in img_list:
        split_tup = os.path.splitext(img_item_path)
        file_name = split_tup[0]
        textFile_name = file_name + '.txt'
        try:
            textFile = open(textFile_name, "r")
        except:
            print("process ended")
            my_sheet.Save()
            return
        docketNumber = (textFile.readline()).strip()
        probateCounty = (textFile.readline()).strip()
        fullName = (textFile.readline()).strip()
        probateDate = (textFile.readline()).strip()
        dateOfDeath = (textFile.readline()).strip()
        print(">>>>>>>>>>", docketNumber, " ", fullName, " ", probateDate, " ", dateOfDeath)
        textFile.close()
        
        decedent = personType.Person()
        petitioner = personType.Person()
        decedent.set_docketInfo(docketNumber, probateCounty, fullName, probateDate, dateOfDeath)
        
        img = Image.open(img_item_path) 
        text = pytesseract.image_to_string(img)
        sift_text = []
        lined_text0 = text.split('\n')
        
        print(len(lined_text0))
        decedent_start_index = -1
        petitioner_start_index = -1
        petitioner_end_index = -1
        decedent_name_line = ''


        for index in range(0, len(lined_text0)):
            tempstr = lined_text0[index]
            #print(tempstr)
            if 'Decedent:' in tempstr:
                decedent_start_index = index
                print("Decedent index1: ", index)
                continue
            if 'Information about the Petitioner' in tempstr:
                petitioner_start_index = index
                print("Decedent index2: ", index)
                continue
            if '3.' in tempstr:
                petitioner_end_index = index
                print("Decedent index3: ", index)
                break 
        if petitioner_end_index == -1:
            petitioner_end_index = len(lined_text0)
            print('>>>>>>', petitioner_end_index)   
        
        probate_county =''
        decedent_suffix = ''
        decedent_ageAtDeath = 0
        decedent_street_addr =''
        decedent_city = ''
        decedent_state = ''
        decedent_zip_code = ''
        decedent_address_info = ''
        decedent_domiciled_in = ''
        
        petitioner_addr_info =''
        petitioner_name_line = ''
        petitioner_phone_info = ''

        
        if decedent_start_index > 0:
            if petitioner_start_index > 0:
                for index in range(decedent_start_index):
                    if 'Division' in lined_text0[index]:
                        string = lined_text0[index]
                        decedent.set_probateCounty(string)
                    break

                for index in range(decedent_start_index, petitioner_start_index):
                    if 'Name:' in lined_text0[index]:
                        decedent_name_line = lined_text0[index]
                        ### get some infromation from decedent_name_line
                        #print(decedent_name_line)
                        continue
                    if 'Domicile at death:' in lined_text0[index]:
                        decedent_address_info = lined_text0[index]
                        print(">>> decedent address info >>> ", decedent_address_info)
                        # TODO : add some function to get detailed information from decendent_address_info
                        decedent.set_addrInfo(decedent_address_info)
                        continue
                    if 'Street Address:' in lined_text0[index]:
                        decedent_address_info = lined_text0[index]
                        decedent.set_addrInfo(decedent_address_info)
                        print(">>> decedent address info >>>", decedent_address_info)
                        continue
                    if 'The Decedent was domiciled in:' in lined_text0[index]:
                        decedent_domiciled_in = lined_text0[index]
                        decedent.set_extraInfo(decedent_domiciled_in)
                        print("decedent_domicled_in:", decedent_domiciled_in)
                        break
                for index in range(petitioner_start_index, petitioner_end_index):
                    if 'Name:' in lined_text0[index]:
                        petitioner_name_line = lined_text0[index]
                        print(">>>>>>>>>>>>>>>>", petitioner_name_line)
                        petitioner.set_pr_nameInfo(petitioner_name_line)
                        petitioner_addr_info = lined_text0[index + 2]
                        petitioner.set_pr_addrInfo(petitioner_addr_info)
                        ### get some infromation from decedent_name_line
                        print(decedent_name_line)
                        continue
                    if '#:' in lined_text0[index]:
                        petitioner_phone_info = lined_text0[index]
                        petitioner.set_phoneInfo(petitioner_phone_info)
                        petitioner.set_emailInfo(petitioner_phone_info) 
                        break               
        result = []
        result.append(decedent.key)
        result.append(decedent.namePulled)
        result.append(decedent.probateCounty)
        result.append(decedent.probateState)
        result.append(decedent.docketNumber)
        result.append(decedent.probateDate)
        result.append(decedent.dateOfDeath)
        result.append(decedent.preffix)
        result.append(decedent.firstName)
        result.append(decedent.middleName)
        result.append(decedent.lastName)
        result.append(decedent.suffix)
        result.append(decedent.lastAddress)
        result.append(decedent.lastCity)
        result.append(decedent.lastState)
        result.append(decedent.lastZip)
        result.append(petitioner.preffix)
        result.append(petitioner.firstName)
        result.append(petitioner.middleName)
        result.append(petitioner.lastName)
        result.append(petitioner.suffix)
        result.append(petitioner.lastAddress)
        result.append(petitioner.lastCity)
        result.append(petitioner.lastState)
        result.append(petitioner.lastZip)
        result.append(petitioner.phone)
        result.append(petitioner.email)
    
        print(">>>> DecdKey: ", decedent.key)
        print(">>>> DecdNamePulled: ", decedent.namePulled)
        print(">>>> ProbateCounty: ", decedent.probateCounty)
        print(">>>> ProbateState: ", decedent.probateState)
        print(">>>> DocketNumber: ", decedent.docketNumber)
        print(">>>> ProbateDate: ", decedent.probateDate)
        print(">>>> DateOfDeath: ", decedent.dateOfDeath)
        print(">>>> DecdPrefix: ", decedent.preffix)
        print(">>>> DecdFirstName: ", decedent.firstName)
        print(">>>> DecdMiddleName: ", decedent.middleName)
        print(">>>> DecdLastName: ", decedent.lastName)
        print(">>>> DecdSuffix: ", decedent.suffix)
        print(">>>> StreetAddress: ", decedent.lastAddress)
        print(">>>> DecdLastCity: ", decedent.lastCity)
        print(">>>> DecdLastState: ", decedent.lastState)
        print(">>>> DecdLastZip: ", decedent.lastZip)

        print(">>>> PRPrefix: ", petitioner.preffix)
        print(">>>> PRFirstName: ", petitioner.firstName)
        print(">>>> PRMiddleName: ", petitioner.middleName)
        print(">>>> PRLastName: ", petitioner.lastName)
        print(">>>> PRSuffix: ", petitioner.suffix)
        print(">>>> PRAddress ", petitioner.lastAddress)
        print(">>>> PRCity: ", petitioner.lastCity)
        print(">>>> PRState: ", petitioner.lastState)
        print(">>>> PRZip: ", petitioner.lastZip)
        print(">>>> PRPhone: ", petitioner.phone)
        print(">>>> PREmail: ", petitioner.email)

        # make xl sheet header

        
        for i in range(0, 27):
            my_sheet.Write(col, i, result[i])
        col = col + 1
    my_sheet.Save()
    print("Process ended")

#save_data()