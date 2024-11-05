import os  # accessing the os functions
import check_camera
import Capture_Image
import Train_Image
import Recognize

def title_bar():
    os.system('cls')  # for windows
    print("\t**********************************************")
    print("\t***** Face Recognition Attendance System *****")
    print("\t**********************************************")

def mainMenu():
    title_bar()
    print()
    print(10 * "*", "WELCOME MENU", 10 * "*")
    print("[1] Check Camera")
    print("[2] Capture Faces")
    print("[3] Train Images")
    print("[4] Recognize & Attendance")
    print("[5] Auto Mail")
    print("[6] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                checkCamera()
            elif choice == 2:
                CaptureFaces()
            elif choice == 3:
                Trainimages()
            elif choice == 4:
                RecognizeFaces()
            elif choice == 5:
                sendEmail()
            elif choice == 6:
                print("Thank You for using the system!")
                break
            else:
                print("Invalid Choice. Please enter a number between 1-6.")
        except ValueError:
            print("Invalid input. Please enter a valid number (1-6).")

def checkCamera():
    check_camera.camer()
    input("Camera check completed. Press any key to return to the main menu.")
    mainMenu()

def CaptureFaces():
    Id = input("Enter ID: ")
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    Capture_Image.takeImages(Id, name, email)
    input("Faces captured successfully. Press any key to return to the main menu.")
    mainMenu()

def Trainimages():
    Train_Image.TrainImages()
    input("Images trained successfully. Press any key to return to the main menu.")
    mainMenu()

def RecognizeFaces():
    Recognize.recognize_attendence()
    input("Recognition completed. Press any key to return to the main menu.")
    mainMenu()

def sendEmail():
    # Execute the automail script and check for successful execution
    try:
        result = os.system("python automail.py")
        if result == 0:
            print("Email sent successfully!")
        else:
            print("An error occurred while sending the email.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    input("Press any key to return to the main menu.")
    mainMenu()

# Start the program
mainMenu()
