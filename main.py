import datetime
import json
import os
import random
import time
from selenium import webdriver  # Google Chrome driver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Loading URL
from selenium.webdriver.common.by import By  # HTML Identifiers
from selenium.webdriver.support.select import Select

USER_FIELD_NAME = "UserLogin"  # HTML identifier
PASSWORD_FIELD_NAME = "UserPassword"  # HTML identifier
SUBMIT_FIELD_NAME = "df"  # HTML identifier
DIRECTORY_URL = "https://mymustangs.milton.edu/student/directory/"

VALUE_ALL = "19611C3D1D020E04070A"
VALUE_2023 = "7E027D7A2B0A0A1900"
VALUE_2024 = "7E027D7D2B0A0A1900"
VALUE_2025 = "7E027D7C2B0A0A1900"
VALUE_2026 = "7E027D7F2B0A0A1900"

chrome_options = Options()
chrome_options.add_argument("--window-size=950,800")
# chrome_options.add_argument("--headless")

service = Service(executable_path="/Users/bryansukidi/Desktop/CS Projects/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(3)

class Student:
    def __init__(self, name, image_url, image_path):
        self.name = name
        self.image_url = image_url
        self.image_path = image_path

    def __repr__(self):
        return f"Student: {self.name} \nImage Path: {self.image_path}"

def main():
    quiz()

def scrape_student_data():
    pass
    # post_login() # Login to myMilton
    # open_student_directory(VALUE_2025) # Open the student directory page
    #
    # names = scrape_names() # Grab all student names
    # image_urls = scrape_image_urls() # Grab all student image URLS
    # save_image_pngs(image_urls, "2025") # Save student image URLS to PNGs in assets folder
    #
    # students = [Student(name, image_url, f"assets/2025/{idx}-profile.png") for idx, (name, image_url) in enumerate(
    # zip(names, image_urls))] dump_student_data(students, "students_2025.json")

def quiz():
    with open("students_2025.json", "r") as f:
        students = [Student(student["name"], student["image_url"], student["image_path"]) for student in json.load(f)]

    for question in range(5):
        correct_student = random.choice(students)

        print(f"Question {question + 1}: {correct_student.image_url}")

        choices = [correct_student.name, random.choice(students).name,
                   random.choice(students).name, random.choice(students).name]
        random.shuffle(choices)

        letters = ['a', 'b', 'c', 'd']
        for idx, choice in enumerate(choices):
            print(f"{letters[idx]}) {choice}")

        answer = letters.index(input("Answer: "))

        if choices[answer] == correct_student.name:
            print("Correct!")
        else:
            break

def format_name(name):
    name = name.split(" - ")[0]
    name = name.split(", ")
    return name[1] + ", " + name[0]

def load_login():
    if os.path.exists('login_info.json'):
        with open('login_info.json', 'r') as login_info:
            login_info = json.load(login_info)
        return login_info['username'], login_info['password']
    else:
        return input("Username: "), input("Password: ")

def post_login():
    # Grab login credentials
    USERNAME, PASSWORD = load_login()

    # Open the myMilton login website
    driver.get("https://mymustangs.milton.edu/student/index.cfm?")
    print("Accessing Website: ", driver.title)

    # Wait 0.5 seconds for website loading time (Selenium is asynchronous)
    driver.implicitly_wait(0.5)

    # Post username to username text box
    print(">>> Entering USERNAME")
    username_field = driver.find_element(by=By.NAME, value=USER_FIELD_NAME)
    username_field.send_keys(USERNAME)

    print(">>> Entering PASSWORD")
    # Post password to password text box
    password_field = driver.find_element(by=By.NAME, value=PASSWORD_FIELD_NAME)
    password_field.send_keys(PASSWORD)

    print(">>> Submitting FORM")
    # Click submit button
    submit_button = driver.find_element(by=By.NAME, value=SUBMIT_FIELD_NAME)
    submit_button.click()

    # Validate Login
    print(">>> Validating Login")
    print("Accessing Website: ", driver.title)

def open_student_directory(value):
    driver.get(DIRECTORY_URL)

    # Select(driver.find_element(By.ID, value="school")).select_by_value("19611C3D1D020E04070A")
    Select(driver.find_element(By.ID, value="class")).select_by_value(value)
    submit_button = driver.find_element(by=By.NAME, value="s")
    submit_button.click()
    new_url = driver.window_handles[1]
    driver.switch_to.window(new_url)

def scrape_names():
    names = driver.find_elements(By.TAG_NAME, value="strong")
    return [format_name(name.text) for name in names]

def scrape_image_urls():
    url_beginning = "https://mymustangs.milton.edu/student/directory/"
    return [url_beginning + elem.get_attribute("background") for elem in driver.find_elements(by=By.TAG_NAME, value="table")[1:]]

def save_image_pngs(image_urls, year):
    if not os.path.exists(f"assets/{year}"):
        os.makedirs(f"assets/{year}")

    for idx, image_url in enumerate(image_urls):
        driver.get(image_url)
        img = driver.find_element(By.TAG_NAME, value="img")
        img.screenshot(f"assets/{year}/{idx}-profile.png")

def dump_student_data(students, file_name):
    with open(file_name, "w") as f:
        json.dump([student.__dict__ for student in students], f, indent=4)


if __name__ == '__main__':
    main()
    driver.quit()