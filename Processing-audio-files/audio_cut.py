import os
import glob
from pydub import AudioSegment
# import ffmpeg

ten_seconds = 10 * 1000
filepath = r'james_blunt-carry_you_home.mp3'

AudioSegment.converter = r"C:\DiT\PACKAGES\ffmpeg-static\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\DiT\PACKAGES\ffmpeg-static\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\DiT\PACKAGES\ffmpeg-static\bin\ffprobe.exe"




def chunk_file(*file_folder):
    
    
    counter = 1
    for path in file_folder:
    
        audio = AudioSegment.from_mp3(path)
        
        # make path to save chunks in the directory
        try:
            os.mkdir(str(path)+'/chunks'
        except:
            print("Path already exists")

        file_length = len(audio)
        interval = 15*1000 # chuck length is 10 seceonds

        # with overlap as 1s, the chunks will be created;
        # chunk1: 0-10s, chunk2: 9-19, chunk3: 18-28
        overlap = 1000 

        # Initialize start and end seconds to 0 
        start = 0
        end = 0

        # To keep tracks of the end of file 
        flag = 0
                     
        # Iterate using 'intervel' as step
        for i in range(0, 2 * file_length, interval): 

            # This only happens at the beginning of the iteration
            if i == 0: 
                start = 0
                end = interval 

            # set end-overlap at the new start and set start+interval at the new end
            else: 
                start = end - overlap 
                end = start + interval

            # Storing audio file from the defined start to end 
            chunk = audio[start:end] 

            # Filename / Path to store the sliced audio
            if counter < 10:
                filename = 'join/chunk0'+str(counter)+'.wav'
            else:
                filename = 'join/chunk'+str(counter)+'.wav'

            # Store the sliced audio file to the defined path 
            chunk.export(filename, format ="wav") 
            # Print information about the current chunk 
            print("Processing chunk "+str(counter)+". Start = "
                                +str(start)+" end = "+str(end))

            # Check if loop has not  
            if end >= file_length: 
                end = file_length 
                flag = 1
                break

            # Increment counter for the next chunk 
            counter = counter + 1
