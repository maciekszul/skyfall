import os
import json
from utilities import files
import misc
from pliers.stimuli import VideoStim, VideoFrameStim
from pliers.extractors import IndicoAPIImageExtractor

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
    vid = VideoStim(vid_file)
