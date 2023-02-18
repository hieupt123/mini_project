import cv2
import numpy as np
from time import time, sleep
import win32gui
import win32ui
import win32con
import mouse

def list_window_name():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(winEnumHandler, None)

def windown_capture():
    w = 1920  # set this
    h = 1080  # set this
    # bmpfilenamename = "out.bmp"  # set this
    # windowname = "Piano Game Classic - Challenge Music Tiles"
    # # windowname = "Anaconda Navigator"
    #
    # hwnd = win32gui.FindWindow(None, windowname)
    # # hwnd = None
    windowname = "Piano Game Classic - Challenge Music Tiles"
    hwnd_target = win32gui.FindWindow(None, windowname)  # used for test

    left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
    w = right - left
    h = bot - top

    win32gui.SetForegroundWindow(hwnd_target)
    hwnd = win32gui.GetDesktopWindow()
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    # save the screenshot
    # dataBitMap.SaveBitmapFile(cDqC, "debug.bmp")

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]
    img = np.ascontiguousarray(img)

    return img

def get_thresh(screenshot):
    img = screenshot.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 135, 255, cv2.THRESH_BINARY)
    return thresh, img

def click(x, y, button='left'):
    mouse.move(x, y, absolute=True)
    mouse.click(button=button)

def click_mouse(thresh):
    x1 = 100
    x2 = 242
    x3 = 390
    x4 = 561
    if thresh[100, x1] == 0:
        click(x1, 420)
        # sleep(0.02)
    elif thresh[100, x2] == 0:
        click(x2, 420)
        # sleep(0.02)

    elif thresh[100, x3] == 0:
        click(x3, 420)
        # sleep(0.02)

    elif thresh[100, x4] == 0:
        click(x4, 420)
        # sleep(0.02)

loop_time = time()
i = 0
while i<100:
    # screenshot = windown_capture()

    thresh, img = get_thresh(windown_capture()[281:526,:])

    # print(thresh[100, 100])
    click_mouse(thresh)
    cv2.imshow("Image", thresh)
    print(f"FPS: {1/(time()-loop_time)} | {time()-loop_time}")
    loop_time=time()
    i+=1

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break