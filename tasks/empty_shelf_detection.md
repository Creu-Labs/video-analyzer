# Retail: Empty Shelf Detection

**Description:** This task monitors a specific, high-traffic retail shelf to alert staff when it becomes empty or is close to being empty.

**Criteria to Look For (in each frame):**

* **Zone:** A 'Shelf Zone' polygon, divided into sections (e.g., 'Section A', 'Section B').
* **Objects:** 'Product' (e.g., 'Cereal Box', 'Soda Bottle').
* **Background:** The 'Empty Shelf Background' (the visible back wall of the shelf).
* **Capacity:** Calculate the percentage of the 'Shelf Zone' that is occupied by 'Product' versus the 'Empty Shelf Background'.
* **Trigger:** Send a "Restock Alert - Section A" if the 'Product' occupancy in 'Section A' drops below 15%.