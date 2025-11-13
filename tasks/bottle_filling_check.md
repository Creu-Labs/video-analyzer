# Assembly Line: Bottle Filling Check

**Description:** This task monitors a beverage filling line to identify bottles that are underfilled or overfilled.

**Criteria to Look For (in each frame):**

* **Objects:** 'Bottle'.
* **Zones:** A static 'Target Fill Line' (defined as a line or narrow band).
* **Properties:** The 'Liquid Level' inside the bottle.
* **Motion State:** The 'Liquid Level' is 'Rising' (being filled) or 'Stable' (filling complete).
* **Trigger (Underfill):** Log an "Underfill Error" if the 'Liquid Level' is 'Stable' AND it is *below* the 'Target Fill Line'.
* **Trigger (Overfill):** Log an "Overfill Error" if the 'Liquid Level' (at any point) rises *above* the 'Target Fill Line'.