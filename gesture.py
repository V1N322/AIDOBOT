class Fingers():
    def __init__(self) -> None:
        self.fingerUp = {'thumb': False,
                         'index': False,
                         'middle': False,
                         'ring': False,
                         'pinky': False}
        
    def update_thumb(self, point4, point5, point17):
        if point4.x < point5.x and point4.x > point17.x:
            self.fingerUp['thumb'] = False
        
        elif point4.x > point5.x and point4.x < point17.x:
            self.fingerUp['thumb'] = False
        
        else:
            self.fingerUp['thumb'] = True

    def update_index(self, point8, point5):
        if point8.y > point5.y:
            self.fingerUp['index'] = False

        else: 
            self.fingerUp['index'] = True

    def update_middle(self, point12, point9):
        if point12.y > point9.y:
            self.fingerUp['middle'] = False

        else: 
            self.fingerUp['middle'] = True

    def update_ring(self, point16, point13):
        if point16.y > point13.y:S
            self.fingerUp['ring'] = False

        else:
            self.fingerUp['ring'] = True

    def update_pinky(self, point20, point17):
        if point20.y > point17.y:
            self.fingerUp['pinky'] = False

        else:
            self.fingerUp['pinky'] = True

    def update_info(self, currentPos):
        self.update_thumb(currentPos[4], currentPos[5], currentPos[17])
        self.update_index(currentPos[8], currentPos[5])
        self.update_middle(currentPos[12], currentPos[9])
        self.update_ring(currentPos[16], currentPos[13])
        self.update_pinky(currentPos[20], currentPos[17])


    def get_fingers_state(self):
      return self.fingerUp
        

class Gesture():
    def __init__(self) -> None:
        self.currentPointPos = {}
        self.lastPointPos = {}
        self.fingersState = Fingers()

    def get_current_up_finger(self):
        return self.fingersState.get_fingers_state()

    def update_point_pos(self, currentPos):
        self.lastPointPos = self.currentPointPos
        self.currentPointPos = currentPos
        self.fingersState.update_info(self.currentPointPos)
