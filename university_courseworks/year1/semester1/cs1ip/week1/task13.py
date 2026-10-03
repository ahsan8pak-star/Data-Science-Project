import math

hallLength = 12.5  # meters
hallWidth = 8.0  # meters
tileSide = 0.5  # meters (square tiles)
wasteRate = 0.08  # 8% extra
pricePerTile = 3.20  # £

hallArea = hallLength * hallWidth
tileArea = tileSide * tileSide
exactTiles = hallArea / tileArea
withWaste = exactTiles * (1.0 + wasteRate)

tilesToBuy = int(math.ceil(withWaste))
totalCost = tilesToBuy * pricePerTile

print("Tiles to buy: " + str(tilesToBuy))
print("Total cost: £%.2f\n" % (totalCost))

