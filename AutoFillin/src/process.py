import cv2

# Define the fixed size
src_size = (800, 1600) # w * h
temp_size = (28, 28)

# Divide source image into rectangles
def Srcimg_proc( src_img ):
    if src_img.shape != src_size:
        src_img = cv2.resize(src_img, src_size)
    print("src_shape:" + str(src_img.shape))

    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow("binary", binary)
    # Find coutours. Return 2 param, we need the first
    contours = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    dis = src_img.copy()
    # Record Y-coordinates of each rectanlge
    ys = []
    for cnt in contours:
        # Detect the heart-shaped pattern on the right
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if area > 1500 and x > 700:  
            # print(area)          
            cv2.rectangle(dis, (x, y), (x+w, y+h), (0, 255, 0), 2)
            ys.append(int(y+h/2))
    ys.reverse()

    # Height of each rectangle
    h = int(ys[1] - ys[0])

    # Store every part that's been seperated
    rects = []
    
    # TODO solve the edge of the first and the last rect
    for i in range(len(ys) - 1):
        # The Y-coordinate of the left top point of a rect
        y = int((ys[i + 1] + ys[i]) / 2)
        # Handle the first rect
        if i == 0:
            if y-h < 0:
                rects.append(dis[:y, 217:375])
            else:
                # cv2.rectangle(dis, (0, y-h), (0+dis.shape[1], y), (0, 0, 255), 2)
                rects.append(dis[y-h:y, 217:375])
        # cv2.rectangle(dis, (0, y), (0 + dis.shape[1], y + h), (0, 0, 255), 2)
        # check the last rect
        if y + h > dis.shape[0]:
            rects.append( dis[y:, 217:375] )
        else:
            rects.append( dis[y:y+h, 217:375])

    # cv2.imshow("dis", dis[:, :])

    return rects

# Load template figures
# Template figures must be sorted
 
def Load_temp(file_path):
    # Numbers of images
    fig_num = 10;
    # Store template figures
    templates = []

    # Load templates
    for i in range(fig_num):
        img = cv2.imread(file_path + "//" + str(i) + ".png")
        if img.shape != temp_size:
            img = cv2.resize(img, temp_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)[1]
        templates.append( img )
    #print(len(templates))
    #print(templates[0].shape)
    return templates

# Load one source image once and resize
def Load_src(img_path):
    img = cv2.imread(img_path)

    if img.shape != src_size:
        cv2.resize(img, src_size)
    return img

