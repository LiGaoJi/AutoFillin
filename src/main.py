import os
from detection import Run
from process import *
import cv2

# TODO add os and waitkey to exit

def main():
    src_path = "src.jpg"
    temp_path = "template/"
    
    templates = Load_temp(temp_path)
    src_img = Load_src(src_path)
    rects = Srcimg_proc(src_img)

    cv2.imshow("rect", rects[0])
   
    numbers = Run(rects[:2], templates)
    print(numbers[0]["id_number"])
    print(numbers[0]["step_number"])

    cv2.waitKey(0)
    input("Press any key to continue...")

main()





