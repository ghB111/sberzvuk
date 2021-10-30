import ffmpeg

video = (
        ffmpeg
        .input('video.mp4')
        .video
        )

audio_1 = (
        ffmpeg
        .input('video.mp4')
        .audio
        .filter('atrim', end=2)
        )

audio_beep = (
        ffmpeg
        .input('censor.wav')
        .filter('atrim', end=0.2)
        .filter('aeval', exprs="val(ch)/2")
        )

audio_2 = (
        ffmpeg
        .input("video.mp4")
        .filter('atrim', start=2.4)
        )

audio_res = (
        ffmpeg
        .filter((audio_1, audio_beep, audio_2), 'concat', n=3, v=0, a=1)
        )

video_res = (
        ffmpeg
        .concat(video, audio_res, v=1, a=1)
        .output("res.mp4")
        .run(overwrite_output=True)
        )

