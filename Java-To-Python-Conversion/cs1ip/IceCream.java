import java.util.Scanner;

public class IceCream {

    private static final int CONE_PRICE = 100;
    private static final int VANILLA_PRICE = 19;
    private static final int CHOCOLATE_PRICE = 34;
    private static final int STRAWBERRY_PRICE = 0;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Would you like (v)anilla, (c)hocolate or (s)trawberry?");
        String flavor = scanner.nextLine().toLowerCase();

        if (!flavor.equals("v") && !flavor.equals("c") && !flavor.equals("s")) {
            System.out.println("We don't have that flavour.");
            scanner.close();
            return;
        }

        System.out.println("How many scoops would you like?");
        int scoops;
        try {
            scoops = scanner.nextInt();
        } catch (Exception e) {
            System.out.println("Please enter a valid number.");
            scanner.close();
            return;
        }

        switch (scoops) {
            case 1:
            case 2:
            case 3:
                break;
            case 0:
                System.out.println("We don't sell just a cone.");
                scanner.close();
                return;
            default:
                System.out.println("That's too many scoops to fit in a cone.");
                scanner.close();
                return;
        }

        int pricePerScoop;
        switch (flavor) {
            case "v":
                pricePerScoop = VANILLA_PRICE;
                break;
            case "c":
                pricePerScoop = CHOCOLATE_PRICE;
                break;
            case "s":
                pricePerScoop = STRAWBERRY_PRICE;
                break;
            default:
                pricePerScoop = 0;
                break;
        }

        int totalPence = CONE_PRICE + (pricePerScoop * scoops);
        double totalPounds = totalPence / 100.0;
        System.out.printf("That will be %.2f please.\n", totalPounds);

        scanner.close();
    }

}

