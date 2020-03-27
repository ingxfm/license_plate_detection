# license-plate-detection-raspberry-pi-3B-plus-OpenAlpr
The aim is to make the code do the following: 
- Function 1: Take images from the live video feed. The live video feed comes from the localhost using the Motion project (https://motion-project.github.io/). 
- Function 2: When the PIR motion sensor senses movement, an image from the live video feed in Function 1 is sent to function 2. Function 2 calls the license plate detection on Function 3. 
- Function 3: This calls OpenAlpr to detect if there is a license plate in the image from Function 2. If there is a license plate the information is saved into a MariaDB local database.
