import json
import requests
import bs4
import time
import os
import pprint

from bs4 import BeautifulSoup
from os import system
from time import sleep

system("cls")
links = {}
for i in range(0, 3937, 24):
    url = f"//doujin-th.com/forum/index.php?action=tags&tagid=1&start={i}"
    links[f"Linkpage{i//24+1}"] = url
    print(f"{f'Linkpage{i//24+1}':<10}: {url}")

new_prefix = "https://doujin-th.com/forum/index.php?action=tags&tagid=1&start="
for key, value in links.items():
    links[key] = value.replace("//doujin-th.com/forum/index.php?action=tags&tagid=1&start=", new_prefix)

print("Save Success")
system("cls")
with open('data\links.json', 'w') as f:
    json.dump(links, f, indent=4)

with open('data\links.json', 'r') as f:
    links = json.load(f)

stories = {}
for key, value in links.items():
    url = value
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith("//doujin-th.com/forum/index.php?topic="):
            story_id = href.split("=")[1]
            stories[f"Story{story_id}"] = f"https://doujin-th.com/forum/index.php{href}"
            print(f"Story{story_id}: https://doujin-th.com/forum/index.php{href}")

with open('data\stories.json', 'w') as f:
    json.dump(stories, f, indent=4)

with open('data\stories.json', 'r') as f:
    stories = json.load(f)

downloads = {}
value_dict = {}
system("cls")
for key, value in stories.items():
    url = value
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    value = soup.find('h1', {'class': 'panel-title'})
    if value:
        value = value.text.strip()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and "http://www.mediafire.com/download" in href:
                if value in value_dict:
                    if href not in value_dict[value]:
                        value_dict[value].append(href)
                        downloads[f"Value{len(downloads)+1}"] = {"value": value, "url": href}
                        print(f"Value{len(downloads)}: {value} - {href}")
                else:
                    value_dict[value] = [href]
                    downloads[f"Value{len(downloads)+1}"] = {"value": value, "url": href}
                    print(f"Value{len(downloads)}: {value} - {href}")
    else:
        print(f"No value found for {url}. Skipping.")

with open('data\downloads.json', 'w') as f:
    json.dump(downloads, f, indent=4)