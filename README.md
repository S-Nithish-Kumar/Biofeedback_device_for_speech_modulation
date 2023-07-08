<h2 align="center">Demonstration video</h2>
<p align="center">
<a href="https://www.youtube.com/watch?v=tNjcQhkGpjM&t=10s"><img src="http://img.youtube.com/vi/tNjcQhkGpjM/0.jpg"></a>
</p>

## Contents:
1. Problem Statement
2. Objectives
3. Impact of Solving the Problem
4. Information Processing Model
5. Existing Products
6. Proposed Approach
7. Implementation
8. Testing and Validation
9. Problems and Troubleshooting
10. Results and Conclusion
11. References

### 1. Problem Statement:
- Neurodegenerative diseases such as Parkinson’s disease can cause vocal disorders leading to reduced
motor control for speech modulation due to limited physical sensations of speech.
+ The limited physical sensations of speech are due to the decline in Dopamine responsible for cognition.

### 2. Objectives:
- People with Neuro vocal disorders seem to modulate their voice better during speech exercises under the
supervision of a therapist. It shows that people with such a disorder can respond well to feedback provided
with an assistive device that will substitute for the therapist, enabling individuals to modulate their voices.
+ This project aims to design and develop a prototype for providing vibrotactile feedback based on ambient
noise to modulate the speech intensity of an individual.

### 3. Impact of Solving the Problem:
- Parkinson's disease is a widespread neurodegenerative disorder affecting millions of individuals worldwide.
In the United States alone, it is estimated that approximately one million people are currently living with
Parkinson's disease. However, this number is just a fraction of the global prevalence, as the disease impacts
an estimated ten million individuals worldwide.
+ According to research, 89 percent of people with Parkinson's disease (PD) have speech and vocal impairments,
including hoarseness, breathiness, and a quiet, monotonous voice.
- A biofeedback device to module speech will help approximately 90 percent of the population with Parkinson’s
disease to improve their speech modulation.
* The device is not only useful for people with speech impairments related to PD but is also functional for
other vocal disorders with calibration as per the need.

### 4. Information Processing Model:
#### Information Processing Model – For a normal human being
<p align="center">
<img src="images/information_processing_model_without_parkinson_disease.png" height="70%" width="70%">
</p>

#### Information processing model - For people with Parkinson’s disease
<p align="center">
<img src="images/information_processing_model_with_parkinson_ disease.png" height="70%" width="70%">
</p>


