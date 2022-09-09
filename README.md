# sv_transtelematica_project
An applicant's autotesting task (Selenium Webdriver, pytest, pytest_bdd)

Install package dependencies in your virtual environment:
```
pip install -r requirements.txt
```
Google Chrome browser is the most popular now. That's why my project call ChromeDriver for testing.

Find the correct driver version at https://sites.google.com/chromium.org/driver/
On the page that opens, right-click on the file for Linux and copy the path to the file. 
In the example below, replace the file path for the wget command with your URL:
```
wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```
Move the unzipped ChromeDriver file to the correct folder and allow chromedriver to run as an executable:
```
sudo mv chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
```

Check that chromedriver is available by running the chromedriver command in the terminal, you should get a message that the process started successfully:

![image](https://user-images.githubusercontent.com/107465356/189307147-b2a795cb-a31d-475f-9980-8b4adb90a293.png)

If you get the message "Command 'chromedriver' not found" then repeat the driver installation following the instructions above.

For starting project go to directory and execute pytest: 
```
pytest -sv --tb=line --reruns 2
```
Sometimes browser work slowly and need to cache some data that's why I put rerun plugin
