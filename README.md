# Computer Graphics Drone

## Week 1:
Started by learning about the drone's python api. tried to control it using the keyboard. after multiple tries it worked.
After that, I get the drone's camera stream and displayed it in a separate window.
In order for them to work together simultaneously, I used the threading library. One thread for the keyboard control and the other for the camera stream.
Also, used Opencv to display the camera stream and resize it to 360x240 for better real-time performance and control responsiveness.

### controls:
* `w` - move forward
* `s` - move backward
* `a` - move left
* `d` - move right
* `up` - move up
* `down` - move down
* `left` - rotate left
* `right` - rotate right
* `q` - terminate program


  Total time: ~7 hours