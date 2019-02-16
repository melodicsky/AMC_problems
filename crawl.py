import urllib3
import time
import requests
from bs4 import BeautifulSoup

URL_PATTERN = 'https://artofproblemsolving.com/wiki/index.php/%d_%s_Problems/Problem_%d'


CONFIG = [
    ('AMC_8', 1999, 1999, 2)
    # ('AMC_10', 2000, 2001, 25),
    # ('AMC_10A', 2002, 2018, 25),
    # ('AMC_10B', 2002, 2018, 25),
    # ('AMC_12', 2000, 2001, 25),
    # ('AMC_12A', 2002, 2018, 25),
    # ('AMC_12B', 2002, 2018, 25),
]


def url_crawl(title, year_start, year_end, num):
  urls = []
  for year in range(year_start, year_end + 1):
    for problem in range(1, num + 1):
      urls.append(URL_PATTERN % (year, title, problem))
  return urls


def between(cur, end):
  length = 1
  while cur and cur != end:
    length += 1
    cur = cur.next_element
  return length


urls = []
for conf in CONFIG:
  urls += url_crawl(conf[0], conf[1], conf[2], conf[3])

problem_list = []
for url in urls:
  r = requests.get(url)
  time.sleep(1)
  c = r.content
  soup = BeautifulSoup(c)
  main_content = soup.find('div', attrs={'class': 'mw-parser-output'})

  problems = main_content.find_all('p')[0:3]

  for problem in problems:
    images = problem.find_all('img', alt=True)
    for image in images:
      image.replace_with(image['alt'])
    problem = problem.get_text()
    # print(problem)
    problem_list.append(problem)

  if 'text{(A)}' not in problem_list[-1]:
    del problem_list[-1]


with open("amc8_1999_to_2002.txt", "w") as out:
  for problem in problem_list:
    out.write(problem)
    out.write("\n")
