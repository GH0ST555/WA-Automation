from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import win32clipboard
from PIL import Image
from io import BytesIO
import random
import tkinter as tk
from tkinter import ttk
import threading


#Photos Initialization
dir_path = os.path.dirname(os.path.realpath(__file__))
image_folder = os.path.join(dir_path, 'photos')
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder)]

#initialize contact
contact = []
with open("groups.txt", "r") as f:
    for x in f:
        contact.append(x.strip())

#Selenium Initialization
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")





#function to copy image to clipboard
def copy_image_to_clipboard(image_path):
    image = Image.open(image_path)
    
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def send_message(group_name):
    try:
        inp_xpath_search = "//button[@aria-label='Search or start new chat']"
        input_box_search = WebDriverWait(driver, 20).until(lambda d: d.find_element("xpath",inp_xpath_search))
        input_box_search.click()
        time.sleep(2)

        #Locate the p element to type the text in
        input_box_p_element = '//p[@class ="selectable-text copyable-text iq0m558w g0rxnol2"]'
        input_box_search_p = WebDriverWait(driver, 20).until(lambda d: d.find_element("xpath",input_box_p_element))
        input_box_search_p.send_keys(group_name)
        
        time.sleep(2)

        selected_contact = driver.find_element("xpath","//span[@title='"+group_name+"']")
        selected_contact.click()
        for image_file in image_files:
            # Copy the image to clipboard
            copy_image_to_clipboard(image_file)

            # Find the WhatsApp chat input box
            inp_xpath = '//div[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"][@contenteditable="true"][@data-tab="10"]'
            input_box = driver.find_element("xpath",inp_xpath)
            time.sleep(2)
            
            # Simulate the CTRL+V operation to paste the image
            input_box.send_keys(Keys.CONTROL, "v")
            time.sleep(2)

    except Exception as e:
        raise RuntimeError(str(e)) 

    send_btn_xpath = '//div[@class="g0rxnol2"]'
    button = driver.find_element("xpath",send_btn_xpath)
    time.sleep(2)
    button.click()
    time.sleep(10)


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