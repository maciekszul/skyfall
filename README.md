# skyfall

to recreate the environment:

```
conda create --name myenv --file spec-file.txt
conda install --name myenv --file spec-file.txt
```

# Analysis JSON

Parameter `"frames_no"` if `0` will start counting frames of the video and update the number in the JSON. Useful for paralellisation of the extraction of the info from the frames
