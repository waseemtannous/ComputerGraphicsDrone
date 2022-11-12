import threading
import cv2
import keyboard

from djitellopy import Tello


def initDrone() -> Tello:
    drone = Tello()
    drone.connect()
    print('Battery = ', drone.get_battery(), '%')

    # reset all parameters and speed
    drone.for_back_velocity = 0
    drone.left_right_velocity = 0
    drone.up_down_velocity = 0
    drone.yaw_velocity = 0
    drone.speed = 0

    # start video stream
    drone.streamoff()
    drone.streamon()

    drone.takeoff()

    return drone


def startStreamingThread(drone: Tello):
    def getDroneStream(drone: Tello):
        # vid = cv2.VideoCapture(1)
        while True:
            img = drone.get_frame_read().frame
            # ret, img = vid.read()
            img = cv2.resize(img, (360, 240))
            cv2.imshow("Drone Camera", img)
            # press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    t = threading.Thread(target=getDroneStream, args=(drone,))
    t.start()


def startControlThread(drone: Tello):
    def controlDrone(drone: Tello):
        speed = 100
        while True:

            if keyboard.is_pressed('q'):
                drone.end()
                break

            left_right_velocity = 0
            forward_backward_velocity = 0
            up_down_velocity = 0
            yaw_velocity = 0

            # wasd
            if keyboard.is_pressed('w'):
                forward_backward_velocity = speed
                print('w')
            if keyboard.is_pressed('s'):
                forward_backward_velocity = -speed
                print('s')
            if keyboard.is_pressed('a'):
                left_right_velocity = -speed
                print('a')
            if keyboard.is_pressed('d'):
                left_right_velocity = speed
                print('d')

            if not keyboard.is_pressed('w') and not keyboard.is_pressed('a'):
                forward_backward_velocity = 0
            if not keyboard.is_pressed('s') and not keyboard.is_pressed('d'):
                left_right_velocity = 0

            # arrow keys
            if keyboard.is_pressed('up'):
                up_down_velocity = speed
                print('up')
            if keyboard.is_pressed('down'):
                up_down_velocity = -speed
                print('down')
            if keyboard.is_pressed('left'):
                yaw_velocity = -speed
                print('left')
            if keyboard.is_pressed('right'):
                yaw_velocity = speed
                print('right')

            if not keyboard.is_pressed('up') and not keyboard.is_pressed('down'):
                up_down_velocity = 0
            if not keyboard.is_pressed('left') and not keyboard.is_pressed('right'):
                yaw_velocity = 0

            if drone.for_back_velocity != forward_backward_velocity or drone.left_right_velocity != left_right_velocity or drone.up_down_velocity != up_down_velocity or drone.yaw_velocity != yaw_velocity:
                drone.send_rc_control(left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity)
            drone.for_back_velocity = forward_backward_velocity
            drone.left_right_velocity = left_right_velocity
            drone.up_down_velocity = up_down_velocity
            drone.yaw_velocity = yaw_velocity

    t = threading.Thread(target=controlDrone, args=(drone,))
    t.start()


if __name__ == '__main__':
    drone = initDrone()
    startStreamingThread(drone)
    startControlThread(drone)
