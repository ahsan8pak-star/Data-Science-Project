import os
import time

def card_compare(card1, card2):
    # Compares two cards based on suit priority, then number.
    # In Python, slicing [:-1] gets everything except the last character (the number)
    # Slicing [-1] gets only the very last character (the suit)
    num1 = int(card1[:-1])
    suit1 = card1[-1]
    
    num2 = int(card2[:-1])
    suit2 = card2[-1]
    
    # Convert suits into unique priority values
    suit_priority1 = get_suit_priority(suit1)
    suit_priority2 = get_suit_priority(suit2)
    
    # Compare suits first
    if suit_priority1 < suit_priority2:
        return -1
    elif suit_priority1 > suit_priority2:
        return 1
        
    # If suits are equal, compare numbers
    if num1 < num2:
        return -1
    elif num1 > num2:
        return 1
        
    # Cards are equal
    return 0

def get_suit_priority(suit):
     # Python's alternative to a Java Switch statement.
     # Equivalent to Java's switch-case, but uses 'match' and 'case' keywords.
    match suit:
        case 'H':
            return 0
        case 'C':
            return 1
        case 'D':
            return 2
        case 'S':
            return 3
        case _:
            return -1  # The underscore acts as the 'default' case

def bubble_sort(lst):
    # Bubble sort algorithm.
    # Create a copy [:] to avoid modifying the original list
    sorted_list = lst[:]
    n = len(sorted_list)
    
    for i in range(n - 1):
        for j in range(n - i - 1):
            # Compare adjacent cards using card_compare
            if card_compare(sorted_list[j], sorted_list[j + 1]) > 0:
                # Python allows you to swap variables in one clean line
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                
    return sorted_list

def merge_sort(array):
    # Recursive Merge Sort algorithm.
    # Base case: if list has 0 or 1 element, it's already sorted
    if len(array) <= 1:
        return array[:]
        
    # Divide the list into two halves
    mid = len(array) // 2
    left = array[:mid]
    right = array[mid:]
    
    # Recursively sort both halves
    left = merge_sort(left)
    right = merge_sort(right)
    
    # Merge the sorted halves
    return merge(left, right)

def merge(left, right):
    # Helper function to merge two sorted lists.
    result = []
    i = 0 # Index for left list
    j = 0 # Index for right list
    
    # Compare elements from both lists and add the smaller one to result
    while i < len(left) and j < len(right):
        if card_compare(left[i], right[j]) <= 0:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    # Python shortcut: list.extend() adds the remaining elements all at once.
    # This replaces the two trailing 'while' loops from the Java code.
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def read_file(filename):
    # Reads lines from a file and returns them as a list.
    cards = []
    
    # __file__ gets the path of SortComparison.py
    # os.path.dirname strips the filename off, leaving just the folder path
    # os.path.abspath makes it a full, absolute C:\ path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 4. Join the folder path with the filename (e.g., sort10.txt)
    file_path = os.path.join(script_dir, filename)
            
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find file: {file_path}")
        
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line: # If line is not empty
                cards.append(line)
                
    return cards

def write_results_to_csv(card_counts, bubble_times, merge_times):
    # Writes benchmarking results to a CSV file.
    # Ensure the CSV saves in the exact same folder as the script
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "SortComparison.csv")
    
    with open(output_path, "w") as writer:
        counts_str = ",".join([f" {c}" for c in card_counts])
        bubble_str = ",".join([f" {t}" for t in bubble_times])
        merge_str = ",".join([f" {t}" for t in merge_times])
        
        writer.write(f",{counts_str}\n")
        writer.write(f"bubbleSort,{bubble_str}\n")
        writer.write(f"mergeSort,{merge_str}\n")

def sort_comparison(files):
    # Runs sorts against files and logs execution times.
    card_counts = []
    bubble_times = []
    merge_times = []
    
    for filename in files:
        # Read the file
        cards = read_file(filename)
        card_counts.append(len(cards))
        
        # Measure bubbleSort execution time
        bubble_list = cards[:]
        
        # time.perf_counter() is Python's most accurate timer. 
        # Multiplying by 1000 converts seconds to milliseconds to match Java.
        bubble_start = int(time.perf_counter() * 1000)
        bubble_sort(bubble_list)
        bubble_end = int(time.perf_counter() * 1000)
        bubble_times.append(bubble_end - bubble_start)
        
        # Measure mergeSort execution time
        merge_list = cards[:]
        merge_start = int(time.perf_counter() * 1000)
        merge_sort(merge_list)
        merge_end = int(time.perf_counter() * 1000)
        merge_times.append(merge_end - merge_start)
        
    write_results_to_csv(card_counts, bubble_times, merge_times)

# ------------------------------------------------------------
# MAIN EXECUTION BLOCK (Equivalent to public static void main)
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("Testing card_compare")
        print(f"card_compare(\"4H\", \"4H\") = {card_compare('4H', '4H')}") # Expected: 0
        print(f"card_compare(\"4H\", \"3S\") = {card_compare('4H', '3S')}") # Expected: -1
        print(f"card_compare(\"4H\", \"3H\") = {card_compare('4H', '3H')}") # Expected: 1
        print(f"card_compare(\"7C\", \"7D\") = {card_compare('7C', '7D')}") # Expected: -1
        print(f"card_compare(\"1S\", \"13S\") = {card_compare('1S', '13S')}") # Expected: -1

        print("\nTesting bubble_sort")
        list1 = ["4H", "3S", "7S", "8C", "2D", "3H"]
        print(f"Original: {list1}")
        print(f"Sorted:   {bubble_sort(list1)}")
        # Expected: ['3H', '4H', '8C', '2D', '3S', '7S']

        print("\nTesting merge_sort")
        list2 = ["4H", "3S", "7S", "8C", "2D", "3H"]
        print(f"Original: {list2}")
        print(f"Sorted:   {merge_sort(list2)}")
        # Expected: ['3H', '4H', '8C', '2D', '3S', '7S']

        print("\nRunning sort_comparison")
        print("Analyzing files: sort10.txt, sort100.txt, sort10000.txt")
        sort_comparison(["sort10.txt", "sort100.txt", "sort10000.txt"])
        print("✓ CSV file 'SortComparison.csv' generated successfully!")
        print("Check the file for performance results.")

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("\nMake sure the following files exist in your project directory:")
        print("  - sort10.txt")
        print("  - sort100.txt")
        print("  - sort10000.txt")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")