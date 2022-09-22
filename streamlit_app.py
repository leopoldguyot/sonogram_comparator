from matplotlib.axes import Axes
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment


def graph_spectrogram(wav_file, title, color):
    global frequency_scale
    y, sr = librosa.load(wav_file)
    D = librosa.stft(y) #computing the short-time Fourier transform
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max) #converting in dB
    fig, axes = plt.subplots() #make the "foundation" of the plot

    img = librosa.display.specshow(
        S_db,
        cmap = color,
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
    color_1 = st.selectbox(
        "Choose a color patern",
        ("gray_r", "magma", "CMRmap","viridis","winter")
    )
    frequency_scale = st.selectbox(
        "Choose the frequency scale",
        ("linear", "log")
    )
    second_spectro = st.checkbox("Add an other spectrogram")
    if second_spectro:
        uploaded_file_2 = st.file_uploader(label= "add a second sample" ,type = ".wav", help = "Watchout, large files can take a long time to be proccessed")
        color_2 = st.selectbox(
            "Choose a color patern for the second spectrogram",
            ("gray_r", "magma", "CMRmap","viridis","winter")
        )
        frequency_scale_2 = st.selectbox(
            "Choose the frequency scale for the second spectrogram",
            ("linear", "log")
        )
    

st.write('''
    ## A simple sonograph maker made in python
    Using the Streamlit API
    ''')


col1, col2 = st.columns(2)


with col1:
    
    if example : 
        with st.spinner("Processing"):
            st.write("Willow tit")
            st.audio("willow_tit.wav", format = 'audio/wav')
            st.pyplot(graph_spectrogram("willow_tit.wav", "Willow tit", color_1))    
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
            st.write(uploaded_file.name)
            st.audio(uploaded_file, format = 'audio/wav')
            st.pyplot(graph_spectrogram(uploaded_file,"First sample", color_1)) 
        st.success("Done!")
        with open("sonogram.png", "rb") as file:
            btn = st.download_button(
                label="Download spectrogram",
                data=file,
                file_name="sonogram.png",
                mime="image/png"
            )


with col2:
    if second_spectro and uploaded_file_2 :
        with st.spinner("Processing..."):
            st.write(uploaded_file_2.name)
            st.audio(uploaded_file_2, format = 'audio/wav')
            st.pyplot(graph_spectrogram(uploaded_file_2,"Second sample", color_2)) 
        st.success("Done!")
        with open("sonogram.png", "rb") as file:
            btn = st.download_button(
                label="Download spectrogram",
                data=file,
                file_name="sonogram.png",
                mime="image/png"
            )


#allow the pnj to be stocked in te cache and settings
#allow to view the first plot in full size
#todo allow more example (maybe one for each bird call in belgium) -> only interesting parts selectionned
