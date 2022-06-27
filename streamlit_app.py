from matplotlib.axes import Axes
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment


def graph_spectrogram(wav_file, title):
    global frequency_scale
    y, sr = librosa.load(wav_file)
    D = librosa.stft(y) #computing the short-time Fourier transform
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max) #converting in dB
    fig, axes = plt.subplots() #make the "foundation" of the plot

    img = librosa.display.specshow(
        S_db,
        x_axis = "time",
        y_axis = frequency_scale,
        ax = axes 
    )

    axes.set(title = title)
    fig.colorbar(img, ax = axes,  format = "%3.f dB")
    plt.savefig("sonogram.png")
    return plt.gcf()


with st.sidebar:
    st.write(''' 
    # Some settings :
    ''')
    uploaded_file = st.file_uploader(label= "" ,type = ".wav", help = "Watchout, large files can take a long time to be proccessed")
    example = st.checkbox("Use an example file (Willow tit)")
    frequency_scale = st.selectbox(
        "Choose the frequency scale",
        ("linear", "log")
    )


st.write('''
    ## A simple sonograph maker made in python
    Using the Streamlit API
    ''')


if example : 
    with st.spinner("Processing"):
        st.audio("willow_tit.wav", format = 'audio/wav')
        st.pyplot(graph_spectrogram("willow_tit.wav", "Willow tit"))    
    st.success("Done!")
    with open("sonogram.png", "rb") as file:
     btn = st.download_button(
             label="Download spectrogram",
             data=file,
             file_name="sonogram.png",
             mime="image/png"
           )
           
elif uploaded_file :
    with st.spinner("Processing..."):
        st.audio(uploaded_file, format = 'audio/wav')
        st.pyplot(graph_spectrogram(uploaded_file,"Sample")) 
    st.success("Done!")
    with open("sonogram.png", "rb") as file:
     btn = st.download_button(
             label="Download spectrogram",
             data=file,
             file_name="sonogram.png",
             mime="image/png"
           )

#allow the pnj to be stocked in te cache
#todo a download button for image output
#todo allow interaction with figure ?
#todo comparaison between spectrograms
#todo allow more example (maybe one for each bird call in belgium) -> only interesting parts selectionned
