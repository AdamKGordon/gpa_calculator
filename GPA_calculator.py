def input_0(print_str):
    try:
        val = int(raw_input(print_str))
    except:
        val = 0
    if val == "":
        val = 0

    return val

def input_four_unit(print_str):
    four_unit_courses = raw_input(print_str)
    #print(four_unit_courses[:1])
    #print(type(four_unit_courses[:1]))
    #print(len(four_unit_courses[:1]))
    if four_unit_courses[:1] in ["y","Y",1,"yes","Yes"]:
        four_unit_courses = 1
    else:
        four_unit_courses = 0

    return four_unit_courses

gd = {  12.0:"A+",
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

gd2 = { 12.0:4.0,
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


total_units = 0
total_3_unit_courses = 0
total_4_unit_courses  = 0
total_grade_points_12 = 0
total_grade_points_4 = 0
total_courses = 0
four_gpa   = 0
twelve_gpa = 0
twelve_gpa_div_by_three = 0


four_unit_courses = input_four_unit("Do you have 4 unit courses? (y/n): ")

print("What is the amount of... that you achieved?:")
for mark in range(12,0,-1):
    num_of_course_3 = input_0("{} 3 Unit Courses: ".format(gd[mark]))
    if four_unit_courses:
        num_of_course_4 = input_0("{} 4 Unit Courses: ".format(gd[mark]))
    else:
        num_of_course_4 = 0

    total_units = num_of_course_3*3.0 + num_of_course_4*4.0 + total_units
    total_3_unit_courses = num_of_course_3 + total_3_unit_courses
    total_4_unit_courses = num_of_course_4 + total_4_unit_courses
    total_grade_points_12 = (num_of_course_3*3.0 + num_of_course_4*4.0)*mark + total_grade_points_12
    total_grade_points_4 = (num_of_course_3*3.0 + num_of_course_4*4.0)*gd2[mark] + total_grade_points_4
    total_courses = num_of_course_3 + num_of_course_4 + total_courses

four_gpa   = total_grade_points_4  / total_units
twelve_gpa = total_grade_points_12 / total_units
twelve_gpa_div_by_three = twelve_gpa / 3.0
gpa_miscalculation_diff = four_gpa - twelve_gpa_div_by_three

print(" ")
print("total_units: {}".format(total_units))
print("total_3_unit_courses: {}".format(total_3_unit_courses))
print("total_4_unit_courses: {}".format(total_4_unit_courses))
print("total_grade_points_12: {}".format(total_grade_points_12))
print("total_grade_points_4: {}".format(total_grade_points_4))
print("total_courses: {}".format(total_courses))

print("four_gpa: {}".format(four_gpa))
print("twelve_gpa: {}".format(twelve_gpa))
print("twelve_gpa_div_by_three: {}".format(twelve_gpa_div_by_three))
print("Properly converting your GPA gained you: {} GPA points".format(gpa_miscalculation_diff))
print(" ")

