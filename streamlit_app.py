import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def graph_spectrogram(wav_file):
    y, sr = librosa.load(wav_file)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(S_db, ax=ax)
    fig.colorbar(img, ax=ax)
    
    return plt.gcf()

st.markdown('''
    ## A simple sonograph maker made in python
    using the streamlit API
    ''')

with st.sidebar:
    st.write(''' 
    # Some settings :
    ''')
    uploaded_file = st.file_uploader("",type = ".wav")
    example = st.checkbox("use an example file (willow tit)")


if example : 
    st.audio("willow_tit.wav", format = 'audio/wav')
    st.pyplot(graph_spectrogram("willow_tit.wav"))    

elif uploaded_file :
    st.audio(uploaded_file, format = 'audio/wav')
    st.pyplot(graph_spectrogram(uploaded_file)) 
    
#todo a download button for image output
#todo allow interaction with figure ?
#todo comparaison between spectrograms
#todo allow more example (maybe one for each bird call in belgium) -> only interesting parts selectionned





