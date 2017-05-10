ffmpeg -r 4 -f image2 -i a-%04d.png test.mp4


ffmpeg -r 4 -f image2 -i a-%04d.png -c:v libx264 -pix_fmt yuv420p test.mp4


ffmpeg -r 2 -f image2 -i a-%04d.png -c:v libx264 -vf "scale=640:trunc(ow/a/2)*2" -pix_fmt yuv420p gh_rain_comp3.mp4