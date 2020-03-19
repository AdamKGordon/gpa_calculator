import mechanize
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
import html2text
import time

# TODO: CLEAN UP CODE!

class Grade:
    def __init__(self, name, link, term, grade, units):
        self.name = name
        self.link = link 
        self.term = term
        self.grade = grade
        self.units = units

def get_semster_ordered_list(grade_list):
    semster_set = set()
    year_set    = set()
    for grade in grade_list:
            semster_set.add(grade.term)
            year_set.add(int(grade.term[:4]))
    
    # TODO: order the list
    months_ordered_list    = ["Winter", "Spring/Summer", "Fall"]
    years_ordered_list     = list(year_set)
    years_ordered_list.sort()
    #print(str(years_ordered_list))
    semester_ordered_list  = []
    semester_list          = list(semster_set)

    for year in years_ordered_list:
        for month in months_ordered_list:
            for sem in semester_list:
                #print(str(year)+" "+sem)
                if (sem == str(year)+" "+month):
                    semester_ordered_list.append(sem)

    return semester_ordered_list



def print_grade_list(grade_list):
    for grade in grade_list:
        print("Name:  "+ grade.name)
        #print("Link:  "+ grade.link)
        print("Term:  "+ grade.term)
        print("Grade: "+ grade.grade)
        print("Units: "+ grade.units + "\n")

letter_grades_list = ["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-"]

gd_12_to_letter = {  12.0:"A+",
        11.0:"A",
        10.0:"A-",
        9.0:"B+",
        8.0:"B",
        7.0:"B-",
        6.0:"C+",
        5.0:"C",
        4.0:"C-",
        3.0:"D+",
        2.0:"D",
        1.0:"D-"} # grade_dict mcmaster to letter grade

gd_letter_to_12 = {"A+": 12,
        "A":  11,
        "A-": 10,
        "B+": 9,
        "B":  8,
        "B-": 7,
        "C+": 6,
        "C":  5,
        "C-": 4,
        "D+": 3,
        "D":  2,
        "D-": 1} # grade_dict mcmaster to letter grade

gd_4_to_12 = { 12.0:4.0,
        11.0:3.9,
        10.0:3.7,
        9.0:3.3,
        8.0:3.0,
        7.0:2.7,
        6.0:2.3,
        5.0:2.0,
        4.0:1.7,
        3.0:1.3,
        2.0:1.0,
        1.0:0.7} # grade_dict_2 mcmaster to 4.0 scale (https://gradecalc.info/ca/on/mcmaster/gpa_calc.pl)
gd_letter_to_4 = { "A+":4.0,
        "A":3.9,
        "A-":3.7,
        "B+":3.3,
        "B":3.0,
        "B-":2.7,
        "C+":2.3,
        "C":2.0,
        "C-":1.7,
        "D+":1.3,
        "D":1.0,
        "D-":0.7} # grade_dict_2 mcmaster to 4.0 scale (https://gradecalc.info/ca/on/mcmaster/gpa_calc.pl)


def slep(seconds, read):
    while seconds:
        if read:
            print("Sleeping... " + str(seconds))
        time.sleep(1) # Delay for 1 minute (60 seconds).
        seconds -= 1

def find_indicies(string, match_string):
    # returns first and end index (end not inclusive)
    start_idx = string.find(match_string) + len(match_string)
    tmp_idx   = start_idx
    while(string[tmp_idx] != "<"):
        tmp_idx += 1

    end_idx = tmp_idx
    return start_idx, end_idx

def get_cell_text(string, match_string):
    start, finish = find_indicies(response_html, match_string)
    return string[start:finish]

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open('https://epprd.mcmaster.ca/psp/prepprd/?cmd=login&languageCd=ENG&')

# View available forms
#for f in br.forms():
#    print("" + str(f))

# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=0)

# User credentials
#print(str(br.form))

users_student_name = input("Enter your Student Name (e.g smithj6): ")
users_password     = input("Enter your Password: ")
br.form['userid']  = users_student_name
br.form['pwd']     = users_password

# Login
br.submit()

site1 = 'https://epprd.mcmaster.ca/psp/prepprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'
site2 = 'https://csprd.mcmaster.ca/psp/prcsprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES_2.SSS_MY_CRSEHIST.GBL?pts_Portal=EMPLOYEE&pts_PortalHostNode=EMPL&pts_Market=GBL'
site3 = 'https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES_2.SSS_MY_CRSEHIST.GBL?pts_Portal=EMPLOYEE&pts_PortalHostNode=EMPL&pts_Market=GBL&PortalActualURL=https%3a%2f%2fcsprd.mcmaster.ca%2fpsc%2fprcsprd%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES_2.SSS_MY_CRSEHIST.GBL%3fpts_Portal%3dEMPLOYEE%26pts_PortalHostNode%3dEMPL%26pts_Market%3dGBL&PortalContentURL=https%3a%2f%2fcsprd.mcmaster.ca%2fpsc%2fprcsprd%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES_2.SSS_MY_CRSEHIST.GBL&PortalContentProvider=SA&PortalCRefLabel=My%20Course%20History&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fcsprd.mcmaster.ca%2fpsp%2fprcsprd%2f&PortalURI=https%3a%2f%2fcsprd.mcmaster.ca%2fpsc%2fprcsprd%2f&PortalHostNode=SA&NoCrumbs=yes&PortalKeyStruct=yes'
response = br.open(site3)
response_html = response.read().decode('utf-8')
num_courses = response_html.count("id='CRSE_TERM$")
if num_courses == 0:
    print("Try Again: Bad username/password combination (or deprecated code), exiting...")
    slep(3,0)
    exit()
    

