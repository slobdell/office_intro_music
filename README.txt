1. Install all required dependencies
-OpenCV
-NumPy
-gPhoto2
-Boost.Python

2. Adjust the Makefile in ./camera_input to your particular environment
3. Run "make" inside of the camera_input folder
4. Run "python collect_training_data.py"
5. You will need to manually classify each face in the "faces" directory.
-Classify by creating a folder name that matches the individual's name
-Create at least two folders and place the faces into the appropriate folder
6. Update your engineer list in "engineer_list.py" to include the names of the appropriate people and associated songs and make them match the directores in "faces"
7. After a fair amount of training data collected from "collect_training_data.py", run "predict_faces.py"
8. To re-train the classifier, which might take a significant amount of time, run "retrain_recognizer.py"
