import json
import hashlib
from collections import OrderedDict
import argparse

# recursively reduces a JSON-like structure to retain only unique key structures at each level.
def reduce_json_structure(data):
     
    if isinstance(data, dict): # if the data structure is a dictionary
        reduced_dict = {} # store the reduced structures
        unique_structures = [] # stores unique key-value pairs 
        seen_structures = set() # keeps track of seen key sets to eliminate duplicates
        
        # recursively process all values first
        for key, value in data.items():
            reduced_value = reduce_json_structure(value)  # reduce nested structures
            reduced_dict[key] = reduced_value # store the processed value 
            
        # identify and keep unique key structures 
        for key, value in reduced_dict.items():
            structure_signature = frozenset(value.keys()) if isinstance(value, dict) else None
            # keep structures with unique key sets or non-dict values 
            if structure_signature is None or structure_signature not in seen_structures:
                seen_structures.add(structure_signature)
                unique_structures.append((key, value))
        
        return dict(unique_structures) # return the filtered dictionary
    
    elif isinstance(data, list): # if the data structure is a list
        reduced_list = [reduce_json_structure(item) for item in data] # reduce each list item
        unique_items = [] # stores unique items
        seen_structures = set() # keeps track of seen key sets
        
        # identify and keep unique structures in the list 
        for item in reduced_list:
            structure_signature = frozenset(item.keys()) if isinstance(item, dict) else None
            # keep structures with unique key sets or non-dict values 
            if structure_signature is None or structure_signature not in seen_structures:
                seen_structures.add(structure_signature)
                unique_items.append(item)
        
        return unique_items # return the filtered list 
    
    return data  # return as-is if not a dict or list

# reads a JSON file, processes it, and writes the unique structures to a new JSON file. 
def main(input_file, output_file):
    
    # open and load the input JSON file 
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # ensure the input is a list of objects; otherwise, raise error
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of objects.")
    
    # process the JSON file to filter for unique structures 
    unique_data = reduce_json_structure(data)
    
    # save the filtered, unique structures to an output file 
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_data, f, indent=4)
    
    print(f"Reduced JSON saved to {output_file}")

if __name__ == "__main__":
    # set up command line argument parsing 
    parser = argparse.ArgumentParser(description="Reduce JSON to unique structures.")
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("output_file", help="Path to output JSON file")
    args = parser.parse_args()
    
    # execute the main function with the provided arguments 
    main(args.input_file, args.output_file)