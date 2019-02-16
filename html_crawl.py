import requests
import time


URL_PATTERN = 'https://artofproblemsolving.com/wiki/index.php/%d_%s_Problems/Problem_%d'

CONFIG = [
    ('AMC_8', 1999, 2003, 25)
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


urls = []
for conf in CONFIG:
  urls += url_crawl(conf[0], conf[1], conf[2], conf[3])

# print(urls)

for url in urls:
  response = requests.get(url)
  time.sleep(1)
  webContent = response.text
  file_name = url[47:]
  file_name = 'html/' + file_name.replace('/', '_')

  with open(file_name, "w") as out:
    out.write(webContent)
    out.close()
