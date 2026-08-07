import os
import shutil
import zipfile
import tempfile

import streamlit as st

from splitter import split_audio

st.set_page_config(
    page_title="Cortador de Áudio",
    page_icon="🎧"
)

st.title("🎧 Cortador de Áudio")

st.write(
    "Divida arquivos grandes em partes menores."
)

uploaded = st.file_uploader(
    "Selecione um áudio",
    type=[
        "mp3",
        "wav",
        "m4a",
        "flac",
        "ogg"
    ]
)

minutes = st.number_input(
    "Tempo de cada parte (minutos)",
    min_value=1,
    value=10
)

if uploaded:

    if st.button("✂ Cortar áudio"):

        with tempfile.TemporaryDirectory() as temp:

            input_path = os.path.join(
                temp,
                uploaded.name
            )

            with open(input_path, "wb") as f:
                f.write(uploaded.getbuffer())

            output_folder = os.path.join(
                temp,
                "partes"
            )

            with st.spinner("Processando..."):

                files, duration = split_audio(
                    input_path,
                    minutes,
                    output_folder
                )

            zip_path = os.path.join(
                temp,
                "audio_dividido.zip"
            )

            with zipfile.ZipFile(
                zip_path,
                "w",
                zipfile.ZIP_DEFLATED
            ) as zipf:

                for file in files:

                    zipf.write(
                        file,
                        arcname=os.path.basename(file)
                    )

            st.success("Concluído!")

            st.write(
                f"Duração: {duration/60:.1f} minutos"
            )

            st.write(
                f"Partes geradas: {len(files)}"
            )

            with open(zip_path, "rb") as f:

                st.download_button(
                    "⬇ Baixar ZIP",
                    f,
                    file_name="audio_dividido.zip"
                )