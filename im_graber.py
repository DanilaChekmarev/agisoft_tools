import os
import cv2
import matplotlib.pyplot as plt


if __name__ == "__main__":

    dir = "D:/testdata/new/inp/new.021"
    files = os.listdir(dir)
    files = [file for file in files if file.find("avi") > 0]
    count = 1
    for file in files:
        path = os.path.abspath(os.path.join(dir, file))
        cap = cv2.VideoCapture(path)
        f = True
        print("---------------->")
        print(file)
        while f:
            f, im = cap.read()
            if f is False:
                break
            im_name = os.path.abspath(os.path.join(dir + "/images/", f"{count:05d}.png"))
            cv2.imwrite(im_name, im)
            count = count + 1