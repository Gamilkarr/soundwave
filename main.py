import ffmpeg
import random


def movie_generate(
    sound_path,
    bg_path,
    output_path,
    timestep,
    _format,
):
    """Generates video from the soundtrack and background"""
    sound = ffmpeg.input(sound_path)
    length = float(ffmpeg.probe(sound_path)["format"]["duration"])
    bg = ffmpeg.input(bg_path, stream_loop=-1, t=length).filter("scale", "1280x720")
    wave = ffmpeg.filter([sound], "showwaves", "1280x720", "cline")
    if timestep:
        for time in range(timestep, int(length), timestep):
            wave = wave.filter(
                "colorize",
                enable=f"between(t,{time},{time+timestep})",
                hue=random.randint(0, 360),
            )
    video = ffmpeg.overlay(bg, wave)
    ffmpeg.output(sound, video, output_path, format=_format).run()
