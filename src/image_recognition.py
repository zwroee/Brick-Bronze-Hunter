import cv2
import numpy as np
from PIL import Image,ImageGrab

from io import BytesIO
from PIL import Image as PILImage
import os
import pytesseract

def compare_images(img_dir, precheck_threshold, threshold, scale_percent, debug):

    frame_num = get_frame_num(img_dir)

    curr_screen = cv2.cvtColor(np.array(ImageGrab.grab().convert('RGB')), cv2.COLOR_BGR2RGB)


    for i in range(frame_num):
        
        if i % 1 == 0:

            img = handle_image_extension(img_dir, i)
            img_process = preprocess_image(img)
            img_search = resize_image(img_process, scale_percent)
            
            method = eval("cv2.TM_SQDIFF_NORMED")
            result = cv2.matchTemplate(curr_screen, img_search, method)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            trows,tcols = img_search.shape[:2]

            flag = False

            #gives precheck of a high threshold saves time so in case the pokemon is clearly not the same, we can just move on
            #I haven't calibrated this yet but im hoping to build a cool thing.
            if min_val >= precheck_threshold:
                print("Did not pass precheck.")
                print("min val: ", min_val, " Precheck Val: ", precheck_threshold)
                if debug == True:
                    print_image(min_loc, tcols, trows, curr_screen)
                return False


            if min_val <= threshold:
                flag = True

                #sends out screenshot of what the computer found...
                if debug == True:
                    print_image(min_loc, tcols, trows, curr_screen)

                return flag

    return flag

def print_image(min_loc, tcols, trows, curr_screen):
    print("DEBUG: Printing where computer found the image...")
    top_left = min_loc
    bottom_right = (top_left[0] + tcols, top_left[1] + trows)
    cv2.rectangle(curr_screen, top_left, bottom_right, (0, 0, 255), 2)
    cv2.imshow('output', curr_screen)
    cv2.waitKey(0)

def detect_file_type(image_path):
    try:
        with PILImage.open(image_path) as img:
            fmt = (img.format or '').lower()
            if fmt == 'jpeg':
                fmt = 'jpg'
            return fmt
    except Exception:
        return None

def get_frame_num(image_path):
    file_type = detect_file_type(image_path)
    if file_type:
        #Gifs working were a pain in the ass, so lets break it down to make sure if something fails, we know exactly what.
        if file_type == 'gif':
            gif_image = Image.open(image_path)

            try:
                num_frames = 0
                while True:
                    gif_image.seek(num_frames)
                    num_frames += 1
            except EOFError:
                # Reached the end of the frames
                pass

            return num_frames
                
        elif file_type == 'webp':
            webp_image = Image.open(image_path)

            try:
                num_frames = 0
                while True:
                    webp_image.seek(num_frames)
                    num_frames += 1
            except EOFError:
                # Reached the end of the frames
                pass

            return num_frames


        elif file_type == 'png' or file_type == 'jpg' or file_type == 'tiff' or file_type == 'tif':
            return 1
        
    else:
        print("File type given is not a supported Format! Supported formats: .gif, .webp, .jpeg, .png, .tiff")
        raise Exception

def handle_image_extension(image_path, frame_num):
    file_type = detect_file_type(image_path)
    if file_type:
        #Gifs working were a pain in the ass, so lets break it down to make sure if something fails, we know exactly what.
        if file_type == 'gif':
            #gets gif image
            gif_image = Image.open(image_path)
            try:
                #gets num frames in gif
                num_frames = get_frame_num(image_path)
                #checks if current frame (in function that called it), is here or not
                if frame_num < num_frames:
                    #gets image on gif loaded
                    gif_image.seek(frame_num)
                    #creates a new gif image, which is just the image but converted to RGBA
                    new_gif_image = gif_image.convert("RGBA")
                    #turns it into a webp
                    webp_buffer = BytesIO()
                    new_gif_image.save(webp_buffer, format="WEBP", lossless=True, save_all=True, append_images=[gif_image])
                    webp_buffer.seek(0)
                    #loads it up again, idk if i actually need this bit
                    new_gif_image = Image.open(webp_buffer)
                    print("Checking frame: ",frame_num+1, " of ",num_frames, end="\r")
                    return cv2.cvtColor(np.array(new_gif_image.convert('RGB')), cv2.COLOR_BGR2RGB)
                else:
                    print("A counting error: im gonna be honest idk how this is even possible. If you see this, please screenshot and send to me lol")
                    return 0

                
                #return cv2.cvtColor(np.array(new_gif_image.convert('RGB')), cv2.COLOR_BGR2RGB) 

            except EOFError:
                print("The GIF file given is corrupted, not really a gif, the conversion from .gif to .webp failed, or something else catastrophic is going on.")
                return 0

        elif file_type == 'webp':
            webp_image = Image.open(image_path)
            try:
                num_frames = get_frame_num(image_path)
                
                if frame_num < num_frames:
                    print("Checking frame: ",frame_num+1, " of ",num_frames, end="\r")
                    webp_image.seek(frame_num)
                else:
                    webp_image.seek(0)
                return cv2.cvtColor(np.array(webp_image.convert('RGB')), cv2.COLOR_BGR2RGB)
            
            except EOFError:
                print("The WEBP file given is corrupted, not really a WEBP File, or something else catastrophic is going on.")
                return 0


        elif file_type == 'png' or file_type == 'jpg' or file_type == 'tiff' or file_type == 'tif':
            print("File type is supported, but i suggest using .gif, or .webp")
            return cv2.imread(image_path)
        
    else:
        print("File type given is not a supported Format! Supported formats: .gif, .webp, .jpeg, .png, .tiff")
        raise Exception
    
def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def preprocess_image(image):
    processed_image = image.copy()

    if image.shape[2] == 4:

        alpha_channel = processed_image[:, :, 3]
        processed_image[alpha_channel == 0, :] = [0, 0, 0, 255]

    return processed_image

def get_text_from_screenshot(coords, debug):

    # Configure tesseract path gracefully
    default_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    env_path = os.environ.get('TESSERACT_PATH')
    if env_path and os.path.exists(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
    elif os.path.exists(default_path):
        pytesseract.pytesseract.tesseract_cmd = default_path
    else:
        # Tesseract not available; skip OCR and avoid crashing
        if debug:
            print("Tesseract not found. Set TESSERACT_PATH env var to tesseract.exe. Skipping OCR.")
        return False
    x1 = coords[0]
    y1 = coords[1]
    x2 = coords[2]
    y2 = coords[3]
    
    cropRect = (x1,y1,x2,y2) 
    screenshot = ImageGrab.grab().convert('L').crop(cropRect)
    values = pytesseract.image_to_string(screenshot)
    
    if debug == True:
        print("DEBUG: showing text seeing if we are in battle...")
        #screenshot.show()
        print(values)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        cv2.imshow("Screenshot", img)
        cv2.waitKey(0)


    text = str(values[:values.find("/n")])
    #if "Lv." in text:
    if text:
        return True
    else:
        return False

def is_run_button_visible(run_coords):
    try:
        x = int(run_coords[0])
        y = int(run_coords[1])
        pixel = ImageGrab.grab().load()[x, y]
        r, g, b = pixel[0], pixel[1], pixel[2]
        # Heuristic for blue-tinted Run button
        if b > 120 and b > r + 20 and b > g + 20:
            return True
        return False
    except Exception:
        return False
