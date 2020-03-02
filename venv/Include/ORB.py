import cv2
import numpy as np
import os


class SimilarImageRecognizer:
    @staticmethod
    def compare_orb_BRUTFORCE_HUMMING(filepath, filepath2):
        # 0 oznacza wczytanie tylko czarno biale
        image = cv2.imread(filepath, 0)
        image2 = cv2.imread(filepath2, 0)
        # TODO normalizacja
        # moze jakas normalizacja by wpadła

        # połaczenie alg fastkeypoints i brief deskryptor
        # number_of_featue => zeby nie trawalo to wiekow
        number_of_feature = 1000
        orb = cv2.ORB_create(number_of_feature)
        # kp - punkty kluczowe, desc - deskryptor
        kp, desc = orb.detectAndCompute(image, None)
        kp2, desc2 = orb.detectAndCompute(image2, None)

        index_param = dict(algorithm=0, trees=0)
        search_params = dict()

        flann = cv2.FlannBasedMatcher(index_param, search_params)
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

        matches = matcher.match(desc, desc2, None)
        # w zależności od odlgełosci humminga
        matches = [m for m in matches if m.distance < 30]

        # powiedzmy 5 maczy które są dokładne
        if len(matches) > 5:
            return True
        return False

    @staticmethod
    def compare_histogram_Probability(filepath, filepath2):
        image = cv2.imread(filepath, 0)
        image2 = cv2.imread(filepath2, 0)

        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0, 256])

        hist_diff = cv2.compareHist(hist, hist2, cv2.HISTCMP_BHATTACHARYYA)
        probability_match = cv2.matchTemplate(hist, hist2, cv2.TM_CCOEFF_NORMED)[0][0]

        img_template_diff = 1 - probability_match

        # srednia wazona bo histogram jest mniej miarodajny ale wnosi informacje
        # commutative_image_diff = (hist_diff+ img_template_diff) / 2
        commutative_image_diff = (hist_diff / 10) + img_template_diff

        # 25% odchyłu
        if commutative_image_diff < 0.25:
            print(commutative_image_diff)
            return True
        return False

    @staticmethod
    def findInFolder(filepath):
        path = os.path.dirname(filepath)
        mainImg = os.path.basename(filepath)
        images = []
        for file in os.listdir(path):
            if file.endswith(".jpg") and not file == mainImg:
                images.append(os.path.join(path, file))

        similar = []
        for img in images:
            if True == SimilarImageRecognizer.compare_histogram_Probability(filepath, img):
                similar.append(img)

        return similar

#Przykładowe wywołanie
img = SimilarImageRecognizer.findInFolder('D:\Programming\python\SIFT\\autodoblurowania2.jpg')
print(img)
