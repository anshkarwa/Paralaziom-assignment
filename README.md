Problem 1: COCO

2. How would you split this dataset into train/val/test while preserving category balance?

   
Ans : Randomly splitting a COCO dataset is risky, as it can create unbalanced training and test sets where rare objects are missing from one split. For reliable results, you need to preserve the category distribution.
The best approach is stratified sampling. Since images have multiple labels, use a technique called "iterative stratification" (found in libraries like scikit-multilearn). This method intelligently assigns images, prioritizing rare categories to ensure they are fairly distributed across your train, validation, and test sets. Finally, create a new, self-contained JSON file for each split, containing only its assigned images and annotations.

Because images can have multiple labels (e.g., a "cat" and a "sofa"), a simple split won't work. The best tool for the job is a clever technique called iterative stratification. You can find this in libraries like scikit-multilearn.
Here's the gist of how it works:
Map it out: First, the tool figures out which objects appear in every single image.
Handle the rare stuff first: It looks for the rarest categories or combinations of categories and deals them out first, making sure every split gets its fair share.
Iterate and balance: It then keeps assigning the rest of the images one by one, constantly checking and adjusting to keep the overall category balance as perfect as possible.

Once the algorithm tells you which image IDs belong in your train, validation, and test sets, the final step is to create three brand-new COCO JSON files.
For each split (train, val, test), you'll create a new JSON file that:
Copies the original info and categories sections.
Includes only the images that were assigned to that split.
Includes only the annotations that belong to those specific images.

3. How would you detect duplicate annotations in a COCO dataset? What fields would you compare?


Ans : A duplicate annotation is when the exact same object in the same image is labeled more than once.
To catch them, you check for annotations that are identical in a few key ways:
image_id: They're in the same image.
category_id: They're the same type of object.
bbox: The bounding box coordinates are exactly the same.
The efficient way to find them:
Keep an empty set to track annotations you've already seen.
Go through every annotation.
For each one, create a unique key, like a tuple: (image_id, category_id, bbox).
If that key is already in your set, it’s a duplicate! You can flag it for removal.
If not, add the key to the set.
This method is great for perfect duplicates. Finding near-duplicates (where boxes are off by a few pixels) requires a more complex approach, like checking for high Intersection over Union (IoU).

4. Find out if there is class imbalance here.


Ans : Yes, we can tell whether there is class imbalance by checking how many annotations exist for each category.

Annotation Counts per Category:
These are the counts for all good annotations in your dataset, sorted from most to least frequent:

bicycle: 32
fire hydrant: 32
car: 31
person: 31
dog: 29
traffic light: 29
truck: 28
cat: 27
bench: 27
bus: 24

Conclusion:
There is a very slight class imbalance, but the dataset overall is fairly well-balanced.

The most common categories ("bicycle," "fire hydrant") occur 32 times, while the least common category ("bus") occurs 24 times. The ratio of the most common to the least common class is only 1.33-to-1 (32 / 24). In actual dataset applications, ratios of 10-to-1 and even 100-to-1 can be common. Since all classes are well-served with an equal number of samples, this dataset would not need special methods (such as over-sampling or loss weighting) to cope with class imbalance.
