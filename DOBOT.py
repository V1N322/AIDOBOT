import threading
import DobotDllType as dType
from time import sleep
import cv2 as cv
import mediapipe
import Morse


class Dobot():
    def __init__(self):
        self.api = None


    def _get_con_str(self):
        return {
            dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    def _exit(self):
        dType.SetQueuedCmdStopExec(self.api)
        dType.DisconnectDobot(self.api)

    def connect(self, showInfo=True):
        self.api = dType.load()
        self.state = dType.ConnectDobot(self.api, "", 115200)[0]


        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            dType.SetPTPJointParams(self.api,200,200,200,200,200,200,200,200,0)
            dType.SetPTPCoordinateParams(self.api,200,200,200,200,0)
            dType.SetPTPJumpParams(self.api, 10, 200,0)
            dType.SetPTPCommonParams(self.api, 100, 100,0)

            print('Connect status:', 'Success')

        else:
            print('Connect status: Error') if showInfo is True else None
            self._exit()

    def play_number(self, number):
        morse = Morse.convert_num_to_morse(number)
        for num in morse:
            print('num')

    def on_air(self):
        dType.SetEndEffectorSuctionCup(self.api, True, True)

    def off_air(self):
        dType.SetEndEffectorSuctionCup(self.api, False, True)

    def clear_command(self):
        dType.SetQueuedCmdClear(self.api)

    def move_to(self, x, y, z, rHead):
        dType.SetPTPCmd(self.api, 2, x, y, z, rHead, 1)

    def get_pos(self):
        return dType.GetPose(self.api)

