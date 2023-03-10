from DOBOT import *
import time
import cv2
import mediapipe as mp
import gesture


dobot = Dobot()
dobot.connect()


class Point():
    def __init__(self) -> None:
        self.currentPos = None
        self.lastPos = None

    def set_pos(self, newPos):
        self.lastPos = newPos if self.currentPos == None else self.currentPos
            
        self.currentPos = newPos

    def made_movements(self, coefficient):

        result = [0,0]


        if self.currentPos.x > self.lastPos.x+coefficient:
            result[0] = -20

        elif self.currentPos.x+coefficient < self.lastPos.x:
            result[0] = 20

        if self.currentPos.y > self.lastPos.y+coefficient:
            result[1] = -20

        elif self.currentPos.y+coefficient < self.lastPos.y:
            result[1] = 20




        return result

def made_triangle(dobotPos):
    dobot.move_to(200, dobotPos[1]+20, dobotPos[2], 10)
    time.sleep(0.5)
    dobot.move_to(200, dobotPos[1], dobotPos[2]-20, 10)
    time.sleep(0.5)
    dobot.move_to(200, dobotPos[1]-20, dobotPos[2], 10)
    time.sleep(0.5)
    dobot.move_to(200, dobotPos[1], dobotPos[2]+20, 10)

def made_shake(dobotPos):
    dobot.move_to(200, dobotPos[1]+20, dobotPos[2], 10)
    time.sleep(1)
    dobot.move_to(200, dobotPos[1]-40, dobotPos[2], 10)
    time.sleep(1)
    dobot.move_to(200, dobotPos[1]+20, dobotPos[2], 10)

def replace_air(startAir):
    result = False

    if startAir:
        return False

    return True

video = cv2.VideoCapture(0)

handsAI = mp.solutions.mediapipe.python.solutions.hands.Hands(static_image_mode=False,
                                                    max_num_hands=1,
                                                    min_tracking_confidence=0.5,
                                                    min_detection_confidence=0.5)

point = Point()
tiks = 0
posXPoint12 = 10
startAir = False
gesture = gesture.Gesture()


while True:
    ret, image = video.read()
    hand = handsAI.process(image)



    if hand.multi_hand_landmarks:
        # input(str(hand.multi_hand_landmarks[0].landmark))
        dobotPos = dobot.get_pos()
        for pointID, pos in enumerate(hand.multi_hand_landmarks[0].landmark):

            gesture.update_point_pos(hand.multi_hand_landmarks[0].landmark)


            height, weight, _ = image.shape
            pointPosInScreenX, pointPosInScreenY = int(pos.x*weight), int(pos.y*height)

            posXPoint12 = pos.y if pointID == 12 else posXPoint12

            if pointID == 9:

                point.set_pos(pos)
                cv2.circle(image, (pointPosInScreenX, pointPosInScreenY), 8, (0,255,0), cv2.FILLED)
                moveTo = point.made_movements(0.06)



                if moveTo[0] != 0 or moveTo[1] != 0:
                    y = dobotPos[1]
                    z = dobotPos[2]
                    
                    dobot.move_to(200, y+moveTo[0], z+moveTo[1], 10)

                fingers = gesture.get_current_up_finger()

                if not fingers['middle'] and tiks%5 == 0:
                    startAir = replace_air(startAir)
                    if startAir:
                        dobot.on_air()
                    elif not startAir:
                        dobot.off_air()

                if not fingers['ring'] and tiks%5 == 0:
                    made_shake(dobotPos)

                if not fingers['index'] and tiks%5 == 0:
                    made_triangle(dobotPos)
                    

    dobot.clear_command()


    tiks+=1
    cv2.imshow('Test', image)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
