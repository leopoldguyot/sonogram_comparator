import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from files_dictionnary import association


@st.experimental_memo
def graph_sample_sonogram(wav_file, title, color, frq):
    y, sr = librosa.load(wav_file)
    d = librosa.stft(y)  # computing the short-time Fourier transform
    s_db = librosa.amplitude_to_db(np.abs(d), ref=np.max)  # converting in dB
    fig, axes = plt.subplots()  # make the "foundation" of the plot

    img = librosa.display.specshow(
        s_db,
        cmap=color,
        x_axis="time",
        y_axis=frq,
        ax=axes
    )

    axes.set(title=title)
    fig.colorbar(img, ax=axes, format="%3.f dB")
    plt.savefig(uploaded_file.name[:-4] + ".png")
    return plt.gcf()


@st.experimental_singleton
def graph_reference_sonogram(wav_file, title, color, frq):  # draw the graph for the reference file
    y, sr = librosa.load(wav_file)
    d = librosa.stft(y)
    s_db = librosa.amplitude_to_db(np.abs(d), ref=np.max)
    fig, axes = plt.subplots()

    img = librosa.display.specshow(
        s_db,
        cmap=color,
        x_axis="time",
        y_axis=frq,
        ax=axes
    )

    axes.set(title=title)
    fig.colorbar(img, ax=axes, format="%3.f dB")
    plt.savefig("sonogram.png") # mettre le nom en argument
    return plt.gcf()


with st.sidebar:
    st.write(''' 
    # Settings :
    ''')
    uploaded_file = st.file_uploader(label="File selection", type=".wav",
                                     help="Watch-out, large files can take a long time to be processed")

    second_sono = st.checkbox("See reference sonogram")

    if second_sono:
        reference_name = st.selectbox("Choose a reference sonogram",
                                      (association.keys())
                                      )

    with st.expander("Customization settings"):
        clr = st.selectbox(
            "Choose a color pattern",
            ("gray_r", "magma", "CMRmap", "viridis", "winter")
        )
        frequency_scale = st.selectbox(
            "Choose the frequency scale",
            ("linear", "log")
        )  # END of the sidebar

st.title("Sonogram Comparator")

if uploaded_file and not second_sono:
    with st.spinner("Processing..."):
        st.write(uploaded_file.name)
        st.audio(uploaded_file, format='audio/wav')
        st.pyplot(graph_sample_sonogram(uploaded_file, uploaded_file.name[:-4], clr, frequency_scale))
        st.success("Done!")
    with open(uploaded_file.name[:-4] + ".png", "rb") as file:
        btn = st.download_button(
            label="Download sample sonogram",
            data=file,
            file_name=uploaded_file.name[:-4] + ".png",
            mime="image/png"
        )


elif second_sono and not uploaded_file:
    with st.spinner("Processing..."):
        st.write(reference_name)
        reference_file = association[reference_name]  # find the corresponding file name with the dictionary
        st.audio(reference_file, format='audio/wav')
        st.pyplot(graph_reference_sonogram(reference_file, reference_name, clr, frequency_scale))
        st.success("Done!")
    with open("sonogram.png", "rb") as file:
        btn = st.download_button(
            label="Download reference sonogram",
            data=file,
            file_name=reference_name + ".png",
            mime="image/png"
        )


else:  # if there is an uploaded file and a reference file selected at the same time
    col1, col2 = st.columns(2)  # allow to have the two sonograms side by side

    with col1:
        if uploaded_file:
            with st.spinner("Processing..."):
                st.write(uploaded_file.name)
                st.audio(uploaded_file, format='audio/wav')
                st.pyplot(graph_sample_sonogram(uploaded_file, uploaded_file.name[:-4], clr, frequency_scale))
                st.success("Done!")
            with open(uploaded_file.name[:-4] + ".png", "rb") as file:
                btn = st.download_button(
                    label="Download sample sonogram",
                    data=file,
                    file_name=uploaded_file.name[:-4] + ".png",
                    mime="image/png"
                )

    with col2:
        if second_sono and reference_name:
            with st.spinner("Processing..."):
                st.write(reference_name)
                reference_file = association[reference_name]  # find the corresponding file name with the dictionary
                st.audio(reference_file, format='audio/wav')
                st.pyplot(graph_reference_sonogram(reference_file, reference_name, clr, frequency_scale))
                st.success("Done!")
            with open("sonogram.png", "rb") as file:
                btn = st.download_button(
                    label="Download reference sonogram",
                    data=file,
                    file_name=reference_name + ".png",
                    mime="image/png"
                )

# todo allow more example (maybe one for each bird call in belgium) -> only interesting parts selectionned
# theming?
