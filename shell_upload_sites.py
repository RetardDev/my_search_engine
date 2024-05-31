from search_engine.models.web import Site


file_txt = r'C:\Users\ataki\OneDrive\Desktop\Intelligent Search Engine\my_search_engine\top-1000-websites.txt'

with open(file_txt, 'r') as file:
  lines = file.readlines()

for line in lines:
  web_protocol = 'http://www.'
  correct_url = web_protocol + line.strip()
  site = Site(url=correct_url)
  site.save()
