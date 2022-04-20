#!/usr/bin/env python3
import argparse
import ffmpeg
import random
import logging


def get_logger(name):
    log_format = "%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    shandler = logging.StreamHandler()
    shandler.setLevel(logging.INFO)
    shandler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(shandler)
    return logger


def movie_generate(
    sound_path,
    bg_path,
    output_path,
    timestep,
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
    ffmpeg.output(sound, video, output_path, format="mp4").run()


logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="generate video from the soundtrack and background"
    )
    parser.add_argument("soundtrack", help="set the path to the soundtrack")
    parser.add_argument("background", help="set the path to the background")
    parser.add_argument("output", help="set the path to the output file")
    parser.add_argument(
        "-t",
        "--timestep",
        default=0,
        type=int,
        help="set the color change time of the sound wave",
    )
    args = parser.parse_args()
    try:
        movie_generate(
            args.soundtrack, args.background, args.output, args.timestep
        )
    except Exception as err:
        logger.error(err)


if __name__ == "__main__":
    main()
