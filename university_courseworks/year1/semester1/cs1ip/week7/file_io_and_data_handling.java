// Writing formatted records
Formatter output = new Formatter("clients.txt");
output.format("%d %s %s %.2f%n", 100, "Bob", "Blue", 24.98);
output.format("%d %s %s %.2f%n", 200, "Steve", "Green", -345.67);
output.close();

// Reading sequential tokens
Scanner input = new Scanner(Path.of("clients.txt"));
while (input.hasNext()) {
    int account = input.nextInt();
    String firstName = input.next();
    String lastName = input.next();
    double balance = input.nextDouble();
    System.out.printf("account %d from %s %s has balance %.2f%n", 
                      account, firstName, lastName, balance);
}
input.close();

