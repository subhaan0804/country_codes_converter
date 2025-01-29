from difflib import SequenceMatcher
import time
import csv

def load_country_dict_from_csv(file_path):
    """
    Load country mappings from CSV file.
    CSV structure:
    name,code
    """
    country_dict = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                country_dict[row['name']] = row['code']
        return country_dict
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return {}

# Calculate similarity ratio between two strings.
def get_sequence_ratio(str1, str2):
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

# Gives the most relevant match when we have multiple matches
def get_best_match(matches, search_term):
    """
    Get the most relevant match using sequence matching.
    
    Args:
        matches: List of tuples (country_name, country_code)
        search_term: Original search term
        
    Returns:
        tuple: Single (country_name, country_code) that is most relevant
    """
    if not matches:
        return None
        
    if len(matches) == 1:
        return matches[0]
    
    search_term = search_term.lower()
    best_ratio = 0
    best_match = None
    
    for country_name, code in matches:
        country_lower = country_name.lower()
        
        # Get similarity ratio
        ratio = SequenceMatcher(None, search_term, country_lower).ratio()
        
        # For directional matches (e.g., "korea n" for "Korea (North)")
        parts = search_term.split()
        if len(parts) > 1:
            # Also check similarity with just the main part of the name
            main_part_ratio = SequenceMatcher(None, parts[0], country_lower).ratio()
            ratio = max(ratio, main_part_ratio)
            
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = (country_name, code)
    
    return best_match

def find_country_code(search_term, country_dict):
    """
    Find country codes using advanced matching including partial matches,
    alternative spellings, and abbreviated directions.
    
    Args:
        search_term (str): The search term to look for (e.g., 'korea n', 'turkeye')
        country_dict (dict): Dictionary mapping country names to their codes
        
    Returns:
        list: List of tuples containing (matched_country_name, country_code)
    """

    # Early return for empty strings
    if not search_term:
        return []

    matches = []
    search_term = search_term.lower().strip()

    search_parts = search_term.split()
    is_directional = len(search_parts) > 1 and search_parts[-1] in {'n', 's', 'e', 'w'}
    
    # Handle directional abbreviations
    if is_directional:
        direction_map = {
            'n': 'north',
            's': 'south',
            'e': 'east',
            'w': 'west'
        }
        main_name = ' '.join(search_parts[:-1])
        direction = direction_map[search_parts[-1]]
    
    for country_name, code in country_dict.items():
        country_lower = country_name.lower()
        
        # Check for exact matches first
        if search_term in country_lower:
            matches.append((country_name, code))
            continue

        # Handle directional searches
        if is_directional:
            if main_name in country_lower and direction in country_lower:
                matches.append((country_name, code))
                continue           

        # Fuzzy matching for alternative spellings
        if len(search_term) > 3:  # Only for longer terms to avoid false positives
            ratio = get_sequence_ratio(search_term, country_lower)

            # Adjust this threshold as needed (according to your strictness)
            if ratio > 0.82:  
                matches.append((country_name, code))
    
    best_match = get_best_match(matches, search_term)

    if best_match is None:
        return None

    return [best_match]


# ************************* Driver Program *****************************

if __name__ == "__main__":

    start = time.time()
    all_countries_alpha2 = load_country_dict_from_csv('country_codes.csv')
    end = time.time()
    print("csv file loading time: ", (end-start) * 1000, " ms")


    test_cases = [
        "nor",
        "zhong",
        "zambi",
        "Alg",
        "Andor",
        "rica",
        "afghaN",
        "new",
        "zea",
        "Jkistan",
        "korea",
        "rica",
        "korea n",
        "newzealand",
        "Herzegovina",
        "  "
    ]

    time_list = []
    print("Testing different search patterns:")
    for search in test_cases:

        start = time.time()
        results = find_country_code(search, all_countries_alpha2)
        end = time.time()
        time_list.append(str(round(float((end-start)* 10**3),2))+ " ms")

        print(f"\nSearching for '{search}':")
        if results:
            for country_name, code in results:
                print(f"Found match: {country_name} ({code})")
        else:
            print("No matches found")

    print(time_list)

