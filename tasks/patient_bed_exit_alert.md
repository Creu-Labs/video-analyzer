# Patient Bed-Exit Alert

**Description:** This task monitors a patient in a hospital bed. It is designed to send an immediate alert if the patient moves from a safe position (lying or sitting in bed) to a high-risk position (attempting to stand or leave the bed).

**Criteria to Look For (in each frame):**

* **Objects:** 'Patient', 'Bed' (as a defined zone).
* **Patient Pose:** 'Hips', 'Legs', 'Feet'.
* **Safe State:** The patient's 'Hips' are on the 'Bed' AND their 'Feet' are on the 'Bed'.
* **Risk State:** The patient's 'Hips' are at the edge of or off the 'Bed' AND one or both 'Feet' are on the floor.
* **Trigger:** Send an "Alert" for any frame where the 'Risk State' is true.