import os
import glob
from pydub import AudioSegment

AudioSegment.converter = r"C:\DiT\PACKAGES\ffmpeg-static\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\DiT\PACKAGES\ffmpeg-static\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\DiT\PACKAGES\ffmpeg-static\bin\ffprobe.exe"


def chunk_file(audio_path, output_path):
    audio = ''
    
    what_file = 1
    counter = 1
    text_file = f'{output_path}/documentation.txt'
    text = open(text_file, 'w+')

    audio_name = audio_path.split("/")[-1]
    print(f"{audio_path} is the audio path")
    text.writelines(f'{audio_name[:-4]}_pt-{what_file} begins at chunk {counter}\n\n')
    print(f"processing {audio_name[:-4]}_trim-{what_file}")

    
    audio = AudioSegment.from_mp3(audio_path)
    file_length = len(audio)
    interval = 15*1000 # chuck length is 10 seceonds

    # with overlap as 1s, the chunks will be created;
    # chunk1: 0-10s, chunk2: 9-19, chunk3: 18-28
    overlap = 2000 

    # Initialize start and end seconds to 0 
    start, end = 0, 0

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
            filename = f"{output_path}/{audio_name[:-4]}_chunk00{counter}.wav"
        elif counter >=10 and counter < 100:
            filename = f"{output_path}/{audio_name[:-4]}_chunk0{counter}.wav"
        else:
            filename = f"{output_path}/{audio_name[:-4]}_chunk{counter}.wav"
        
         # Store the sliced audio file to the defined path 
        chunk.export(filename, format ="wav", bitrate=None) 
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
    
    text.close()


# make folder to save chunk file in the directory
def get_audio_to_chunk(directory):

    files_to_chunk_filepath = f"{directory}/processed_files"
    print(f"{files_to_chunk_filepath} is the file to chunk filepath")
    try:
        list_of_audios = os.listdir(files_to_chunk_filepath)
        os.mkdir(directory + '/chunks')
    except Exception as e:
        print(e)

    for audio in list_of_audios:
        audio_path = f"{files_to_chunk_filepath}/{audio}"

        print(f"the name of the audio is {audio}")
        print(audio_path, '\n\n')
        chunk_file(audio_path, directory + '/chunks')


filepath = "C:\DiT\CS\\Data_Engineer\\Audio-data\\bible"
path_lists = os.listdir(filepath)


for path in path_lists:
    path = f"{filepath}\\{path}"
    get_audio_to_chunk(path)