#print(response_html)
#out_file = "adam_test.txt" 
#f = open(out_file,"w")
#f.write(response_html) # writes course history page into out_file
find_list = ['id="CRSE_NAME{}">', 
             'id="CRSE_LINK{}">', 
             'id="CRSE_TERM{}">', 
             'id="CRSE_GRADE{}">', 
             'id="CRSE_UNITS{}">']


#y=response_html.find("id='CRSE_NAME$0'>'")
#y=response_html.find("id='CRSE_TERM$0'>")
#print(y)
idx = 0
tmp_list = []
while(idx<num_courses):
    name   = get_cell_text(response_html, "id='CRSE_NAME${}'>".format(idx))
    link   = get_cell_text(response_html, "id='CRSE_LINK${}'>".format(idx))
    term   = get_cell_text(response_html, "id='CRSE_TERM${}'>".format(idx))
    grades = get_cell_text(response_html, "id='CRSE_GRADE${}'>".format(idx))
    units  = get_cell_text(response_html, "id='CRSE_UNITS${}'>".format(idx))
    tmp = Grade(name,link,term,grades,units)
    tmp_list.append(tmp)
    idx += 1
grade_list = tmp_list
# print_grade_list(tmp_list)

total_units=0
mac_grade_points=0
mac_grade_points=0
four_point_o_grade_points = 0

for grade in grade_list:
    if (grade.grade not in letter_grades_list):
        #print("<>"+grade.grade)
        #print("<<>>" +grade.units[0])
        continue
    total_units += int(grade.units[0])
    mac_grade_points += int(grade.units[0]) * gd_letter_to_12[grade.grade]
    four_point_o_grade_points += int(grade.units[0]) * gd_letter_to_4[grade.grade]

mac_avg  = float(mac_grade_points) / total_units
mac_avg_div_3  =  mac_avg / 3.0
four_avg = float(four_point_o_grade_points) / total_units

#print("\nResults")
#print("4.0 GPA points gained by converting properly: {}".format(round(four_avg-mac_avg_div_3),4))
#print("Num Courses:   {}".format(num_courses))
#print("Total Units:   {}".format(total_units))
#print("12.0 Avg:      {}".format(round(mac_avg,4)))
#print("Incorrectly Calculated 4.0 Avg:  {}".format(round(mac_avg_div_3,4)))
#print("Correctly Calculated 4.0 Avg:    {}".format(round(four_avg,4)))
#print("\nResults")
print("4.0 GPA points gained by converting properly: {:.4f}".format(four_avg-mac_avg_div_3))
print("Num Courses:   {}".format(num_courses))
print("Total Units:   {}".format(total_units))
print("12.0 Avg:     {:.4f}".format(mac_avg))
print("Incorrectly Calculated 4.0 Avg: {:.4f}".format(mac_avg_div_3))
print("Correctly Calculated 4.0 Avg:   {:.4f}\n".format(four_avg))

if(input('Enter "y" to see your average for a range of semsters or anything else to exit: ')!="y"):
    print("Exiting")
    slep(2,0)
    exit()

semster_ordered_list = get_semster_ordered_list(grade_list)
tmp_idx=1
for sem in semster_ordered_list:
    print(str(tmp_idx) +". " +sem)
    tmp_idx += 1

in_str = input("Which sems to average (format: start-end eg, 2-6): ")
valid = (len(in_str.split("-")) == 2)
while not valid: 
    print("Bad input, try again")
    in_str = input("Which sems to average (format: start-end eg, 2-6): ")
    valid = (len(in_str.split("-")) == 2)


start_sem = int(in_str.split("-")[0])
final_sem = int(in_str.split("-")[1])
sem_sub_list = semster_ordered_list[start_sem-1:final_sem+1]
#print(str(sem_sub_list))
# calc avearger within range of dates only
###################################################################
total_units=0
mac_grade_points=0
mac_grade_points=0
four_point_o_grade_points = 0
sub_num_courses = 0
for grade in grade_list:
    if (grade.grade not in letter_grades_list or grade.term not in sem_sub_list):
        #print("<>"+grade.grade)
        #print("<<>>" +grade.units[0])
        continue
    total_units += int(grade.units[0])
    mac_grade_points += int(grade.units[0]) * gd_letter_to_12[grade.grade]
    four_point_o_grade_points += int(grade.units[0]) * gd_letter_to_4[grade.grade]
    sub_num_courses += 1

mac_avg  = float(mac_grade_points) / total_units
mac_avg_div_3  =  mac_avg / 3.0
four_avg = float(four_point_o_grade_points) / total_units

print("\n4.0 GPA points gained by converting properly: {:.4f}".format(four_avg-mac_avg_div_3))
print("Num Courses:   {}".format(sub_num_courses))
print("Total Units:   {}".format(total_units))
print("12.0 Avg:     {:.4f}".format(mac_avg))
print("Incorrectly Calculated 4.0 Avg: {:.4f}".format(mac_avg_div_3))
print("Correctly Calculated 4.0 Avg:   {:.4f}".format(four_avg))
###################################################################

input("\nHit enter to exit\n")
