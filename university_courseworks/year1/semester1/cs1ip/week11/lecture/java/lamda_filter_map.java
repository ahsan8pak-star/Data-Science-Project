// Filtering elements and transforming to uppercase via Streams
String[] names = {"Alice", "Bob", "Charlie"};
String[] filteredNames = Arrays.stream(names)
    .filter(name -> name.startsWith("A"))
    .map(String::toUpperCase)
    .toArray(String[]::new);

