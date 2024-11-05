import os
import pandas as pd
def cal():
    fp=os.getcwd()+os.sep+"Attendance"
    no=len(os.listdir(fp))
    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
    col_names = ['Id','Name','Email','number_of_classes','Attendance_Percentage']
    attendance = pd.DataFrame(columns=col_names)
    for index,row in df.iterrows():
        noc=row['number_of_classes']
        ap=(noc*100)//no
        a=row['Id']
        b=row['Name']
        c=row['Email']
        d=row['number_of_classes']
        e=ap
        attendance.loc[len(attendance)] = [a,b,c,d,e]
    print(attendance) 
    attendance.to_csv("StudentDetails\StudentDetails.csv",index=False)
