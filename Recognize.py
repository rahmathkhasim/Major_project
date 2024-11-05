import datetime
import os
import time
import calculateAttedance
import cv2
import pandas as pd
import winsound
from csv import writer

# Function to recognize attendance using face recognition
def recognize_attendence():
    # Load the pre-trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel" + os.sep + "Trainner.yml")

    # Load the Haar cascade for face detection
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    # Load the student details CSV file
    df = pd.read_csv("StudentDetails" + os.sep + "StudentDetails.csv")
    
    # Set the font for text on the video stream
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start real-time video capture from the webcam
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # Set video width
    cam.set(4, 480)  # Set video height

    # Define the minimum window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    # Set a minimum threshold for recognition confidence
    minThreshold = 40  # Set to 40 for a good threshold

    try:
        while True:
            # Read a frame from the camera
            ret, im = cam.read()
            if not ret:
                print("Failed to capture image from camera.")
                break

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)

                # Recognize the face and get the confidence value
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                # If confidence is less than 100, it means a match was found
                if conf < 100:
                    aa = df.loc[df['Id'] == Id]['Name'].values
                    confstr = "  {0}%".format(round(100 - conf))
                    tt = str(Id) + "-" + str(aa)
                else:
                    winsound.Beep(500, 2000)  # Beep for unknown faces
                    Id = 'Unknown'
                    tt = str(Id)
                    confstr = "  {0}%".format(round(100 - conf))

                # Log attendance if confidence is above the threshold
                if (100 - conf) > minThreshold and Id != 'Unknown':
                    ts = time.time()
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = str(aa)[2:-2]
                    attendance.loc[len(attendance)] = [Id, aa, timeStamp]
                    tt = tt + " [Pass]"

                # Display the ID and confidence on the video frame
                tt = str(tt)[2:-2]
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 0), 1)

            # Remove duplicates in the attendance log
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

            # Show the frame with face recognition results
            cv2.imshow('Attendance', im)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break

    finally:
        # Always release the camera and close windows, even if an error occurs
        cam.release()
        cv2.destroyAllWindows()

    # Create the file name for saving attendance
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance" + os.sep + "Attendance_" + date + "_" + Hour + ".csv"

    # Save attendance to CSV
    temp = os.getcwd() + os.sep + fileName
    if os.path.exists(temp):
        old_file = pd.read_csv(temp)
        new_file = pd.concat([old_file, attendance])
        new_file.drop_duplicates(subset=['Id'], keep='first', inplace=True)

        # Find new students and update their class count
        y = new_file[~new_file['Id'].isin(old_file['Id'])]
        if not y.empty:
            for index, row in y.iterrows():
                id_value = row["Id"]
                student_index = df.index[df['Id'] == id_value].tolist()[0]
                df.at[student_index, "number_of_classes"] += 1

            df.to_csv("StudentDetails" + os.sep + "StudentDetails.csv", index=False)

        new_file.to_csv(fileName, index=False)
    else:
        attendance.to_csv(fileName, index=False)

        # Update class count for recognized students
        for index, row in attendance.iterrows():
            id_value = row["Id"]
            student_index = df.index[df['Id'] == id_value].tolist()[0]
            df.at[student_index, "number_of_classes"] += 1

        df.to_csv("StudentDetails" + os.sep + "StudentDetails.csv", index=False)

    print("Attendance Successful")

    # Call function to calculate final attendance (if applicable)
    calculateAttedance.cal()