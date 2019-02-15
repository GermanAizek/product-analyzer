import csv
import configparser

listPrice = []
listPriceSite = []
listItems = []
listItemsSite = []

listUnchanged = []
listValid = []
listNotValid = []

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
	for item in listItems:
		listAppend.append(item.sku)

#def getInfoBySku(sku):
	#
 
if __name__ == "__main__":
	fileReadAppend(config['DEFAULT']['NameFile'] + '.' + config['DEFAULT']['FormatPrice'], listItems)
	fileReadAppend(config['DEFAULT']['NameFileOld'] + '.' + config['DEFAULT']['FormatPrice'], listItemsSite)

	getSkuItemsAppend(listPrice, listItems)
	getSkuItemsAppend(listPriceSite, listItemsSite)

	for result in list(set(listPrice) ^ set(listPriceSite)):
		if result in listPrice:
			listValid.append(result)
		else:
			listNotValid.append(result)

	listUnchanged = list(set(listPrice) & set(listPriceSite))

	print('Unchanged: ' + str(listUnchanged))
	print('Exist in ' + config['DEFAULT']['NameFile'] + '.' + config['DEFAULT']['FormatPrice'] + ': ' + str(listValid))
	print('Exist in ' + config['DEFAULT']['NameFileOld'] + '.' + config['DEFAULT']['FormatPrice'] + ': ' + str(listNotValid))
	
