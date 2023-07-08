# import the required libraries
import board
import analogio
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
mic1_current_raw_data = 0
mic1_current_filtered_data=0
mic2_previous_raw_data = 0
mic2_previous_filtered_data = 0
mic2_current_raw_data = 0
mic2_current_filtered_data=0

# set the analog pins for the microphones
mic1_pin = analogio.AnalogIn(board.A0) # user mic
mic2_pin = analogio.AnalogIn(board.A1) # ambient mic

current_time = time.monotonic() # store the current time
start_time = time.monotonic() # store the time just before starting the data collection

# create empty arrays to append microphone values and the corresponding time frame
mic1_data = []
mic2_data = []
time_data = []

# open a file to store the microphone data
with open("data_log.txt","a") as f:
    while True:
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
            current_time = time.monotonic()
            mic1_peak_to_peak_signal = mic1_signal_max - mic1_signal_min
            mic2_peak_to_peak_signal = mic2_signal_max - mic2_signal_min
            mic1_voltage = (mic1_peak_to_peak_signal * 3.3) / 65536
            mic1_current_raw_data = mic1_voltage
            # filter for microphone 1 (user mic). Low pass first order filter 200Hz. sampling frequency 7000Hz
            mic1_current_filtered_data = 0.83526683*mic1_previous_filtered_data + 0.08236658*mic1_current_raw_data + 0.08236658*mic1_current_raw_data
            mic1_current_raw_data = mic1_current_raw_data
            mic1_previous_filtered_data = mic1_current_filtered_data
            mic2_voltage = (mic2_peak_to_peak_signal * 3.3) / 65536
            mic2_current_raw_data = mic2_voltage
            # filter for microphone 2 (ambient mic). Low pass first order filter 500Hz sampling frequency 30000Hz
            mic2_current_filtered_data = 0.90049055*mic2_previous_filtered_data + 0.04975473*mic2_current_raw_data + 0.04975473*mic2_current_raw_data
            mic2_current_raw_data = mic2_current_raw_data
            mic2_previous_filtered_data = mic2_current_filtered_data
            print((mic1_current_filtered_data, mic2_current_filtered_data))
            current_time = time.monotonic() # update current time
            # reset variables again for the next iteration
            mic1_peak_to_peak_signal, mic2_peak_to_peak_signal = 0, 0
            mic1_voltage, mic2_voltage = 0, 0
            mic1_signal_max, mic2_signal_max = 0, 0
            mic1_signal_min, mic2_signal_min = 65536, 65536
            # append filtered microphones values and the corresponding time to the arrays
            mic1_data.append(mic1_current_filtered_data)
            mic2_data.append(mic2_current_filtered_data)
            time_data.append(current_time)
        if time.monotonic()-start_time >30:
            # after 30 seconds write the values stored in the array in the file and exit
            f.write(str(mic1_data))
            f.write(str(mic2_data))
            f.write(str(time_data))
            break





