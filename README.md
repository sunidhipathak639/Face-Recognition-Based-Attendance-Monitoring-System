Face Recognition Attendance Management System
Overview
This project is an Attendance Management System based on Face Recognition, developed using Python and OpenCV. It helps automate the process of taking attendance by recognizing faces using a trained model.

Technologies Used:
OpenCV (pip install opencv-python): For face detection and image processing.
Tkinter: For building the GUI interface (Available by default in Python).
Pillow (pip install Pillow): For image manipulation.
Pandas (pip install pandas): For handling and saving data in CSV format.
Steps to Set Up the System:
Download the Repository:

Clone or download the project repository to your local machine.
Create the TrainingImage Folder:

Create a folder named TrainingImage inside the project directory. This folder will store the images of faces captured for training the model.
Set the Correct Paths:

Open the AMS_Run.py file and update all paths (like haarcascade_frontalface_default.xml, and any file paths) to match your local system's directory structure.
Run the System:

Execute the AMS_Run.py file to run the system.
How the System Works:
Collecting Face Data:

Open the GUI and enter your ID and Name in the input boxes.
Click on the Take Images button. The system will capture 200 images of your face and store them in the TrainingImage folder.
Training the Model:

After collecting the images, click the Train Image button. The system will use the collected images to train the Face Recognition Model.
Training takes approximately 5-10 minutes (for training 10 people's data).
Automatic Attendance:

After training, click on the Automatic Attendance button. The system will automatically recognize faces and mark attendance based on the trained model.
Attendance is saved in a .csv file, which includes the ID, Name, Time, and Subject.
Manually Filling Attendance:

The system also has a Manually Fill Attendance button. This allows you to manually mark attendance without face recognition, which will also generate a .csv file and store the data in a database (if connected).
Database Setup (Optional):
If you want to store attendance in a database, you will need WAMP Server or any other local database server.
Install WAMP Server, create a database, and then change the DB name in the AMS_Run.py file to match your database name.
The system can then store the attendance data directly in the database.
Notes:
High Processing Power Required: The system requires good processing power for face recognition, especially if you have a large number of students. It is recommended to use a system with at least 8 GB RAM.
Image Quality: The accuracy of face recognition may reduce with noisy images or low-quality images. Ensure that the faces are clear and visible while capturing images.
Created by:
Sunidhi Pathak

