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

def getInfoBySku(sku):
	for item in listItems:
		for item in listItemsSite:
			if sku == item.sku:
				break

	return item.name, item.price

 
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

	listUnchanged = list(set(listPrice) & set(listPriceSite))

	# print('Unchanged: ' + str(listUnchanged) + '\n')
	
	# print('Exist in ' + config['DEFAULT']['NameFile'] + '.' + config['DEFAULT']['FormatPrice'] + ': ' + str(listValid) + '\n')
	# print(" SKU      Name      Price")
	# for sku in listValid:
	# 	print(" " + sku + " " + getInfoBySku(sku)[0] + " " + getInfoBySku(sku)[1])
	
	# print('\nExist in ' + config['DEFAULT']['NameFileSecond'] + '.' + config['DEFAULT']['FormatPrice'] + ': ' + str(listNotValid) + '\n')
	# print(" SKU      Name      Price")
	# for sku in listNotValid:
	# 	print(" " + sku + " " + getInfoBySku(sku)[0] + " " + getInfoBySku(sku)[1])

	with open(config['DEFAULT']['NameFileOut'] + '.' + config['DEFAULT']['FormatPrice'], 'w', newline='') as csvfile:
		csvfile.write('Exist in ' + config['DEFAULT']['NameFile'] + '.' + config['DEFAULT']['FormatPrice'] + '\n\n')

		fieldnames = ['_SKU_', '_NAME_', '_PRICE_']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=config['CSV']['DelimiterCSV'])

		writer.writeheader()

		for sku in listValid:
			writer.writerow({'_SKU_': sku, '_PRICE_': getInfoBySku(sku)[1], '_NAME_': getInfoBySku(sku)[0]})

		csvfile.write('\nExist in ' + config['DEFAULT']['NameFileSecond'] + '.' + config['DEFAULT']['FormatPrice'] + '\n\n')

		writer.writeheader()
		
		for sku in listNotValid:
			writer.writerow({'_SKU_': sku, '_PRICE_': getInfoBySku(sku)[1], '_NAME_': getInfoBySku(sku)[0]})