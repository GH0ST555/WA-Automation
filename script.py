from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import win32clipboard
from PIL import Image
from io import BytesIO
import random
import tkinter as tk
from tkinter import ttk
import threading
import logging
import pyautogui

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

#Photos Initialization
dir_path = os.path.dirname(os.path.realpath(__file__))
image_folder = os.path.join(dir_path, 'photos')
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder)]

#initialize contact
contact = []
failures = []

with open("contacts.txt", "r") as f:
    for x in f:
        contact.append(x.strip())
    
    

#Selenium Initialization
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")


#function to copy image to clipboard unused
def copy_image_to_clipboard(image_path):
    if not os.path.exists(image_path):
        logging.info(f" Image path not found: {image_path}")
        return

    try:
        image = Image.open(image_path)
        logging.info(f"Opened image: {image_path}")
        logging.info(f"Image mode: {image.mode}")
        
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # Skip BMP header
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        print("✅ Image copied to clipboard.")

    except Exception as e:
        print(f"❌ Failed to copy image: {e}")

def send_message(group_name):
    logging.info(f"Attempting to send to {group_name}")
    logging.info("Trying to find TextBox")
    inp_xpath_search = "//div[@aria-label='Search input textbox']"
    input_box_search = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.XPATH, inp_xpath_search))
    input_box_search.click()
    logging.info("Found TextBox")
    time.sleep(random.uniform(2, 5))

    print("Attempting to enter contact")
    input_box_p_element = '//p[@class ="selectable-text copyable-text x15bjb6t x1n2onr6"]'
    input_box_search_p = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.XPATH, input_box_p_element))
    input_box_search_p.send_keys(group_name)
    print("Found And Entered Contact")
    time.sleep(random.uniform(2, 5))



    #at any point when attempting to push text to the image
    try:
        logging.info("Finding Group")
        selected_contact = driver.find_element(By.XPATH, f"//span[@title='{group_name}']")
        selected_contact.click()
        logging.info("Found Group")
        time.sleep(random.uniform(1, 3))

        logging.info("Finding Text Box")
        inp_xpath = "//div[@aria-label='Type a message' and @role='textbox']//p"
        input_box = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, inp_xpath))
        logging.info("Found Text Box")

        # Type the message


        for image_file in image_files:
            # Copy the image to clipboard
            copy_image_to_clipboard(image_file)

            # Simulate the CTRL+V operation to paste the image
            input_box.send_keys(Keys.CONTROL, "v")
            time.sleep(random.uniform(2, 4))



        logging.info("Finding Send icon after pasting imgs...")
        element = driver.find_element(By.XPATH, '//div[@role="button" and @aria-label="Send"]')



        logging.info("Found Send icon After imgs")
        driver.execute_script("arguments[0].click();", element)
        logging.info("Clicked Send Button")
        time.sleep(random.uniform(1, 3))

        input_box2 = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, inp_xpath))


	# INSERT TEXT HERE ------------------------------------------------------------------
        input_box2.send_keys('for more details :- https://www.facebook.com/share/r/1F7N1Rd3gq/ \n https://www.facebook.com/share/p/1EGTFB6VgF/ \n We are open for Demo/Viewing on Saturdays & Sundays \nContact us https://wa.me/+919745123322 \n')
	#-------------------------------------------------------------------------------------
	
        time.sleep(random.uniform(1, 3))
        driver.find_element(By.XPATH, '//button[@aria-label="Send"]').click()


    except Exception as e:
        failures.append(group_name)
        logging.info(f"Reruting to handle failure. Reason: {e}")
        cancel_search()
        return


def cancel_search():
    """Click the 'Cancel search' button to reset the state."""
    try:
        cancel_btn_xpath = '//button[@aria-label="Cancel search"]'
        cancel_btn = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.XPATH, cancel_btn_xpath))
        cancel_btn.click()
        logging.info("Clicked cancel search to reset.")
        time.sleep(random.uniform(1, 3))
    except Exception as ce:
        logging.info(f" Could not click cancel search: {ce}")


def update_progress_text(count, total):
    """ Update the progress label text """
    progress_label.config(text=f"{count}/{total} contacts processed")

def show_completion_message():
    """ Update the GUI content to show task completion message """
    progress_bar.grid_forget()
    progress_label.grid_forget()

    completion_label = ttk.Label(frame, text="Task Completed!")
    completion_label.grid(row=2, column=0, pady=(10, 10))

    ok_button = ttk.Button(frame, text="OK", command=exit_program)
    ok_button.grid(row=3, column=0, pady=(10, 10))

def exit_program():
    """ Close the Selenium driver and exit the GUI """
    driver.quit()
    root.quit()

def start_automation():
    for idx, y in enumerate(contact, 1):
        try:
            send_message(y)
            progress_var.set(idx)  
            update_progress_text(idx, len(contact))
            root.update_idletasks()
        except RuntimeError as e:
            error_handler(y, str(e))
            return 
    show_completion_message()

    with open("failures.txt", "w") as f:
        if not failures:
            f.write(f"All {len(contact)} contacts received messages successfully. No failures to log.\n")
        else:
            f.write(f"{len(failures)} out of {len(contact)} contacts failed to receive messages.\n\n")
            f.write("Failed contacts:\n")
            for name in failures:
                f.write(name + "\n")


def start_thread():
    threading.Thread(target=start_automation).start()

def confirm_qr_scan():
    qr_label.grid_forget()
    yes_button.grid_forget()
    no_button.grid_forget()
    progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), columnspan=2)
    progress_label.grid(row=3, column=0, sticky=(tk.W, tk.E), columnspan=2, pady=(10, 0))
    update_progress_text(0, len(contact))  # Set the progress to 0 initially
    start_thread()

def decline_qr_scan():
    driver.quit()
    root.quit()

def error_handler(contact_name, error_message):
    """ Update the GUI to show the error message """
    progress_bar.grid_forget()
    progress_label.grid_forget()
    
    error_label = ttk.Label(frame, text=f"Error processing '{contact_name}' please try again")
    error_label.grid(row=2, column=0, pady=(10, 10))
    
    ok_button = ttk.Button(frame, text="OK", command=exit_program)
    ok_button.grid(row=3, column=0, pady=(10, 10))



root = tk.Tk()
root.title("WhatsApp Automation")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

qr_label = ttk.Label(frame, text="Did you scan the QR Code?")
qr_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

yes_button = ttk.Button(frame, text="Yes", command=confirm_qr_scan)
yes_button.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

no_button = ttk.Button(frame, text="No", command=decline_qr_scan)
no_button.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=len(contact))
progress_label = ttk.Label(frame, text="")

frame.columnconfigure(0, weight=1)  
root.mainloop()









#Commented code for sending texts
# text = "Hey, this message automated using python Selenium :)"
# inp_xpath = '//div[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"][@contenteditable="true"][@data-tab="10"]'
# input_box = driver.find_element("xpath",inp_xpath)
# time.sleep(2)
# input_box.send_keys(text + Keys.ENTER)
# time.sleep(2)
# driver.quit()





