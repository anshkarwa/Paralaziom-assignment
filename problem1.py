import json

def get_coco_summary(json_path):
    """
    Quick script to get a feel for a COCO dataset. It just prints out
    some basic stats like image count and the most common object categories.
    """
    print(f"--- Analyzing {json_path} ---")

    with open(json_path, 'r') as f:
        data = json.load(f)

    # First, let's get the easy stuff
    num_images = len(data.get('images', []))
    all_annotations = data.get('annotations', [])
    num_total_anns = len(all_annotations)

    # Create a simple lookup for category IDs to names, it's just easier this way.
    cat_lookup = {cat['id']: cat['name'] for cat in data.get('categories', [])}

    # Now, let's count how many of each object we have.
    # We'll use a dictionary to store counts: {category_id: count}
    category_counts = {}
    problem_anns = 0 # for annotations that are missing a category ID
    for ann in all_annotations:
        cat_id = ann.get('category_id')
        if cat_id is None:
            problem_anns += 1
            continue
        
        # Add to the count for this category
        category_counts[cat_id] = category_counts.get(cat_id, 0) + 1

    # --- Time to print the results ---
    print(f"\nFound {num_images} images.")
    print(f"Found {num_total_anns} total annotations.")

    if problem_anns > 0:
        print(f"--> Heads up: {problem_anns} annotations were missing a category ID.")

    print("\nTop 3 Most Common Categories:")
    if not category_counts:
        print("Couldn't find any categorized annotations.")
    else:
        # Sort the categories by count to find the most common ones
        sorted_counts = sorted(category_counts.items(), key=lambda item: item[1], reverse=True)
        
        # Print the top 3
        for i, (cat_id, count) in enumerate(sorted_counts[:3]):
            cat_name = cat_lookup.get(cat_id, "Unknown")
            print(f"  {i+1}. {cat_name} ({count} instances)")

    print("\n--- Done ---\n")


# This makes the script runnable from the command line
if __name__ == "__main__":

    file_to_inspect = 'mock_coco.json' 
    get_coco_summary(file_to_inspect)