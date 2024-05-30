import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk # installing the ttkthemes wrapper to make the program look nicer
import subprocess
import json
import os 
import schedule # used to schedule the running of script automatically
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from price import url_or_item                                                                                  

root = ThemedTk(theme='adapta')
root.title("Price Monitoring")

# Create a list of column labels
column_labels = ["Item", "In stock?", "Description", "Price", "Savings", "Ratings"]

# Create a frame for column labels
label_frame = ttk.Frame(root)
label_frame.pack(pady=10, fill='x')

# Create labels for column headers
label_widgets = []
for col, label_text in enumerate(column_labels):
    label = ttk.Label(label_frame, text=label_text, font=("Arial", 10, "bold"))
    label.grid(row=0, column=col, padx=35, pady=10, sticky='ew')
    label_widgets.append(label)
    
total_columns = len(column_labels)
for col in range(total_columns):
    label_frame.grid_columnconfigure(col, weight=1)  # Set weight=1 for equal distribution

# Create a table frame
table_frame = ttk.Frame(root)
table_frame.pack(pady=20)

# Create a list to store the entry boxes and text boxes
entries = []
outputs = []

# Create the table
for row in range(5):
    row_entries = []
    row_outputs = []
    for col in range(6):
        if col == 0:
            # Create an entry box in the first column
            entry = ttk.Entry(table_frame)
            entry.grid(row=row, column=col, padx=5, pady=5)
            row_entries.append(entry)
        else:
            # Create a text box in the other columns
            output = ttk.Entry(table_frame, state="readonly")
            output.grid(row=row, column=col, padx=5, pady=5)
            row_outputs.append(output)
    entries.append(row_entries)
    outputs.append(row_outputs)

def get_items():
    # Get the input from the first entry box
    items = []  # create a list to store items
    for x in range(5):
        input_text = entries[x][0].get()
        if input_text:
            items.append(input_text)
    return items

def update_output():
    items = get_items()
    for x in range(5):
        input_text = entries[x][0].get()
        if input_text:
            outputs[x][0].configure(state="normal")
            outputs[x][0].delete(0, tk.END)
            outputs[x][0].insert(0, input_text.upper())
            outputs[x][0].configure(state="readonly")
            
    return 'Done'

def start_scraping():
    items = get_items()
    if items:
        price_list = get_price(items)
        #print(price_list)
        for x in range(5):
            input_text = entries[x][0].get()
            if input_text:
                price_found = False
                for item_dict in price_list:
                    if item_dict['item'] == input_text:
                        name = item_dict['title']
                        price = item_dict['price']
                        stock = item_dict['availability']
                        
                        outputs[x][1].configure(state="normal")
                        outputs[x][1].delete(0, tk.END)
                        outputs[x][1].insert(0, name)
                        outputs[x][1].configure(state="readonly")
                        
                        outputs[x][1].configure(state="normal")
                        outputs[x][1].delete(0, tk.END)
                        outputs[x][1].insert(0, name)
                        outputs[x][1].configure(state="readonly")
                        
                        outputs[x][2].configure(state="normal")
                        outputs[x][2].delete(0, tk.END)
                        outputs[x][2].insert(0, price)
                        outputs[x][2].configure(state="readonly")
                        
                        outputs[x][3].configure(state="normal")
                        outputs[x][3].delete(0, tk.END)
                        outputs[x][3].insert(0, item_dict['savings'])
                        outputs[x][3].configure(state="readonly")
                        
                        outputs[x][4].configure(state="normal")
                        outputs[x][4].delete(0, tk.END)
                        outputs[x][4].insert(0, item_dict['ratings'])
                        outputs[x][4].configure(state="readonly")
                        price_found = True
                        break
                if not price_found:
                    outputs[x][2].configure(state="normal")
                    outputs[x][2].delete(0, tk.END)
                    outputs[x][2].insert(0, "Price not found")
                    outputs[x][2].configure(state="readonly")
                    
                    
                    
    
                    
                
        
