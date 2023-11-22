import re
import pathlib
import phonenumbers
import gender_guesser.detector as gender


pattern_1= r'^(?P<last_name>[^,]+),\s*(?P<first_name>[^\s]+)\s*(?P<middle_name>.*)$'
pattern_2 = r'^(?P<last_name>[^,]+),\s*(?P<suffix>\w+)?,\s*(?P<first_name>[^\s]+)\s*(?P<middle_name>.*)$'
class Person:
    def __init__(self):
    # sef information
        self.docketInfo = ''
        self.nameInfo = ''
        self.addrInfo = ''
        self.extraInfo = ''
        self.phoneInfo = ''
        self.emailInfo = ''
        self.gender = gender.Detector()
    # get information
        # base information
        self.key = ''
        self.namePulled = ''
        self.probateCounty = ''
        self.probateState = ''
        self.docketNumber = ''
        self.probateDate = ''
        self.dateOfDeath = ''
        # name information
        self.preffix = ''
        self.firstName = ''
        self.middleName = ''
        self.lastName = ''
        self.suffix = ''
        # Address information
        self.lastAddress = ''
        self.lastCity = ''
        self.lastState = ''
        self.lastZip = ''
        self.phone= ''
        self.email = ''
    def set_docketInfo(self, _docketNo, _probateCounty, fullname, _probateDate, _dateOfDeath):
        self.docketInfo = _docketNo
        self.namePulled = fullname
        self.make_real_name()
        self.key = _docketNo + self.lastName
        #print(self.key)
        self.probateCounty = _probateCounty
        self.docketNumber = _docketNo
        self.probateDate = _probateDate
        self.dateOfDeath = _dateOfDeath
        ###

    def set_pr_nameInfo(self, _nameInfo):
        tempName = _nameInfo.split(':')
        self.nameInfo = (tempName[1]).strip()
        print(">>>>>>>>>>>", self.nameInfo)

        splited_name = self.nameInfo.split(' ')
        split_len = len(splited_name)
        print(split_len)
        if split_len == 2:
            self.firstName = (splited_name[0]).strip()
            self.lastName = (splited_name[1]).strip()
        elif split_len == 3:
            self.firstName = (splited_name[0]).strip()
            self.lastName = (splited_name[2]).strip()
            self.middleName = (splited_name[1]).strip()
        elif split_len == 4:
            self.firstName = (splited_name[0]).strip()
            self.lastName = (splited_name[2]).strip(',')
            self.middleName = (splited_name[1]).strip()
            self.suffix = (splited_name[3]).strip()

        gender = self.gender.get_gender(self.firstName)
        if gender == "male":
            self.preffix = "Mr."
        elif gender == "female":
            self.preffix = "Ms."
        elif gender == "unknown":
            self.preffix= " "
        else:
            self.preffix = " "
    def set_addrInfo(self, _addrInfo):
        t_split_addr = _addrInfo.split(':')
        split_addr = (t_split_addr[1]).split(' ')
        self.extraInfo = _addrInfo
        state_pattern = r"\b[A-Z]{2}\b"
        zip_pattern = r"\b\d{5}\b"
        state_match = re.search(state_pattern, _addrInfo)
        zip_match = re.search(zip_pattern, _addrInfo)
        if state_match:
            self.lastState = state_match.group()
            self.probateState = self.lastState
        if zip_match:
            self.lastZip = zip_match.group()
            self.lastCity = split_addr[len(split_addr) - 3]
        else:
            self.lastCity = split_addr[len(split_addr) - 2]
        
        tStr =''
        for item in split_addr:
            if item == self.lastCity:
                self.lastAddress = tStr
                break
            else:
                tStr = tStr + " " + item
        
       
    def set_pr_addrInfo(self, _addrInfo):
        split_addr = _addrInfo.split(' ')
        self.extraInfo = _addrInfo
        state_pattern = r"\b[A-Z]{2}\b"
        zip_pattern = r"\b\d{5}\b"
        state_match = re.search(state_pattern, _addrInfo)
        zip_match = re.search(zip_pattern, _addrInfo)
        if state_match:
            self.lastState = state_match.group()
        if zip_match:
            self.lastZip = zip_match.group()
            self.lastCity = split_addr[len(split_addr) - 3]
        else:
            self.lastCity = split_addr[len(split_addr) - 2]
        tStr =''
        for item in split_addr:
            if item == self.lastCity:
                self.lastAddress = tStr
                break
            else:
                tStr = tStr + " " + item.strip()
    def set_extraInfo(self, _extraInfo):
        t_extraInfo = (_extraInfo.split(':'))[1]
        self.extraInfo = _extraInfo.strip()
        state_pattern = r"\b[A-Z]{2}\b"
        city_pattern = r"\b[A-Za-z\s]+\b"
        city_match = re.search(city_pattern, _extraInfo)
        state_match = re.search(state_pattern, _extraInfo)
        if state_match:
            self.lastState = state_match.group()
        if city_match:
            self.lastCity = city_match.group()
        ###
    def set_phoneInfo(self, _phoneInfo):
        self.phoneInfo = _phoneInfo
        pattern = r"\d"
        # Find all matches of the pattern in the string
        matches = re.findall(pattern, _phoneInfo)
        # Join the matches into a single string
        digits = ''.join(matches)
        print("digits ====>", digits)
        if len(digits) >= 10:
            formatted_number = digits[0:3] + '-' + digits[3:6] + '-' + digits[6:10] 
        else:
            formatted_number = ''
#        print(digits)
        if len(digits) == 10:
            phone_digits = digits[:10]
        elif len(digits) == 11:
            if digits[0] == '1':
                phone_digits = digits[1:11]
            else:
                phone_digits = digits[0:10]
        else:
            phone_digits = digits

        try:
            parsed_number = phonenumbers.parse(phone_digits, "US")
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        except: 
            print('Non-american type')          
        # Format the parsed number as a telephone number
        print(formatted_number)
        self.phone = formatted_number
        ###
    def set_emailInfo(self, _emailInfo):
        self.emailInfo = _emailInfo
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        # Find the first match of the pattern in the string
        match = re.search(pattern, _emailInfo)
        if match:
            self.email = match.group()
            print("Email found:", self.email)
        else:
            print("No email found.")    
    def set_probateCounty(self, probateCountyInfo):
        pattern = r"(\w+)\s+Division"
        # Search for the pattern in the string
        match = re.search(pattern, probateCountyInfo)
        if match:
            self.probateCounty = match.group(1)
    def isDigit(self, _str):
        pattern = r"\d+"
        # Find all matches of the pattern in the string 
        matches = re.findall(pattern, _str)
        if matches:
            digits = [int(match) for match in matches]
            return False
        else:
            return True
    def make_real_name(self):
        print(self.namePulled)
        splited_name = self.namePulled.split(' ')
        split_len = len(splited_name)
        if split_len == 2:
            self.firstName = (splited_name[1]).strip()
            self.lastName = (splited_name[0]).strip(',')
        elif split_len == 3:
            self.firstName = (splited_name[1]).strip()
            self.lastName = (splited_name[0]).strip(',')
            self.middleName = (splited_name[2]).strip()
        elif split_len == 4:
            self.firstName = (splited_name[2]).strip()
            self.lastName = (splited_name[0]).strip(',')
            self.middleName = (splited_name[3]).strip()
            self.suffix = (splited_name[1]).strip(',')
       
        gender = self.gender.get_gender(self.firstName)
        if gender == "male":
            self.preffix = "Mr."
        elif gender == "female":
            self.preffix = "Ms."
        elif gender == "unknown":
            self.preffix= " "
        else:
            self.preffix = " "