import os
import sys
import defs

from bs4 import BeautifulSoup

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print('Usage:')
    print('')
    print('python ofrip.py "pathToHtmlFile"')
    sys.exit()

if not os.path.isfile(filename):
    print(f"File [{filename}] is not found.")
    sys.exit()

f = open(filename, encoding="utf8").read()
print(len(f))

soup = BeautifulSoup(f, 'html.parser')

par_div = soup.findAll("div", {"class": "b-post"})

defs.getAll(False, par_div)

graball = input("Download everything? y or n :=> ")

if graball.strip().lower() == "y":

    defs.reset_prct()
    defs.getAll(True, par_div)


