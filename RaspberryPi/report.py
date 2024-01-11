import os
import time
from twilio.rest import Client

account_sid = 'AC89e8a032aebf2f25740ef8da9363c3fc'
auth_token = '6fc6281d96cb922ba032a53b09f75e17'
from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+41767017159'


client = Client(account_sid,auth_token)
def create_report(counter, neck_counter, hip_ear_counter, folder):
    report_filename = "posture_report.txt"
    full_report_path = os.path.join(folder, report_filename)

    print("New report: ", report_filename)
    creation_time = time.strftime("%Y-%m-%d %H:%M:%S")
    comment = ""
    if counter == 0:
        comment = "You had perfect posture"
    elif neck_counter > hip_ear_counter:
        comment = "Your main issue seems to be the neck inclination.\nTry to keep you head upright in your next Pomodoro-Session.\nYou might want to consider the following exercises for your neck: https://www.dcorthodocs.com/docs/oms/Neck%20Stretches.pdf"
    elif neck_counter == hip_ear_counter:
        comment = "You seem to have posture issues with your neck inclination and your troso inclination.\n Try to keep your head, shoulders & hips in one line.\nou might want to consider the following exercises for your neck and torso: https://www.dcorthodocs.com/docs/oms/Neck%20Stretches.pdf"
    else:
        comment = "Your main issue seems to be the torso inclination.\nTry to sit upright and align your hips and shoulders in your next Pomodoro-Session.\nYou might want to consider the following exercises for your torso: https://www.versusarthritis.org/media/21786/backpain-exercise-sheet.pdf"

    with open(full_report_path, "w") as report_file:
        report_file.write("Posture Detection Report\n")
        report_file.write("------------------------\n")
        report_file.write(f"Date and Time of this report:{creation_time}\n\n")
        report_file.write("------------------------\n")
        report_file.write(f"Total Bad Postures: {counter}\n")
        report_file.write(f"Bad Neck Postures: {neck_counter}\n")
        report_file.write(f"Bad Hip-Ear Postures: {hip_ear_counter}\n")
        report_file.write("------------------------\n\n")
        report_file.write(f"{comment}")

    print(f"Report generated and saved to {full_report_path}")
    
    whatsapp_message = f"Posture Detetection Report\nTotal Bad Postures: {counter}\nBad Neck Postures: {neck_counter}\nBad Hip-Ear Postures: {hip_ear_counter}\n\n{comment}"
    client.messages.create(
        body=whatsapp_message,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )   

    print("Whatsapp message sent successfully.")
