import cv2
from handDetector import HandDetector
import pyglet


class PianoKey():
    def __init__(self, pos, text, size, color):
        self.location = pos
        self.displayText = text
        self.colorType = color
        self.size = size


def drawPiano(img, keys):
    for key in keys:
        posx, posy = key.location
        width, height = key.size
        cv2.rectangle(img, key.location, (posx + width, posy + height), key.colorType, cv2.FILLED)
        cv2.putText(img, key.displayText, (posx + 10, posy + height - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (214, 0, 220),
                    2)

    return img


if __name__ == '__main__':
    videoCapture = cv2.VideoCapture(0)
    videoCapture.set(3, 1080)
    videoCapture.set(4, 460)

    window = pyglet.window.Window()
    detector = HandDetector(detectionCon=0.9)

    keys = [["C", "D", 'E', "F", "G", "A", "B", "C", "D", "E", "F", "G", "A", "B"],
            ["C#", "D#", "F#", "G#", "A#", "C#", "D#", "F#", "G#", "A#"]]

    keysList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            if i == 0:
                keysList.append(PianoKey([38 * j + 15, 80], key, [35, 100], (255, 255, 255)))
            else:
                keysList.append(PianoKey([(40 + j) * j + 25, 80], key, [35, 50], (0, 0, 0)))

    while True:
        success, img = videoCapture.read()

        img = detector.findHands(img)
        lmlist, bboxInfo = img['lmList'], img['bbox']
        img = drawPiano(img, keysList)

        if lmlist:
            for key in keysList:
                x, y = key.location
                w, h = key.size
                tips = [4, 8, 12, 16, 20]

                for tip in tips:
                    if x < lmlist[tip][0] < x + w and y < lmlist[tip][1] < y + h:
                        length, _, _ = detector.findDistance(tip, tip - 3, img)
                        if length <= 120:
                            cv2.rectangle(img, key.location, (x + w, y + h), (65, 12, 78), cv2.FILLED)
                            pyglet.resource.media(f"./sound/${key.displayText}.wav", streaming=False).play()

        cv2.imshow("Virtual Piano", img)
        cv2.waitKey(1)
