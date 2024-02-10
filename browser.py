import argparse
import os
import pathlib

import requests
from bs4 import BeautifulSoup
from colorama import Fore


def url_is_good(url):
    return "." in url


def save_content_url(url_input_text: str, folder: str, content_text: str):
    file_name_ = url_input_text.split(".")[0]

    with open(pathlib.Path(folder).joinpath(file_name_), mode="w",
              encoding="utf-8") as f:
        f.write(content_text)


def check_file_exists(folder, file):
    return os.access(pathlib.Path(folder).joinpath(file), os.F_OK)


def print_file_content(folder, file):
    with open(pathlib.Path(folder).joinpath(file), mode="r", encoding="utf-8") as f:
        print(f.read())


def requests_get(url: str) -> requests.Response:
    if not url.startswith("https://"):
        url = "https://" + url
    return requests.get(url)
    # if r:
    #     return r.content
    # else:
    #     return None


parser = argparse.ArgumentParser()
parser.add_argument("folder")
args = parser.parse_args()
folder_name = args.folder
if not os.access(folder_name, mode=os.F_OK):
    os.mkdir(folder_name)

stack_urls = []


def parse_response(response_url):
    soup = BeautifulSoup(response_url.content, 'html.parser')

    # print(soup.prettify())
    text_content = ""
    for p in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"]):
        # print(p.getText())
        if p.name == "a":
            text_content += Fore.BLUE + p.text + "\n"
        else:
            text_content += Fore.WHITE + p.text + "\n"

    return text_content


while True:
    url_input = input()
    if url_input == "exit":
        break
    elif url_input == "back":
        if stack_urls:
            stack_urls.pop()
            if stack_urls:
                print_file_content(folder_name, stack_urls[-1])
            else:
                pass
        else:
            pass

    elif check_file_exists(folder_name, url_input):
        stack_urls.append(url_input)
        print_file_content(folder_name, url_input)
    elif url_is_good(url_input):
        file_name = url_input.split(".")[0].replace("https://", "")
        response = requests_get(url_input)
        content_text = parse_response(response)
        print(content_text)

        save_content_url(file_name, folder_name, content_text)
        stack_urls.append(file_name)

        # if url_input == "bloomberg.com":
        #     print(bloomberg_com)
        #     save_content_url(file_name, folder_name, bloomberg_com)
        #     stack_urls.append(file_name)
        # elif url_input == "nytimes.com":
        #     print(nytimes_com)
        #     save_content_url(file_name, folder_name, nytimes_com)
        #     stack_urls.append(file_name)
        # else:
        #     print("Invalid URL")
    else:
        print("Invalid URL")
