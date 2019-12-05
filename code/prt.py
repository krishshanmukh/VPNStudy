# Python program to measure page load times
#!/usr/bin/env python

import sys

websites = []
def load_websites():
    with open("./google_sites.txt") as f:
        line = f.readline()
        while line:
            websites.append([line[:-1], [],[]])
            line = f.readline()

COUNT = 10
import requests
import json
def get_page_request_times(filename):
    for i in range(len(websites)):
        website = "https://"+websites[i][0]
        for _ in range(COUNT):
            response = requests.get(website)
            websites[i][1].append(response.elapsed.total_seconds())
            websites[i][2].append(len(response.content))

        print("Done "+website)

    print(json.dumps(websites))
    with open("plt_"+filename+".json","w+") as f:
        f.write(json.dumps(websites))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the name of the file where the content will be written.")
        sys.exit()

    load_websites()
    get_page_request_times(sys.argv[1])