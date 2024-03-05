import requests
import time
import webbrowser
import datetime
global toast_ready
toast_ready = True
try:
    from win11toast import toast
except ImportError:
    print("win10toast not installed or unsupported, you will not be notified if an update has occured from outside the console")
    toast_ready = False

url = "https://example.com/"
loop_time = 1   

print("checking " + url + " every " + str(loop_time) + " seconds for updates")
try:
    def check_website(url):
        response = requests.get(url)
        return response.text

    def show_notification(title, message, url):
        curernt_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(curernt_time + " Website has been updated!")
        toast(title, message, on_click=url)

    def monitor_website(url):
        previous_code = None

        while True:
            curernt_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_code = check_website(url)

            if previous_code and current_code != previous_code:
              if toast_ready == True:
                show_notification("Website has been updated!", "Click to open website", website_url)
              else:
                print("Website has been updated!")
            else:
              print(curernt_time + " no update")

            previous_code = current_code
            time.sleep(loop_time)

    if __name__ == "__main__":
        website_url = url
        monitor_website(website_url)
except KeyboardInterrupt:
    exit("\b\b  \nProgram stopped by user via \"^C\"")