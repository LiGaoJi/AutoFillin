import cv2
from os.path import join, dirname
from os import getcwd
from os import listdir
from process import *
from detection import DetecRun
from excel import XlsRun

# last directory
last_dir = dirname(getcwd())
# source picture directory
src_dir = join(last_dir, "screenshots")
# template figures directory
temp_dir = join(last_dir, "template")
# excel directory
xls_dir = join(last_dir, "xls")
# result excel path
# result_path = join(last_dir, "result", "result.xlsx")

def main():
#   Notice no chinese path names!!!
#   source pictures 
    if len(listdir(xls_dir)) == 0:
        print("No xlsx file found.")
        input("Press ENTER to exit")
        exit()
    elif len(listdir(xls_dir)) > 1:
        print("More than 1 xlsx file found.")
        input("Press ENTER to exit")
        exit()
    if len(listdir(src_dir)) == 0:
        print("No picture found.")
        input("Press ENTER to exit")
        exit()

    src_paths = []
    for path in listdir(src_dir):
        src_paths.append(join(src_dir, path))

    xls_path = join(xls_dir, listdir(xls_dir)[0])

    templates = Load_temp(temp_dir)
    
    numbers_dict = []

    # index = 3
    for i in range(len(src_paths)):
        src_img = Load_src(src_paths[i])
        rects = Srcimg_proc(src_img)
        
        # cv2.imshow("rect", rects[index])
    
        numbers_dict += DetecRun(rects, templates)
                   
        # print("rects length: " + str(len(rects)))
        # print(numbers[0]["id_number"])
        # print(numbers[0]["step_number"])
    # print(numbers_dict)
    numbers = []   

    for element in numbers_dict:
        numbers.append(list(element.values()))
    # print(numbers)
    for element in numbers:
        print("id_number:" + str(element[0]) + "  step_number:" + str(element[1]) )

    if(len(numbers) == 0):
        print("Blank number set, please check your files.")
        print("Or get contact with the author.")
        input("Press ENTER to exit")
        exit()     

    XlsRun(xls_path, "Sheet1", numbers)
    # XlsRun(numbers, xls_path, result_path)         
    # cv2.waitKey(0)
    input("Press ENTER to continue...")

main()

