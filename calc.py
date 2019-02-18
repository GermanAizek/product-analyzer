import csv
import configparser

listPrice = []
listPriceSite = []
listItems = []
listItemsSite = []

listPrice = []
listSecond = []

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# read config
try:
	config = configparser.ConfigParser()
	config.read('config.ini')
except KeyError:
	print("[ERROR] config.ini not valid")

class Item(object):
	def __init__(self, sku, name, price):
		self.sku = sku;
		self.name = name;
		self.price = price;

def fileReadAppend(name, list):
	with open(name) as file:
		reader = csv.DictReader(file, delimiter=config['CSV']['DelimiterCSV'])
		for line in reader:
			list.append(Item(line[config['TABLE']['ColumnVendorCode']], line[config['TABLE']['ColumnNameItem']], line[config['TABLE']['ColumnPriceItem']]))

def getSkuItemsAppend(listAppend, listItems):
	length = len(listItems)
	printProgressBar(0, length, prefix = 'Getting SKU, Items Append:', suffix = 'Complete', length = 50)
	for idx, item in enumerate(listItems):
		listAppend.append(item.sku)
		printProgressBar(idx + 1, length, prefix = 'Getting SKU, Items Append:', suffix = 'Complete', length = 50)

def getInfoBySku(sku):
	for item in listItems:
		if sku == item.sku:
			break

	for item in listItemsSite:
		if sku == item.sku:
			break

	return item.name, item.price

def writeInFile(name, list):
	with open(name + '_result.' + config['DEFAULT']['FormatPrice'], 'w', newline='') as csvfile:
		fieldnames = ['_SKU_', '_NAME_', '_PRICE_']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=config['CSV']['DelimiterCSV'])

		writer.writeheader()

		length = len(list)
		printProgressBar(0, length, prefix = 'Write to CSV list:', suffix = 'Complete', length = 50)
		for idx, sku in enumerate(list):
			info = getInfoBySku(sku)
			writer.writerow({'_SKU_': sku, '_PRICE_': info[1], '_NAME_': info[0]})
			printProgressBar(idx + 1, length, prefix = 'Write to CSV list:', suffix = 'Complete', length = 50)

 
if __name__ == "__main__":
	fileReadAppend(config['DEFAULT']['NameFile'] + '.' + config['DEFAULT']['FormatPrice'], listItems)
	fileReadAppend(config['DEFAULT']['NameFileSecond'] + '.' + config['DEFAULT']['FormatPrice'], listItemsSite)

	getSkuItemsAppend(listPrice, listItems)
	getSkuItemsAppend(listPriceSite, listItemsSite)

	for result in list(set(listPrice) ^ set(listPriceSite)):
		if result in listPrice:
			listValid.append(result)
		else:
			listNotValid.append(result)

	writeInFile(config['DEFAULT']['NameFile'], listValid)
	writeInFile(config['DEFAULT']['NameFileSecond'], listNotValid)
