# Python program to measure page load times

websites = []
COUNT = 5

def load_websites():
    with open("./websites.txt") as f:
        line = f.readline()
        while line:
            websites.append([line[:-1], []])
            line = f.readline()

def get_page_request_times():
    import requests
    for i in range(len(websites)):
        website = websites[i][0]
        for _ in range(COUNT):
            websites[i][1].append(requests.get(website).elapsed.total_seconds())
        print(websites[i])
        

if __name__ == "__main__":
    load_websites()
    print(websites)
    get_page_request_times()