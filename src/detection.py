import cv2

src_size = (400, 600) # w * h
temp_size = (20, 38)
#distance_thresh = 330

# Go through the pixels 
# Calculate Hamming distance
def CalDistance(img1, img2):
    res = 0
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if img1[i][j] != img2[i][j]:
                res += 1
    return res

# Seperate figures in one given picture
# Return a list filled in figure images
# TODO check the number of contours
def Cut_fig(fig_img):
    gray = cv2.cvtColor(fig_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    digits_dict = {}
    for cnt in contours:
            [x, y, w, h] = cv2.boundingRect(cnt)
            #cv2.rectangle(dst_img, (x, y), (x+w, y+h), (0, 255, 0), 1)
            roi = thresh[y:y+h, x:x+w]
            roismall = cv2.resize(roi, temp_size)   
            # store X-Coordinates and the rect to sort
            digits_dict[x] = roismall
    # sort the figures according to X-Coordinates
    digits_list = sorted(digits_dict.items(), key=lambda x:x[0])

    digits = {}
    for i in range(len(digits_list)):
        digits[i] = digits_list[i][1]

    return digits

# Detect one rect once
# Return a dictionary for id_number and step_number
# TODO give it a function to detect numbers
def Detect(rect, templates):
    if rect.shape[0] not in range(45, 55):
        print("incorrect rect height: " + str(rect.shape[0]))

    id_img = rect[:int(rect.shape[0]/2) , :81]
    step_img = rect[int(rect.shape[0]/2): , :64]

    # cv2.imshow("id_img", id_img)
    # cv2.imshow("step_img", step_img)

    # Cut figures
    id_figures = Cut_fig(id_img)
    step_figures = Cut_fig(step_img)

    # print("id_figures len: " + str(len(id_figures)))
    # print("step_figures len: " + str(len(step_figures)))
    
    # Store detected numbers
    id_number = ""
    step_number = ""

    # Detect id_numbers
    for i in range(len(id_figures)):
        min_distance = temp_size[0] * temp_size[1]
        index = 0
        for j in range(len(templates)):
            k = CalDistance(id_figures[i], templates[j])
            if k < min_distance:
                min_distance = k
                index = j

        id_number += str(index)
    if len(id_number) != 9:
        print("incorrect id_number: " + id_number + " " + str(len(id_number)) )

    # Detect step_numbers
    for i in range(len(step_figures)):
        min_distance = temp_size[0] * temp_size[1]
        index = 0
        for j in range(len(templates)):
            k = CalDistance(step_figures[i], templates[j])
            if k < min_distance:
                min_distance = k
                index = j

        step_number += str(index)
    if len(step_number) not in [3, 4, 5]:
        print("incorrect step_number: " + step_number + " " + str(len(step_number)))  

    # dictionary whose first key is "id_number" and the second is "step_number"
    return dict([("id_number", eval(id_number) ) , ("step_number", eval(step_number) )  ])

# Overall detection function
# Param1: divided rectangles
# Param2: template figures
def Run(rects, templates):
    if len(templates) != 10:
        print("invalid template length: " + str(len(templates))) 
    # Store detected numbers, each element is a dict
    numbers = []

    for i in range(len(rects)):
        numbers.append( Detect(rects[i], templates) )

    print("numbers length: " + str(len(numbers) ) )

    return numbers