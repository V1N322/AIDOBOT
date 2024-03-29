import math
import numpy as np


class Finger():
    def __init__(self, currentPos, name='', isRaised=True) -> None:
        self.name = name
        self.isRaised = isRaised
        self.currentPos = currentPos
        fingerslist = ['thumb', 'index', 'middle', 'ring', 'pinky']
        i = fingerslist.index(self.name)
        self.knuckle = self.currentPos[1 + i * 4]
        self.joint1 = self.currentPos[2 + i * 4]
        self.joint2 = self.currentPos[3 + i * 4]
        self.tip = self.currentPos[4 + i * 4]

    def update_isRaised(self):
        if type(self.currentPos[0]) == int:
            return False

        def distanceInSpace(point1, point2):
            return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2 + (point2.z - point1.z) ** 2) ** 0.5

        spaceBehindKnuckles = distanceInSpace(self.currentPos[13], self.currentPos[17])

        def unit_vector(vector):
            return vector / np.linalg.norm(vector)

        def angle_between(v1, v2):
            v1_u = unit_vector(v1)
            v2_u = unit_vector(v2)
            return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

        if self.name == 'thumb':
            for j in [5, 9, 13, 17]:  # knuckles
                v31 = (self.currentPos[3].x - self.currentPos[1].x, self.currentPos[3].y - self.currentPos[1].y,
                       self.currentPos[3].z - self.currentPos[1].z)
                v15 = (self.currentPos[1].x - self.currentPos[5].x, self.currentPos[1].y - self.currentPos[5].y,
                       self.currentPos[1].z - self.currentPos[5].z)

                if distanceInSpace(self.tip, self.currentPos[j]) < spaceBehindKnuckles * 1.3 or distanceInSpace(
                        self.joint2, self.currentPos[j]) < spaceBehindKnuckles * 1.2 or angle_between(v31,
                                                                                                      v15) * 57.3 < 30:
                    self.isRaised = False
                    return

            self.isRaised = True

            return
        else:
            v34 = (self.tip.x - self.joint2.x, self.tip.y - self.joint2.y, self.tip.z - self.joint2.z)
            v23 = (self.joint2.x - self.joint1.x, self.joint2.x - self.joint1.y, self.joint2.z - self.joint1.z)
            self.isRaised = angle_between(v34, v23) * 57.3 > 95


class Arm():

    def __init__(self, currentPos=[]) -> None:
        self.thumbDirection = None
        self.handDirection = None
        self.currentPos = currentPos
        self.fingersDict = {}

    def _update_info_points(self, currentPos):
        self.currentPos = currentPos
        self.fingersDict = {
            'thumb': Finger(self.currentPos, 'thumb'),
            'index': Finger(self.currentPos, 'index'),
            'middle': Finger(self.currentPos, 'middle'),
            'ring': Finger(self.currentPos, 'ring'),
            'pinky': Finger(self.currentPos, 'pinky')}

    def _update_info_hand_position(self):
        point5 = self.currentPos[5]
        point0 = self.currentPos[0]
        point13 = self.currentPos[13]
        point9 = self.currentPos[9]
        point8 = self.currentPos[8]
        point1 = self.currentPos[1]

        def distanceInPlane(point1, point2):
            return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** 0.5

        # вычисление направления большого пальца

        gradusThumb = math.atan((point5.y - point13.y) / (point5.x - point13.x)) * -57.3

        if gradusThumb < 0:
            gradusThumb = abs(gradusThumb)
            if gradusThumb > 90:
                gradusThumb = 180 + (180 - gradusThumb)
            else:
                gradusThumb = 180 + gradusThumb

        if 60 < gradusThumb < 110:
            self.thumbDirection = 'up'
        elif 110 < gradusThumb < 225:
            self.thumbDirection = 'left'
        elif 225 < gradusThumb < 290:
            self.thumbDirection = 'down'
        elif 290 < gradusThumb < 360 or 0 < gradusThumb < 60:
            self.thumbDirection = 'right'

        # вычисление направления ладони

        gradusHand = math.atan2(((point13.y + point9.y) / 2 - point0.y),
                                ((point9.x + point13.x) / 2 - point0.x)) * -57.3

        if gradusHand < 0:
            gradusHand = abs(gradusHand)
            if gradusHand > 90:
                gradusHand = 180 + (180 - gradusHand)
            else:
                gradusHand = 180 + gradusHand

        self.gradusHand = gradusHand
        spaceBehindKnuckles = distanceInPlane(self.currentPos[5], self.currentPos[9])

        if distanceInPlane(point9, point0) < spaceBehindKnuckles * 1.5:
            self.handDirection = 'on'
        elif 45 < gradusHand < 135:
            self.handDirection = 'up'
        elif 135 < gradusHand < 225:
            self.handDirection = 'right'
        elif 225 < gradusHand < 315:
            self.handDirection = 'down'
        elif 315 < gradusHand < 360 or 0 < gradusHand < 45:
            self.handDirection = 'left'

    def _update_info_fingers_raised(self):
        for finger in self.fingersDict.values():
            finger.update_isRaised()

    def update_info(self, currentPos):
        self._update_info_points(currentPos)
        self._update_info_hand_position()
        self._update_info_fingers_raised()


class Gesture():
    def __init__(self) -> None:
        self.arm = Arm()
        self.currentPointsPos = {}
        self.lastPointPos = {}
        self.fingersState = Arm(self.currentPointsPos)

    def get_current_raised_fingers(self):
        return self.fingersState.get_raised_fingers_state()

    def get_current_direction_fingers(self):
        return self.fingersState.get_direction_fingers_state()

    def update_point_pos(self, currentPos):
        self.lastPointPos = self.currentPointsPos
        self.currentPointsPos = currentPos
        # self.fingersState.update_info(self.currentPointsPos)

    def update_info(self, arm, curentPos):
        # обновляет все параметры руки
        arm.update_info(curentPos)
        pass