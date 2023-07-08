# import the required libraries
import board
import digitalio
import analogio
import pwmio
from adafruit_debouncer import Debouncer
import time

sample_window_time_for_sensors = 0.05 # 50ms sample time. In the 50ms period find the max and min microphone output values
# initialize the microphone minimum and maximum output value variables
mic1_signal_max = 0
mic1_signal_min = 65536
mic2_signal_max = 0
mic2_signal_min = 65536
# initialize microphone output values (voltage)
mic1_previous_raw_data = 0 # raw_data means before filtering
mic1_previous_filtered_data = 0 # filtered_data means after filtering
mic1_current_raw_data=0
mic1_current_filtered_data=0
mic2_previous_raw_data = 0
mic2_previous_filtered_data = 0
mic2_current_raw_data=0
mic2_current_filtered_data=0

# set the pins for motor intensity control buttons
motor_intensity_up_button = digitalio.DigitalInOut(board.D4)
motor_intensity_up_button.direction = digitalio.Direction.INPUT
motor_intensity_up_button.pull = digitalio.Pull.UP
switch_for_motor_intensity_up = Debouncer(motor_intensity_up_button)
motor_intensity_down_button = digitalio.DigitalInOut(board.D5)
motor_intensity_down_button.direction = digitalio.Direction.INPUT
motor_intensity_down_button.pull = digitalio.Pull.UP
switch_for_motor_intensity_down = Debouncer(motor_intensity_down_button)
# set the pwm pin for motor intensity control
motor_control_pin = pwmio.PWMOut(board.A3, duty_cycle=0, frequency=1000, variable_frequency=True)
motor_intensity = 25000 # initial motor intensity

# set the analog pins for the microphones
mic1_pin = analogio.AnalogIn(board.A0) # user mic
mic2_pin = analogio.AnalogIn(board.A1) # ambient mic

current_time = time.monotonic() # store the current time

# initialize the variables for processing the filtered microphone data
high_volume_counter=0
normal_volume_counter=0
low_volume_counter=0
user_voice_counter = 0
ambient_noise_counter = 0
no_ambient_noise_counter = 0
ambient_noise_status=0

# function for continuous vibration feedback
def continuous_feedback():
    global motor_intensity
    motor_control_pin.duty_cycle = motor_intensity
    motor_control_pin.frequency = 2000
    time.sleep(1)
    motor_control_pin.duty_cycle = 0

# function for intermittent vibration feedback
def intermittent_feedback():
    global motor_intensity
    motor_control_pin.duty_cycle = motor_intensity
    motor_control_pin.frequency = 2
    time.sleep(1)
    motor_control_pin.duty_cycle = 0

# function for processing the filtered microphone data
def data_process():
    global high_volume_counter,normal_volume_counter,low_volume_counter,user_voice_counter,ambient_noise_counter,ambient_noise_status,no_ambient_noise_counter
    if(mic1_current_filtered_data>=0.05):
        # if the user's mic output is >=0.05, then the user is considered speaking. The background noise just before the user started to speak will be used here
        print("hello")
        user_voice_counter = user_voice_counter+1
        if(user_voice_counter>=2):
            ambient_noise_counter = 0
            # just because of a spike in the user's microphone signal, it can't be fixed that the user is speaking. So a counter is used. If counter is >=2, then it's confirmed that the user is speaking
            if(mic1_current_filtered_data>0.19):
                # if mic1 data is greater than 0.3, then the volume is high
                high_volume_counter=high_volume_counter+1
                normal_volume_counter=0
                low_volume_counter=0
            elif(mic1_current_filtered_data>=0.09 and mic1_current_filtered_data<=0.18):
                # if the data is between 0.09 and 0.2, then the user is speaking at normal voice. There is a deadzone between the previous condition and this condition to avoid false triggers by the spikes
                high_volume_counter=0
                normal_volume_counter=normal_volume_counter+1
                low_volume_counter=0
                print(normal_volume_counter)
            elif(mic1_current_filtered_data>=0.05 and mic1_current_filtered_data<0.07):
                # if the data is between 0.05 and 0.08, then the user is speaking at low voice. Again there is a small deadzone between the previous and current condition
                high_volume_counter=0
                normal_volume_counter=0
                low_volume_counter=low_volume_counter+1
                #print(low_volume_counter)
            if(user_voice_counter==20):
                # only a chunk of data is consider. Before moving on to the next chunk of data, all the variables are reset
                user_voice_counter=0
                high_volume_counter=0
                normal_volume_counter=0
                low_volume_counter=0
            if(low_volume_counter==18):
                # low_volume_counter equals 18, then the user's voice is low and continuous feedback is sent for one second. To provide this feedback, high counter value is used to avoid false feedback
                low_volume_counter=0
                print("continuous feedback low")
                continuous_feedback()
            elif(high_volume_counter==2 or normal_volume_counter==18):
                # if the user is not speaking in low voice, then other conditions are checked
                if(ambient_noise_status==1 and normal_volume_counter==18):
                    # if the ambient noise is present and the user is speaking in normal volume, then continuous feedback is provided
                    normal_volume_counter=0
                    print("continuous feedback noise")
                    continuous_feedback()
                elif(ambient_noise_status==0 and high_volume_counter==2):
                    # if there is no ambient noise and the user is speaking at high volume, then intermittent feedback is provided, triggering the user to reduce there volume
                    high_volume_counter=0
                    print("Intermittent feedback NO L H")
                    intermittent_feedback()
    elif(mic1_current_filtered_data<0.04): 
        # if the signal from the user's mic is less than 0.5, then ambient microphone's signal will be processed
        ambient_noise_counter = ambient_noise_counter+1
        if(ambient_noise_counter>=3):
            user_voice_counter = 0
            if(ambient_noise_counter==10):
                # after a chuck of data is processed, all the variables are reset
                ambient_noise_counter=0
                no_ambient_noise_counter = 0
            if(mic2_current_filtered_data<0.9):
                # if signal < 0.9, there is no ambient noise
                no_ambient_noise_counter = no_ambient_noise_counter+1
                if(no_ambient_noise_counter>4):
                    ambient_noise_status=0
            elif(mic2_current_filtered_data>=1.0):
                ambient_noise_status=1
                no_ambient_noise_counter = 0