### 5. Existing Products:
#### SpeechVive
<p align="center">
<img src="images/SpeechVive.jpg" height="50%" width="50%">
</p>
- [SpeechVive](http://www.speechvive.com/) is a small, portable device designed to improve speech and voice production in individuals with
Parkinson’s disease. The programmable device is worn behind the ear, like a hearing aid. When the user speaks,
a babbling noise plays in their ear, acting upon a reflex that causes them to speak louder. Because the device
does not require training, it can be successfully used by people with mild cognitive impairment or reduced memory.
+ SpeechVive is designed to improve the vocal loudness and/or speech clarity of individuals with hypophonia,
a common motor speech symptom in people diagnosed with Parkinson’s disease and related diagnoses.
* The SpeechVive device detects when the user speaks and plays background noise, which is an autonomous cue to
elicit louder speech through the Lombard Effect. The Lombard Effect is a well-known phenomenon where speakers
naturally speak louder under background noise. When the user does not speak, SpeechVive does not deliver babble
noise to the ear.

#### Drawbacks of SpeechVive
- SpeechVive is intended to increase the user’s voice level through the Lombard effect, and it cannot provide
feedback to prompt the user to reduce their volume if it’s not at the appropriate level for that ambient condition.
+ High cost.
+ Visible to others.

#### Hi-VOLT
<p align="center">
<img src="images/Hi_VOLT_voice_on_light_bracelet.jpg" height="45%" width="45%">
</p>
- [Hi-VOLT® 4 PD](https://voiceaerobicsdvd.com/product/hi-volt-voice-on-light-bracelet/) is a calibrated, voice-activated light bracelet that can be used by people with PD in and out of
speech and physical therapy. Feedback from the Hi-VOLT® voice-on-light can help the user gauge the level of loudness
required to be understood by others. Since the light is calibrated, users only have to speak loud enough to activate
the light.
+ Hi-VOLT® 4 PD was developed by a speech-language pathologist, Mary Spremulli, and clinical data collected in her
practice over three years on 63 patients has shown that at the time of the initial evaluation, most patients were able
to attain a 7.5 dB increase in sound pressure level in response to the cue: “speak loud enough to activate the light”.
Patients using the Hi-VOLT® light during home practice report that it helps them judge if they are reaching their goals
for a more normal loudness.
* These products are economically priced and reinforce the principles that patients learn in many sessions of prior
voice treatment and now.

#### Drawbacks of Hi-VOLT
- The battery of the device lasts only for 48 hours and is not rechargeable.
- Ambient noise level is not considered for providing feedback.
- Visible to others.

### 6. Proposed Approach:
- Two microphones are used. One microphone will capture the user’s voice, and another will capture ambient noise.
- The signals from these two microphones will be filtered using a low-pass filter to remove spikes, and the filtered
data will be processed to provide feedback to the user.
+ A vibration motor is used to provide vibro-tactile feedback to the user. The vibration motor is tuned to produce
two different types of vibrations. Intermittent vibration prompts the user to reduce the volume, and continuous vibration
makes the user increase their voice.
* All the components will be placed inside a shoulder brace that can be worn on either shoulder.

### 7. Implementation:
#### Circuit Diagram
<p align="center">
<img src="images/circuit_diagram.jpg" height="80%" width="80%">
</p>
- The circuit diagram above shows the components used in the device.
- An adjustable-gain microphone is used as a user microphone. The gain of the user microphone is optimized so that
it will only capture the user's voice and eliminate ambient noise.
+ Though the gain is optimized, the user's microphone will capture some background noise, but it is negligible.
A bone conduction microphone with better sensitivity can help overcome this problem. The bone conduction microphone
can be placed on top of the collarbone, where the sensitivity is better.
* An Auto-gain microphone is used as an ambient microphone. The gain of this microphone adjusts automatically and
is directly proportional to the distance of the sound source. Hence, this microphone is effective at capturing
background noise that is far away.
- Buttons are provided to adjust the intensity of the vibration motor.

#### Working
<p align="center">
<img src="images/overall_sequence_flow_diagram.jpg" height="80%" width="80%">
</p>
- Once the device is turned on, the ambient mic will capture background noise. When the user starts speaking,
the captured background noise is used for comparison with the user’s voice level and provides feedback. The
sequence flow diagram above illustrates the feedback logic of the device.
+ The logic has three different states: high, normal, and low for the user’s voice level, and two discrete
states: noise and no noise for background noise.
* When the user speaks at a low volume, irrespective of ambient noise, continuous vibrotactile feedback will
be generated.
+ When there is no background noise and the user converses in a normal voice, no feedback is provided. But if
the user is conversing in a normal voice in the presence of background noise, continuous feedback will be provided.
- If the user speaks at a high volume in the absence of ambient sound, intermittent vibrotactile feedback will be
provided, prompting the user to reduce their volume. But if ambient noise is present and the user speaks at a high
volume, feedback is not provided.

#### Microphone Data Filtering
Signals from both user and ambient microphones are filtered using first-order low-pass filters to remove noise 
and avoid sudden spikes that could affect the feedback of the device.
<p align="center">
<img src="images/user_mic_raw_and_filtered_data.jpg" height="80%" width="80%">
</p>
<p align="center">
<img src="images/ambient_mic_raw_and_filtered_data.jpg" height="80%" width="80%">
</p>

#### Housing
<p align="center">
<img src="images/component_housing.jpg" height="40%" width="40%">
</p>
As shown in the figure above, all the components are placed inside 3D printed boxes.
<p align="center">
<img src="images/shoulder_brace.jpg" height="40%" width="40%">
</p>

- The shoulder brace shown above is modified to incorporate the device onto the interior surface of the
brace, ensuring that it remains hidden from view. Additionally, the device is removable, allowing users
to detach it during washing, and the shoulder brace is lightweight and flexible to make the user comfortable.
+ The box containing the vibration motor, Battery Management System, ambient microphone, and controller will
be placed inside the shoulder brace, and the brace can be worn on either shoulder.
* The user's microphone placed on top of the collarbone will pick up the user's vocal intensity.
+ Signals from both microphones are filtered using a low-pass filter to avoid spikes. Both these signals are
used in determining the user's and ambient sound levels for providing feedback.
- The intensity of the vibration motor can be adjusted using the buttons provided based on the user’s convenience.
The device comes with a rechargeable battery and a battery life of 12 hours on a single charge.
* The primary aim of designing the device is to ensure user-friendliness and accessibility with minimal effort
and disturbance to the wearer. The shoulder brace is adjustable to accommodate all body types comfortably.

<p align="center">
<img src="images/shoulder_brace_under_regular_attire.jpg" height="40%" width="40%">
</p>

As shown in the figure above, the shoulder brace is hidden under regular attire.

### 8. Testing and Validation:
- The device was tested with four people with varying voice levels.
- The user is asked to position the user microphone at the appropriate position near the face, and the ambient
microphone is placed on the shoulder. The user is made to speak at three different voice levels: low, medium,
and high.
-  As said before, all the users have significantly varying voice levels, and the device can provide proper
feedback to different users with varying voice and ambient sound levels. It showed that the device could
be used by a wide.
+ However, tuning the device for each specific user enhances the accuracy of the feedback provided by the device.

### 9. Problems and Troubleshooting:
- The auto-gain microphone, which is used for capturing background noise, provides negative values for certain
periods of time when there is a sudden change in the sound level. This has a huge negative impact on feedback.
To overcome this problem, a counter is added, which makes the controller more stable, but this increases the
feedback delay to some extent.
+ Though the gain of the user microphone is set to minimum to capture only the user’s voice, at higher background
noise levels it captures some of the ambient noise, which affects the feedback. The user's microphone is surrounded
by a sponge material to reduce the intensity of the noise captured by it.
* Even if the user speaks in a normal voice, at the start and end of each word, the voice level falls below the
low band level of the controller. This triggers the controller to provide false feedback. Counters are used to
overcome this problem, but with a slight increase in feedback delay.

### 10. Results and Conclusion:
- The device was found to perform with reasonable accuracy and delay for a range of people with varying voice levels.
- Replacing the electret microphone with a bone conduction microphone for the receiving user’s voice will help in
avoiding ambient noise.
+ From the testing, it has been found that tuning the device for each user will improve the accuracy and response
time of the device.
* The shoulder is tested with people of varying body sizes and shapes and is found to be comfortable for
day-to-day activities.













