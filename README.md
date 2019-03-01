# skyfall

to recreate the environment:

```
conda create --name myenv --file spec-file.txt
conda install --name myenv --file spec-file.txt
```

# Analysis parameters - JSON file

Parameter `"frames_no"` if `0` will start counting exact amount of frames of the video and update the number in the JSON. Useful for paralellisation of the extraction of the info from the frames.

Parameter`SSIM` will produce a structural similarity metric between two consecutive frames 
