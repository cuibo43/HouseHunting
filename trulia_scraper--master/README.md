# Trulia_scraper
Scrape [Truila](https://www.trulia.com/) for homes(House, Condo, Townhome, Multi-Family, Land, Mobile/Manufactured) and will give you a csv file sorted by date.

Usage
-----

````
usage: trulia [-h] [-s STATE] [-c CITY] [-b] [-min MIN] [-max MAX] [-o OUT]

optional arguments:
  -h, --help            show this help message and exit
  -s STATE, --state STATE
                        state name. e.g. NY
  -c CITY, --city CITY  city or borough name. e.g. Manhattan
  -b, --beds            beds number, to increase -bbbb = 4 beds
  -min MIN              minimum price 100
  -max MAX              max price 100000
  -o OUT, --out OUT     file name
````

Install requirements and Run
----------------------------

````
pip install -r requirements.txt

python main.py -s NY -c Manhattan -bbb -min 15000 -max 1900000
````

![imgae](https://user-images.githubusercontent.com/14273726/46585556-ba91cd00-ca72-11e8-9b5c-39ab71d905b8.gif)

## Authors

* **Mohamed Salah** - [Gitexel](https://github.com/gitexel)
