# from DOBOT import *
import time
import cv2
import mediapipe as mp
# import gesture

# dobot = Dobot()
# dobot.connect()

video = cv2.VideoCapture(0)

handsAI = mp.solutions.mediapipe.python.solutions.hands.Hands(static_image_mode=False,
                                                    max_num_hands=1,
                                                    min_tracking_confidence=0.5,
                                                    min_detection_confidence=0.5)

# gesture = gesture.Gesture()


def _update_info_direction_fingers(firstPoint, secondPoint):
    if firstPoint.y > secondPoint.y:
        print('xd')


while True:
    ret, image = video.read()
    hand = handsAI.process(image)

    if hand.multi_hand_landmarks:
        for pointID, pos in enumerate(hand.multi_hand_landmarks[0].landmark):

            height, weight, _ = image.shape
            pointPosInScreenX, pointPosInScreenY = int(pos.x*weight), int(pos.y*height)

            _update_info_direction_fingers(hand.multi_hand_landmarks[0].landmark[9], hand.multi_hand_landmarks[0].landmark[5])

            # gesture.update_point_pos(hand.multi_hand_landmarks[0].landmark)
    

    cv2.imshow('Test', image)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
