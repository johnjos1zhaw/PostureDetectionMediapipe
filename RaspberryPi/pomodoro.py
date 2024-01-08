import cv2
import os
import mediapipe as mp
import socket
import struct
import time
import numpy as np
import math as m
from report import create_report
from sense_hat import SenseHat
 
 
sense = SenseHat()
 
def pomodoro():
    # Function to calculate angle
    def findAngle(x1, y1, x2, y2):
        theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
        degree = int(180 / m.pi) * theta
        return degree
 
    # Start cv2 video capturing through CSI port
    cap = cv2.VideoCapture(0)
 
    # Initialise Media Pipe Pose features
    mp_pose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    pose = mp_pose.Pose()
 
    # Create a socket connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    # Debugging Output
    print("Connecting to the server...")
 
    try:
        client_socket.connect(('your_laptop_ip', 8000))  # Replace 'your_laptop_ip' with your laptop's IPv4 address
        connection = client_socket.makefile('wb')
 
        # Debugging Output
        print("Connected to the server")
 
        # CONSTANTS and INITIALIZATIONS
        HIP_EAR_ANGLE_THRESHOLD = 14  # Adjust the threshold
        NECK_INCLINATION_THRESHOLD = 152
        POMODORO_DURATION = 1 * 60  # 1 minute for testing
        bad_counter = 0
        bad_hip_ear_counter = 0
        bad_neck_inclination_counter = 0
        bad_posture = ""
 
        start_time = time.time()
        last_bad_posture_time = 0  # Initialize the last bad posture time
 
        sense = SenseHat()
       
        def create_session_folder():
        # Create a timestamp for the session
            time_folder = time.strftime("%Y%m%d%H%M%S")
            bad_posture_path = "/home/pi/Desktop/MQTT/PostureDetection/Bad_posture_img/"
            # Create a folder for the session
            new_session_folder = os.path.join(bad_posture_path, f"{time_folder}/")
            os.makedirs(new_session_folder, exist_ok=True)
            return new_session_folder
        
        new_session_folder = create_session_folder()
        picture_folder = new_session_folder
        # Main loop
        while time.time() - start_time < POMODORO_DURATION:
            ret, frame = cap.read()
            flipped = cv2.flip(frame, flipCode=1)
            frame1 = cv2.resize(flipped, (640, 480))
            rgb_img = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb_img)
 
            try:
                if result.pose_landmarks:
                    try:
                        nose_x = result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * 640
                        nose_y = result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * 480
                        print('X Coords are', nose_x)
                        print('Y Coords are', nose_y)
                    except AttributeError:
                        print("AttributeError: 'NoneType' object has no attribute 'landmark'")
            except Exception as e:
                print(f"Error processing frame: {e}")
 
            mpDraw.draw_landmarks(frame1, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
 
            if result.pose_landmarks:
                right_ear_x = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x * 640)
                right_ear_y = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y * 480)
                right_hip_x = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * 640)
                right_hip_y = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * 480)
                right_shoulder_x = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * 640)
                right_shoulder_y = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * 480)
 
                neck_inclination = findAngle(right_ear_x, right_ear_y, right_shoulder_x, right_shoulder_y)
                hip_ear_inclination = findAngle(right_hip_x, right_hip_y, right_ear_x, right_ear_y)
 
                # Additional visualization for good and bad posture
                if (
                    hip_ear_inclination < HIP_EAR_ANGLE_THRESHOLD and
                    neck_inclination > NECK_INCLINATION_THRESHOLD
                ):
                    cv2.putText(frame1, "Good Posture", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    sense.clear()  # Clear Sense HAT LEDs for good posture
                else:
                   
                    sense.clear(255, 0, 0)
                    # Draw lines for neck_inclination and torso_inclination
                    neck_line_end_x = int(right_ear_x - 100 * m.cos(m.radians(neck_inclination)))
                    neck_line_end_y = int(right_ear_y - 100 * m.sin(m.radians(neck_inclination)))
                    cv2.line(frame1, (right_ear_x, right_ear_y), (neck_line_end_x, neck_line_end_y), (0, 255, 0), 2)
                    cv2.putText(frame1, f"Neck Angle: {neck_inclination:.2f}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
 
                    # Draw lines for ear, shoulder, and hip
                    cv2.line(frame1, (int(right_ear_x), int(right_ear_y)), (int(right_shoulder_x), int(right_shoulder_y)), (255, 0, 0), 2)
                    cv2.line(frame1, (int(right_shoulder_x), int(right_shoulder_y)), (int(right_hip_x), int(right_hip_y)), (255, 0, 0), 2)
                    cv2.line(frame1, (int(right_ear_x), int(right_ear_y)), (int(right_hip_x), int(right_hip_y)), (255, 0, 0), 2)
                    cv2.putText(frame1, f"Hip-Ear Angle: {findAngle(right_hip_x, right_hip_y, right_ear_x, right_ear_y):.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame1, f"{bad_posture}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)                    
 
                    is_bad_neck_inclination = neck_inclination > NECK_INCLINATION_THRESHOLD
                    is_bad_hip_ear_alignment = hip_ear_inclination < HIP_EAR_ANGLE_THRESHOLD
 
                    # Detecting any bad posture (general bad posture condition)
                    if is_bad_neck_inclination or is_bad_hip_ear_alignment:
                        # Logic for taking action on bad posture detection, such as saving images or sending alerts
                        if time.time() - last_bad_posture_time > 5:
                            bad_counter += 1  
                            if is_bad_neck_inclination:
                                bad_posture = "Bad posture"
                                bad_neck_inclination_counter += 1  # Increment specific bad posture counter for neck
 
                            if is_bad_hip_ear_alignment:
                                bad_posture = "Bad posture"
                                bad_hip_ear_counter += 1  # Increment specific bad posture counter for hip-ear
                            
                            timestamp = time.strftime("%Y%m%d%H%M%S")
                            cv2.imwrite(picture_folder + f"bad_posture_{timestamp}.jpg", frame1)                            
                            last_bad_posture_time = time.time()
 
            # Encode and send the frame to the laptop
            _, buffer = cv2.imencode('.jpg', frame1)
            data = np.array(buffer).tostring()
            connection.write(struct.pack('<L', len(data)) + data)
 
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
 
    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing the connection")
        cap.release()
        client_socket.close()
        sense.clear()
        create_report(bad_counter, bad_neck_inclination_counter,bad_hip_ear_counter, picture_folder)