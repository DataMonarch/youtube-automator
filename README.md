# youtube-automator

This is a fun project centered around finding interesting stories on Reddit and compiling youtube shorts videos with them. The visuals are intended to be some gaming oriented videos 


## Developing

To clone this project and build your awesome next-gen solution based on it:

```shell
git clone https://github.com/DataMonarch/youtube-automator.git
```

## How to Run the Video Processor Script
This script is used to trim videos. To run the script, follow the steps below after cloning the repo:

### Step 1: Install the Required Libraries
Before running the script, ensure that the required libraries are installed by running the following command in your terminal:

``` shell
pip install numpy pandas moviepy
```
### Step 2: Run the App

``` shell
cd <path-to-repo-parent>/youtube-automator
python app.py
```
*Disclaimer: the app interface displays only the most important info, for more verbose logging, see the terminal outputs.*


### Alternative to step 2: Use the CLI tool
The video processing script can be run with the following command:

``` shell
python yt_shorts_main.py [-l URL | -vid VIDEO_ID] [-s START] [-e END] [-c COUNT]

Arguments

    -l, --url: The URL of the video to be trimmed
    -s, --start: The start time in the format hh.mm.ss
    -e, --end: The end time in the format hh.mm.ss
    -vid, --video_id: The ID of the video to be trimmed
    -c, --count: The number of times the video should be trimmed
```
*Note that either -l or -vid must be specified. If both are specified, -l will be used.*

### Example Usage

To trim a video with ID 12345 from 00:10:00 to 00:15:00, run the following command:

``` shell
python yt_shorts_main.py -vid 12345 -s 00.10.00 -e 00.15.00

```
To trim a video from a YouTube URL, run the following command:

``` shell
python yt_shorts_main.py -l https://www.youtube.com/watch?v=12345 -s 00.10.00 -e 00.15.00


```

## Configuration
> This section will be updated at a later stage

## Contributing

"If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome."


## Licensing
> This section will be updated at a later stage
