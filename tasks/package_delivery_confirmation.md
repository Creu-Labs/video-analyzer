# Porch Package Delivery Confirmation

**Description:** This task monitors a front porch or designated delivery area to confirm when a package has been successfully delivered and the courier has left. 

**Criteria to Look For (in each frame):**

* **Objects:** 'Person' (courier), 'Package'.
* **Zone:** A 'Delivery Zone' polygon (the porch area).
* **"Delivery in Progress" State:** A 'Person' AND a 'Package' are *both* present inside the 'Delivery Zone'.
* **"Package Delivered" State:** A 'Package' is 'Stationary' inside the 'Delivery Zone' AND no 'Person' is present in the 'Delivery Zone'.
* **Event:** Log a "Delivery Complete" event on the first frame where the '"Package Delivered" State' is true.