class Fingers():
    def __init__(self) -> None:
        self.fingerRaised = {'thumb': False,
                         'index': False,
                         'middle': False,
                         'ring': False,
                         'pinky': False}

        self.fingerDirection = {'thumb': '',
                         'index': '',
                         'middle': '',
                         'ring': '',
                         'pinky': ''}

        
    def _update_info_raised_fingers(self, fingerName, firstPoint, secondPoint):
        if firstPoint.y > secondPoint.y:
            self.fingerRaised[fingerName] = False

        else: 
            self.fingerRaised[fingerName] = True

    def _update_info_raised_thumb(self, point4, point5, point17):
        if point4.x < point5.x and point4.x > point17.x:
            self.fingerRaised['thumb'] = False
        
        elif point4.x > point5.x and point4.x < point17.x:
            self.fingerRaised['thumb'] = False
        
        else:
            self.fingerRaised['thumb'] = True

    def _update_info_direction_fingers(self, fingerName, firstPoint, secondPoint):
        if firstPoint.y > secondPoint.y and firstPoint.x in range(secondPoint.x-3, secondPoint.x+3):
            print('xd')

    def update_raised_fingers(self, currentPos):
        self._update_info_raised_thumb(currentPos[4], currentPos[5], currentPos[17])
        self._update_info_raised_fingers('index', currentPos[8], currentPos[5])
        self._update_info_raised_fingers('middle', currentPos[12], currentPos[9])
        self._update_info_raised_fingers('ring', currentPos[16], currentPos[13])
        self._update_info_raised_fingers('pinky', currentPos[20], currentPos[17])

    def update_direction_fingers(self, currentPos):
        pass

    def update_info(self, currentPos):
        self.update_raised_fingers(currentPos)
        self.update_direction_fingers(currentPos)

    def get_raised_fingers_state(self):
        return self.fingerRaised

    def get_direction_fingers_state(self):
        return self.fingerDirection
        

class Gesture():
    def __init__(self) -> None:
        self.currentPointPos = {}
        self.lastPointPos = {}
        self.fingersState = Fingers()

    def get_current_raised_fingers(self):
        return self.fingersState.get_raised_fingers_state()

    def get_current_direction_fingers(self):
        return self.fingersState.get_direction_fingers_state()

    def update_point_pos(self, currentPos):
        self.lastPointPos = self.currentPointPos
        self.currentPointPos = currentPos
        self.fingersState.update_info(self.currentPointPos)
