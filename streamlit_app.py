from matplotlib.axes import Axes
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display


names_list = ["Willow tit"]
files_list = ["willow_tit.wav"]


@st.experimental_memo
def graph_sample_sonogram(wav_file, title, color): 
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
    plt.savefig(uploaded_file.name[:-4]+".png")
    return plt.gcf()


@st.experimental_singleton
def graph_reference_sonogram(wav_file, title, color): # draw the graph for the reference file
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
    plt.savefig("sonogram.png") #trouver le nom du fichier
    return plt.gcf()


def reference_file_finder(name):
    i = names_list.index(name)
    return files_list[i]
    #chercher le nom dans une liste et puis sortir le fichier avec l'index dans une autre liste


with st.sidebar:
    st.write(''' 
    # Some settings :
    ''')
    uploaded_file = st.file_uploader(label= "" ,type = ".wav", help = "Watchout, large files can take a long time to be proccessed")

    second_sono = st.checkbox("See reference sonogram")

    if second_sono:
        reference_name = st.selectbox("Choose a reference sonogram",
        ("Willow tit","")
        )

    with st.expander("Customization settings"):
        color = st.selectbox(
            "Choose a color patern",
            ("gray_r", "magma", "CMRmap","viridis","winter")
        )
        frequency_scale = st.selectbox(
            "Choose the frequency scale",
            ("linear", "log")
        )


st.title("Sonogram Comparator")


if uploaded_file and not second_sono:
    with st.spinner("Processing..."):
        st.write(uploaded_file.name)
        st.audio(uploaded_file, format = 'audio/wav')
        st.pyplot(graph_sample_sonogram(uploaded_file,"First sample", color)) 
        st.success("Done!")
    with open(uploaded_file.name[:-4]+".png", "rb") as file:
                btn = st.download_button(
                    label="Download sample sonogram",
                    data=file,
                    file_name=uploaded_file.name[:-4]+".png",
                    mime="image/png"
                )


elif second_sono and not uploaded_file :
            with st.spinner("Processing..."):
                st.write(reference_name)
                reference_file = reference_file_finder(reference_name)
                st.audio(reference_file, format = 'audio/wav')
                st.pyplot(graph_reference_sonogram(reference_file,reference_name, color)) 
                st.success("Done!")
            with open("sonogram.png", "rb") as file:
                btn = st.download_button(
                    label="Download reference sonogram",
                    data=file,
                    file_name= reference_name + ".png",
                    mime="image/png"
                )
    

else :
    col1, col2 = st.columns(2)


    with col1:
        if uploaded_file :
            with st.spinner("Processing..."):
                st.write(uploaded_file.name)
                st.audio(uploaded_file, format = 'audio/wav')
                st.pyplot(graph_sample_sonogram(uploaded_file,"First sample", color)) 
                st.success("Done!")
            with open(uploaded_file.name[:-4]+".png", "rb") as file:
                btn = st.download_button(
                    label="Download sample sonogram",
                    data=file,
                    file_name=uploaded_file.name[:-4]+".png",
                    mime="image/png"
                )


    with col2:
        if second_sono and reference_name :
            with st.spinner("Processing..."):
                st.write(reference_name)
                reference_file = reference_file_finder(reference_name)
                st.audio(reference_file, format = 'audio/wav')
                st.pyplot(graph_reference_sonogram(reference_file,reference_name, color)) 
                st.success("Done!")
            with open("sonogram.png", "rb") as file:
                btn = st.download_button(
                    label="Download reference sonogram",
                    data=file,
                    file_name= reference_name + ".png",
                    mime="image/png"
                )

#todo allow more example (maybe one for each bird call in belgium) -> only interesting parts selectionned
#theming?
