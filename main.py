from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import math
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ssl
import certifi
import random
import time
import undetected_chromedriver as uc
import time

def merge_sort(array):
    # If the input array contains fewer than two elements,
    # then return it as the result of the function
    if len(array) < 2:
        return array

    midpoint = len(array) // 2

    # Sort the array by recursively splitting the input
    # into two equal halves, sorting each half and merging them
    # together into the final result
    return merge(
        left=merge_sort(array[:midpoint]),
        right=merge_sort(array[midpoint:]))

def merge(left, right):
    # If the first array is empty, then nothing needs
    # to be merged, and you can return the second array as the result
    if len(left) == 0:
        return right

    # If the second array is empty, then nothing needs
    # to be merged, and you can return the first array as the result
    if len(right) == 0:
        return left

    result = []
    index_left = index_right = 0

    # Now go through both arrays until all the elements
    # make it into the resultant array
    while len(result) < len(left) + len(right):
        # The elements need to be sorted to add them to the
        # resultant array, so you need to decide whether to get
        # the next element from the first or the second array
        if len(left[index_left]) <= len(right[index_right]):
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        # If you reach the end of either array, then you can
        # add the remaining elements from the other array to
        # the result and break the loop
        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break

    return result





with open("/Users/jackvu/Desktop/PDS/jklm/venv/scrabble.txt", "r") as file:
    words = [line.strip() for line in file]

def find_word(substring, played_words): # to start simple, just play the shortest one?
    legalWords = []
    for word in words:
        if substring in word and word not in played_words:
            legalWords.append(word)
    list_size = len(legalWords)
    legalWords = merge_sort(legalWords)
    seed = random.random() * (list_size - 1)# seed value is just some value x in between zero and the list size
    index = round((list_size - 1) / (1 + math.exp(seed * -1 * (list_size - 1) / 8))) # logistic function where k = -L/4, L is the size of the list - 1
    return legalWords[index] # function gravitates towards the top, but not completely


driver_path = "/Users/jackvu/Desktop/PDS/jklm/venv/chromedriver"

# Chrome options to make the browser less detectable
options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"  # Path to Chrome Beta

# Adding Chrome options to help evade detection
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--disable-popup-blocking")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initializing the Chrome driver with specified options
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Anti-detection code to modify navigator properties
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
    """
})
driver.get("https://jklm.fun/")
time.sleep(2)
game_options = driver.find_element(by=By.CLASS_NAME, value="list")
separate_games = game_options.find_elements(by=By.CLASS_NAME, value="bombparty")
current = 0
count = round(random.random() * 3)
for element in separate_games:
    if "English" in element.text and count == current:
        time.sleep(.5)
        href_value = element.get_attribute("href")
    # Navigate to the URL
        if href_value:
            driver.get(href_value)
            break
    elif "English" in element.text:
        current += 1
# all navigates to some bomb party game automatically
# enter name in the tet box

time.sleep(2)

text_box = driver.find_element(by=By.CLASS_NAME, value="line").find_element(By.TAG_NAME, "input")
text_box.send_keys("Griffious")
# click the submit button
time.sleep(1.5)
submit_button = driver.find_element(by=By.CLASS_NAME, value="line").find_element(By.TAG_NAME, "button")
submit_button.click()

game_finished = False
game_joined = False

while True:
    try:
        iframe = driver.find_element(by=By.CSS_SELECTOR, value="iframe")
        break
    except:
        continue
time.sleep(30)
driver.switch_to.frame(0)
syllable = "" # right now, just have it only play once
played_words = []
while not game_finished: # also, if the join game button is present, click it,
    if not game_joined:
        try:
            join_button = driver.find_element(by=By.CLASS_NAME, value="join").find_element(By.TAG_NAME, "button")
            join_button.click()
            game_joined = True
        except:
            print("game in progress, unable to join")
        try:
            syllable = driver.find_element(by=By.CLASS_NAME, value="syllable").text
            print(syllable)
        except:
            print("no syllable found")
    else:
        try:
            syllable = driver.find_element(by=By.CLASS_NAME, value="syllable").text
            try:
                name = driver.find_element(by=By.CLASS_NAME, value="player").text
                if name == "":
                    time.sleep(.5)
                    syllable = driver.find_element(by=By.CLASS_NAME, value="syllable").text
                    word = find_word(syllable, played_words).lower()
                    played_words.append(word)
                    answer_box = driver.find_element(by=By.CLASS_NAME, value="otherTurn").find_element(By.TAG_NAME, "input")
                    time.sleep(random.random() * 2)
                    for char in word:
                        answer_box.send_keys(char)
                        time.sleep(random.random() / 20)
                    answer_box.submit()
                    print(word + " played")
            except:
                time.sleep(.5)
                syllable = driver.find_element(by=By.CLASS_NAME, value="syllable").text
                word = find_word(syllable, played_words).lower()
                played_words.append(word)
                answer_box = driver.find_element(by=By.CLASS_NAME, value="otherTurn").find_element(By.TAG_NAME, "input")
                time.sleep(random.random() * 2)
                for char in word:
                    answer_box.send_keys(char)
                    time.sleep(random.random() / 20)
                answer_box.submit()
                print(word + " played")

        except:
            print("no syllable found")

# For example, locate and interact with an element inside the iframe
time.sleep(15)




driver.quit()


