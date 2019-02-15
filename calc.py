import csv

listPrice = []
listPriceOld = []
listItems = []
listItemsOld = []
listAdded = []
listRemoved = []
#result = []

def getItem(list):
	for i in list:
		print(i.sku),
		print(i.name),
		print(i.price)


class Item(object):
	def __init__(self, sku, name, price):
		self.sku = sku;
		self.name = name;
		self.price = price;

	def getSku(self):
		return self.sku;
 
if __name__ == "__main__":
	with open("price_old.csv") as fo:
		reader = csv.DictReader(fo, delimiter=';')
		for line in reader:
			listItemsOld.append(Item(line["_SKU_"], line["_NAME_"], line["_PRICE_"]))

	with open("price.csv") as f:
		reader = csv.DictReader(f, delimiter=';')
		for line in reader:
			listItems.append(Item(line["_SKU_"], line["_NAME_"], line["_PRICE_"]))


	for result in list(set(listPrice) ^ set(listPriceOld)):
		if result in listPrice:
			listAdded.append(result)
		else:
			listRemoved.append(result)

	getItem(listRemoved)

	#print(listRemoved)
	#print(listAdded)
