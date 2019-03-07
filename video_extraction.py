import os
import json
from utilities import files
import numpy as np
import itertools
import argparse
import misc
from pliers.stimuli import VideoStim, VideoFrameStim
from pliers.extractors import IndicoAPIImageExtractor
from joblib import Parallel, delayed, dump, load
import shutil


des = "SPLIT"
parser = argparse.ArgumentParser(description=des)
parser.add_argument('-n', type=int, nargs="?", const=0, help="number of split parts")
parser.add_argument('-s', type=int, nargs="?", const=0, help="split part number")
args = parser.parse_args()
params = vars(args)
split_no = params["n"]
split_pt = params["s"]

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


if analysis["SSIM"]:
    fr = analysis["frames_no"]
    vid = VideoStim(vid_file)
    fr_pw = misc.pairwise(range(fr))
    fr_pw_split = np.array_split(fr_pw, split_no)
    fr_pw_pt = fr_pw_split[split_pt]
    results = np.zeros(len(fr_pw_pt))

    def ext(ix, i):
        fr1, fr2 = i
        fr1_data = VideoFrameStim(vid, fr1)
        fr2_data = VideoFrameStim(vid, fr2)
        res = misc.SSIM(fr1_data.data, fr2_data.data)
        results[ix] = res
    
    Parallel(n_jobs=-1, backend="threading", verbose=0)(delayed(ext)(ix, i) for ix, i in enumerate(fr_pw_pt))
    np.save(
        "data/{}_SSIM.npy".format(str(split_pt).zfill(5)),
        results
    )


if analysis["SSIM_TG"]:
    fr = analysis["frames_no"]
    fr = 10
    vid = VideoStim(vid_file)
    fr_pw = np.array(list(itertools.combinations(list(range(fr)), 2)))
    fr_pw_split = np.array_split(fr_pw, split_no)
    fr_pw_pt = fr_pw_split[split_pt]
    results = np.zeros((fr, fr))
    memmap_file = "data/.temp/{}_SSIM_TG".format(str(split_pt).zfill(5))
    output = np.memmap(
        memmap_file,
        dtype=results.dtype,
        shape=results.shape,
        mode="w+"
    )

    def ext(ix, i, output):
        fr1, fr2 = i
        fr1_data = VideoFrameStim(vid, fr1)
        fr2_data = VideoFrameStim(vid, fr2)
        res = misc.SSIM(fr1_data.data, fr2_data.data)
        output[fr1, fr2] = res
        feedback = "{}/{}_{}_{}_{}".format(
            str(ix+1).zfill(5),
            str(len(fr_pw_pt)).zfill(5),
            fr1,
            fr2,
            res
        )
        print(feedback)

    Parallel(n_jobs=-1, backend="multiprocessing", verbose=0)(delayed(ext)(ix, i, output) for ix, i in enumerate(fr_pw_pt))

    out_array = np.asarray(output)
    np.save(
        "data/{}_SSIM_TG.npy".format(str(split_pt).zfill(5)),
        out_array
    )
    np.allclose(out_array, output)
    os.remove(memmap_file)