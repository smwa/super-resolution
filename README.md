# Super Resolution API

This is a webserver that receives an image and returns a higher resolution version, based on the forked project.

This webserver is not secured or rate-limited, use at your own risk. If hosted publically, anonymous users may eat up your CPU cycles.

This is available on docker hub
`docker run -d -e RESOLUTION_LIMIT=2500 -p 80:80 smwa/super-resolution:latest`
