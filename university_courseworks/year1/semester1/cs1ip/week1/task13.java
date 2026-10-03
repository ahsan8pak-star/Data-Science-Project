public class Task13 { 
    public static void main(String[] args) { 
        double hallLength = 12.5;   // meters 
        double hallWidth  = 8.0;    // meters 
        double tileSide   = 0.5;    // meters (square tiles) 
        double wasteRate  = 0.08;   // 8% extra 
        double pricePerTile = 3.20; // £ 
 
        double hallArea = hallLength * hallWidth; 
        double tileArea = tileSide * tileSide; 
        double exactTiles = hallArea / tileArea; 
        double withWaste = exactTiles * (1.0 + wasteRate); 

        int tilesToBuy = (int) Math.ceil(withWaste); 
        double totalCost = tilesToBuy * pricePerTile; 

        System.out.println("Tiles to buy: " + tilesToBuy); 
        System.out.printf("Total cost: £%.2f%n", totalCost); 
    } 
}

