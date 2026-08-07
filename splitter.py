import os
import math
import subprocess
from mutagen import File


def get_duration(audio_file):
    """
    Retorna a duração do áudio em segundos.
    """
    audio = File(audio_file)
    return audio.info.length


def split_audio(audio_path, minutes, output_folder):

    duration = get_duration(audio_path)

    seconds = minutes * 60

    total_parts = math.ceil(duration / seconds)

    os.makedirs(output_folder, exist_ok=True)

    generated_files = []

    for part in range(total_parts):

        start = part * seconds

        output = os.path.join(
            output_folder,
            f"parte_{part+1:03}.mp3"
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            audio_path,
            "-ss",
            str(start),
            "-t",
            str(seconds),
            "-c",
            "copy",
            output
        ]

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        generated_files.append(output)

    return generated_files, duration