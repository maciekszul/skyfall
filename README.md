# SKYFALL
Cloudbased services which accounts might be needed:
- Google Cloud https://cloud.google.com/
- Indico https://indico.io
- ClarifAI https://clarifai.com
- Amazon AWS https://aws.amazon.com


to recreate the environment used in analysis:
```
conda env create -f environment.yml
```

# Analysis parameters - JSON file

Parameter `"frames_no"` if `0` will start counting exact amount of frames of the video and update the number in the JSON. Useful for paralellisation of the extraction of the info from the frames.

Parameter`"SSIM"` will produce a structural similarity metric between two consecutive frames along the timeline of the video.



# misc

export the environment

```
conda env export | grep -v "^prefix: " > environment.yml
```