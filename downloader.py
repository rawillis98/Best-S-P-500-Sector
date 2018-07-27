import requests, os, sys
from Datafile import *
def download(indir, symbol): #downloads CSV of historical [symbol] data from Alphavantage
    print("downloading", symbol + "...")
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&&symbol=" + symbol + "&outputsize=full&datatype=csv&apikey=IRJ3C7BL8LQGE7PR"
    print(url)
    r = requests.get(url)
    with open(indir + "//" + symbol + ".csv", 'wb') as f:
        f.write(r.content)
path = r'C:\Users\ricwi\Documents\Projects\Project 5 - Best Sector\Data'
symbols = ['XLB', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'IYR', 'XLK', 'IYZ', 'XLU']
for symbol in symbols:
    download(path, symbol)
