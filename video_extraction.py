import os
import json
from utilities import files
import numpy as np
import itertools
import misc
import matplotlib.pyplot as plt
from pliers.stimuli import VideoStim, VideoFrameStim
from pliers.extractors import IndicoAPIImageExtractor
from joblib import Parallel, delayed

json_key_file = "keys/keys.json"
with open(json_key_file) as key_file:
    params = json.load(key_file)

json_vid_file = "video_analysis_params.json"
with open(json_vid_file) as vid_json:
    analysis = json.load(vid_json)

os.environ["INDICO_APP_KEY"] = params["indico"]
os.environ["CLARIFAI_API_KEY"] = params["clarifai"]
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = params["google"]

vid_file = analysis["video_path"]

files.make_folder("data")

if analysis["frames_no"] == 0:
    video = cv2.VideoCapture(vid_file)
    total_frames = 0
    while True:
        (grab, frame) = video.read()
        if not grab:
            break
        
        total_frames += 1
    video.release()
    cv2.destroyAllWindows()

    misc.update_key_value(json_vid_file, "frames_no", total_frames)

# vid = VideoStim(vid_file)
# frame1 = VideoFrameStim(vid, 1)
# frame2 = VideoFrameStim(vid, 2)

if analysis["SSIM"]:
    pass
    # vid = VideoStim(vid_file)
    # frame1 = VideoFrameStim(vid, 1)
    # frame2 = VideoFrameStim(vid, 2)
    # print(misc.SSIM(frame1.data, frame2.data))


if analysis["SSIM_tg"]:
    # fr = analyipythonsis["frames_no"]
    fr = 100
    vid = VideoStim(vid_file)
    results = np.zeros((fr, fr))
    fr_array = list(itertools.product(range(fr), range(fr)))
    def ext(i):
        fr1, fr2 = i
        fr1_data = VideoFrameStim(vid, fr1)
        fr2_data = VideoFrameStim(vid, fr2)
        res = misc.SSIM(fr1_data.data, fr2_data.data)
        results[fr1, fr2] = res
    Parallel(n_jobs=-1, backend="loky", verbose=11)(delayed(ext)(i) for i in fr_array)
    plt.imshow(
        results, 
        cmap="RdBu_r", 
        origin="upper",
        vmin=0.0,
        vmax=1.0
    )
    np.save("data/results.npy", results)
    plt.savefig("data/tg.png")


