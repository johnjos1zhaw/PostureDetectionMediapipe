### Posture Detection with Mediapipe on the Raspberry Pi 4

#### What is this?

This project utilizes the Mediapipe library to perform real-time posture detection using the Raspberry Pi camera. The system helps users maintain better posture during work sessions, combining posture assessment with the Pomodoro Technique for effective time management.

#### What can this help with?

1. **Pomodoro Technique Integration:** The system seamlessly integrates with the Pomodoro Technique, a time management method that enhances productivity. Users can initiate Pomodoro sessions with posture monitoring to boost focus and avoid burnout.

2. **Posture Improvement:** By providing real-time feedback on posture, the system assists users in maintaining a healthy sitting position. The accompanying posture report and images offer insights into specific areas of improvement.

#### Python Version

- **Raspberry Pi:** Python 3.7.3
- **Laptop:** Python 3.9

#### Installation

1. Clone the repository to your Raspberry Pi and laptop:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install required packages on the Raspberry Pi:

   ```bash
   sudo pip install -r sudo_requirements.txt
   ```

3. Install required packages on your laptop:

   ```bash
   pip install -r requirements.txt
   ```

4. Find your Raspberry Pi's IP address:

   ```bash
   ifconfig
   ```

   Copy the IPv4 address into the `pomodoro.py` file.

#### Running the System

1. Run `receiver.py` on your laptop:

   ```bash
   python receiver.py
   ```

2. Run `main.py` on the Raspberry Pi:

   ```bash
   python main.py
   ```

3. Start the Pomodoro session by pressing the Sense HAT stick in the middle.

   - **Note:** The session duration is currently set to 60 seconds for testing purposes. Adjust it to 25 minutes for a real Pomodoro session.

#### Pomodoro Technique

The Pomodoro Technique is a time management method that uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. It promotes sustained focus and productivity while avoiding burnout.