while True:
    switch_for_motor_intensity_up.update()
    switch_for_motor_intensity_down.update()
    # check and update the motor intensity if any of the buttons is pressed
    if switch_for_motor_intensity_up.fell and switch_for_motor_intensity_down.fell:
        print("Both buttons pressed. Do nothing")
    elif switch_for_motor_intensity_up.fell:
        if motor_intensity <35000:
            motor_intensity = motor_intensity+1000
            print("Intensity up",motor_intensity)
    elif switch_for_motor_intensity_down.fell:
        if motor_intensity >15000:
            motor_intensity = motor_intensity-1000
            print("Intensity down",motor_intensity)
    mic1 = mic1_pin.value
    mic2 = mic2_pin.value
    # find the min and max values of the microphone signals
    if mic1 < 65536:
        if mic1 > mic1_signal_max:
            mic1_signal_max = mic1
        elif mic1 < mic1_signal_min:
            mic1_signal_min = mic1
    if mic2 < 65536:
        if mic2 > mic2_signal_max:
            mic2_signal_max = mic2
        elif mic2 < mic2_signal_min:
            mic2_signal_min = mic2
    if (current_time + sample_window_time_for_sensors) < time.monotonic():
        # enter into this block every 50ms
        mic1_peak_to_peak_signal = mic1_signal_max - mic1_signal_min
        mic2_peak_to_peak_signal = mic2_signal_max - mic2_signal_min
        mic1_voltage = (mic1_peak_to_peak_signal * 3.3) / 65536
        mic1_current_raw_data = mic1_voltage
        # filter for microphone 1 (user mic). Low pass first order filter 200Hz. sampling frequency 7000Hz 
        mic1_current_filtered_data = 0.83526683*mic1_previous_filtered_data + 0.08236658*mic1_current_raw_data + 0.08236658*mic1_previous_raw_data
        mic1_previous_raw_data = mic1_current_raw_data
        mic1_previous_filtered_data = mic1_current_filtered_data
        mic2_voltage = (mic2_peak_to_peak_signal * 3.3) / 65536
        mic2_current_raw_data = mic2_voltage
        # filter for microphone 2 (ambient mic). Low pass first order filter 500Hz sampling frequency 30000Hz
        mic2_current_filtered_data = 0.90049055*mic2_previous_filtered_data + 0.04975473*mic2_current_raw_data + 0.04975473*mic2_previous_raw_data
        mic2_previous_raw_data = mic2_current_raw_data
        mic2_previous_filtered_data = mic2_current_filtered_data
        current_time = time.monotonic() # update current time
        # reset variables again for the next iteration
        mic1_peak_to_peak_signal, mic2_peak_to_peak_signal = 0, 0
        mic1_voltage, mic2_voltage = 0, 0
        mic1_signal_max, mic2_signal_max = 0, 0
        mic1_signal_min, mic2_signal_min = 65536, 65536
        print((mic1_current_filtered_data,ambient_noise_status))
        data_process() # call the function to process the signals






