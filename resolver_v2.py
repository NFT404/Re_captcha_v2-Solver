#Script By NFT404
#Github: https://github.com/NFT404/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import requests
import soundfile
import speech_recognition as sr


#config chrome options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#driver config
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

def get_re_Captcha_v2():
    driver.get('https://recaptcha-demo.appspot.com/recaptcha-v2-invisible.php')
    
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit ↦')]"))).click()
    try:
        #thats wait for re_Captcha if dont have re_Captcha will pass
        wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')))
        #print fiding the Captcha with loading emoji
        print('Fiding the Captcha...🔍')
        #change to the iframe of the captcha
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')))
        #click on the audio button
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, 'recaptcha-audio-button'))).click()
        #get attribute of the audio source
        audio_source = wait.until(EC.presence_of_element_located((By.XPATH, '//audio[@id="audio-source"]'))).get_attribute('src')
    
        print('Downloading the audio file...📥')
        #download the audio file with requests
        audio_file = requests.get(audio_source, stream=True)

        #save the audio file as wav
        with open('audio.wav', 'wb') as f:
            f.write(audio_file.content)
            data, samplerate = soundfile.read('audio.wav')
            soundfile.write('audio.wav', data, samplerate, subtype='PCM_16')
            print('Audio file downloaded...✅')

        print('Converting the audio file to text...🕑')
        
        r = sr.Recognizer()
        with sr.AudioFile('audio.wav') as source:
            audio = r.record(source)
            print('Audio file converted to text...✅')
        
        print('Audio file converted to text...✅')
        print('Inputing the text...🕑')

        wait.until(EC.element_to_be_clickable((By.ID, 'audio-response'))).send_keys(r.recognize_google(audio))
        wait.until(EC.element_to_be_clickable((By.ID, 'recaptcha-verify-button'))).click()
       
        print('Captcha solved...✅')

        driver.back()
    except:
        print('Captcha not found...❌')

if __name__ == '__main__':
    get_re_Captcha_v2()
