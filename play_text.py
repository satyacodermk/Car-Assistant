'''
from gtts import gTTS
from playsound import playsound
'''


#============================= Online making text to voice=> using gtts library =====================

# text_val="All the best for your exam."
# language='en'

# #Passing the text and language to the engine
# #here we have assign slow=False which denotes that the module that the transformed audio should have a high speed
# obj=gTTS(text=text_val,lang=language,slow=False)

# obj.save("exam.mp3")
# #to play the sound
# playsound("exam.mp3")

#============================= Offline making text to voice=> using pyttsx3 =====================
#note that pyttx3 is offline api where gTTS is online api provided by the google
#and this also allow you to no need to save it and no need to play it using playsound() 
#so always better to use it for chat bot or any program were we no need to save it
import pyttsx3

#initialize Test to Speech engine
engine=pyttsx3.init()

#convert this text to speech
text="Python is a great programming language and how are you"

#for changing the rate of speech
#to change the rate of speed as we want  uses setProperty('rate',my_rate) my_rate will assign to the engine and note use it before say() and runAndWait()


#say function is used to add a word to speak to the queue, while the runAndWait() method runs the real event loop until all commands queued up
engine.say(text)

#play the speech
engine.runAndWait()

#to get details of speaking rate of sound
rate=engine.getProperty('rate')
print(rate)



#get details of all voices available
voices=engine.getProperty("voices")
print(voices)
"""
#checking all the voices that are available
index=0
for voice in voices:
    #print(voice,voice.id)
    #printing the voices index 
    print('index->',index," -- ",voice.name)
    index+=1
    engine.setProperty('voice',voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
    """
text="Welcome Sir my name is carvis"
engine.say(text)

engine.runAndWait()