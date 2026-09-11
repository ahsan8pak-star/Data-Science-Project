def shipping_label(*name, **location):

    # *name captures positional args as a tuple: ("Dr.", "Nobody", "Knows")
    full_name = " ".join(name).upper().replace(".", "") # removes any dots (.) if initials are inputted as such after uppercasing all letters
    print(full_name)

    # **location captures keyword args as a dictionary
    # Define layout sequence as a structural checklist
    label_template = [
        ("floor", "FLOOR "),
        ("street", ""),
        ("city", ""),
        ("county", ""),
        ("postcode", "")
    ]

    # Dynamically looks up kwargs keys ( **location ) using the sequence template
    for key, prefix in label_template: # Converts each key mentioned into its respective converted form on 'label_template'
        if value := location.get(key): # uses the Walrus operator (:=) to get 'location' key and assigns to 'value'
            cleaned_value = str(value).upper().replace(".", "").replace(",", "")
            # converts all values to string, uppercases all, and replaces dots (.) and commas (,) into empty strings ("")
            print(f"{prefix}{cleaned_value}")

# Executing using standard positional (*args) and keyword (**kwargs) syntax
shipping_label("Dr.", "Nobody", "Knows",
               street = "1 Fake Av.",
               floor = "123", 
               postcode = "RD1 2AB",
               city = "Reading",
               county = "Berkshire")