def get_price(items):
    driver = webdriver.Chrome()
    results = [] # list that holds all dictionaries for each item

    for item in items:
        print(item)
        typa_shii = url_or_item(item)
        print(typa_shii)
        singular = {} # dictionary that contains the details about the item

        if typa_shii == "item":
            driver.get("https://www.amazon.com/")
            wait = WebDriverWait(driver, 10)
            searchbox = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            searchbox.clear()
            searchbox.send_keys(item)
            submit = wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button")))
            submit.click()
            time.sleep(5)

            new = driver.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-no-outline')
            try:
                #print(new.text)
                new.click()
                time.sleep(5)
            except:
                #print(f"error: cannot find price")
                time.sleep(2)
                
            title = driver.find_element(By.ID, 'titleSection')
            if title:
                title = title.find_element(By.ID, 'productTitle')
                title = title.text
                singular['title'] = title
            else:
                singular['title'] = "No title found"

            price_elements = driver.find_elements(By.CSS_SELECTOR, ".a-price")
            for price in price_elements:
                price = price.text
                if "$" in price:
                    price = price.replace('\n', ".")
                    #singular['item'] = price
                    #print(f'Dictionary after adding one item: {singular}')
                    break
                singular['price'] = 'error: cannot find price' #THIS LINE WILL ONLY PRINT IF THE PRICE IS NOT FOUND
                #print(f'No print:: {item}: {results[item]}')
                
            ratings = driver.find_element(By.ID, 'averageCustomerReviews')
            if ratings:
                ratings = ratings.text  
                ratings = ratings.split()
                ratings = ratings[0]
                
            amt_reviews = driver.find_element(By.ID, 'acrCustomerReviewLink')
            if amt_reviews:
                amt_reviews = amt_reviews.text
                
            avaliablity = driver.find_element(By.ID, 'availability')
            avaliablity = avaliablity.text
            if "In Stock" in avaliablity:
                singular['availability'] = "In Stock"
            else:
                singular['availability'] = "Out of Stock"
                

            try:
                savings_div = driver.find_element(By.CSS_SELECTOR, "div[style='padding:5px 0px 5px 0px;']") # finding the div that the savings is in
                if savings_div:
                    savings = savings_div.find_element(By.XPATH, "//*[contains(@id, 'couponText')]") #method for finding savings inside savings_div
                    savings = savings.text
                    print(savings)
            except:
                print("No savings found")
                savings = 'None'
                
            singular['item'] = item
            singular['price'] = price
            print(f'dictionary so far: {singular}')
            singular['savings'] = savings
            singular['ratings'] = f'{ratings} ({amt_reviews})'
                
            results.append(singular) # add dictionary about item to list containing all items

        elif typa_shii == "url":
            driver.get(item)
            
            title = driver.find_element(By.ID, 'titleSection')
            if title:
                title = title.find_element(By.ID, 'productTitle')
                title = title.text
                singular['title'] = title
            else:
                singular['title'] = "No title found"
        
            price_elements = driver.find_elements(By.CSS_SELECTOR, ".a-price")
            for price in price_elements:
                price = price.text
                if "$" in price:
                    price = price.replace('\n', ".")
                    #results[item] = price
                    break
                
            ratings = driver.find_element(By.ID, 'averageCustomerReviews')
            if ratings:
                ratings = ratings.text  
                
            amt_reviews = driver.find_element(By.ID, 'acrCustomerReviewLink')
            if amt_reviews:
                amt_reviews = amt_reviews.text
                
            
            avaliablity = driver.find_element(By.ID, 'availability')
            avaliablity = avaliablity.text
            if "In Stock" in avaliablity:
                singular['availability'] = "In Stock"
            else:
                singular['availability'] = "Out of Stock"

            try:
                savings_div = driver.find_element(By.CSS_SELECTOR, "div[style='padding:5px 0px 5px 0px;']")
                if savings_div:
                    savings = savings_div.find_element(By.XPATH, "//*[contains(@id, 'couponText')]") #method for finding savings inside savings_div
                    savings = savings.text
                    print(savings)
            except:
                print("No savings found")
                savings = 'None'
                
            singular['item'] = item
            singular['price'] = price
            singular['savings'] = savings
            singular['ratings'] = f'{ratings} ({amt_reviews})'
                
            results.append(singular) # add dictionary about item to list containing all items

    driver.quit()
    return results

"""Sets up the scheduler to run everyday at 9am"""
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

schedule.every().day.at("09:00").do(start_scraping)
start_scheduler()


# Create a button to trigger the update
update_button = ttk.Button(root, text="Update", command=update_output)
update_button.pack(pady=10)

# Create a button to start scraping
scrape_button = ttk.Button(root, text="Start Scraping", command=start_scraping)
scrape_button.pack(pady=10)

root.mainloop()
