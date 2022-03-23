import cv2
import numpy as np

from marked_card_detector.graphics import flattener

font = cv2.FONT_HERSHEY_SIMPLEX

# based on https://github.com/EdjeElectronics/OpenCV-Playing-Card-Detector/blob/master/Cards.py
# Width and height of card corner, where rank and suit are
CORNER_WIDTH = 32
CORNER_HEIGHT = 84


class Card:
    """Structure to store information about query cards in the camera image."""

    def __init__(self, contour, image):
        self.image = image
        self.one_percent = int(image.shape[0] * 0.01)

        self.contour = contour  # Contour of card
        self.width, self.height = 0, 0  # Width and height of card
        self.corner_pts = []  # Corner points of card
        self.center = []  # Center point of card
        self.warp = []  # 200x300, flattened, grayed, blurred image
        self.rank_img = []  # Thresholded, sized image of card's rank
        self.suit_img = []  # Thresholded, sized image of card's suit
        self.best_rank_match = "Unknown"  # Best matched rank
        self.best_suit_match = "Unknown"  # Best matched suit
        self.rank_diff = 0  # Difference between rank image and best matched train rank image
        self.suit_diff = 0  # Difference between suit image and best matched train suit image

        self.__preprocess_card__()

    def __preprocess_card__(self):
        """Uses contour to find information about the query card. Isolates rank
        and suit images from the card."""

        image = self.image
        contour = self.contour

        # Find perimeter of card and use it to approximate corner points
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
        pts = np.float32(approx)
        self.corner_pts = pts

        # Find width and height of card's bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        self.width, self.height = w, h

        # Find center point of card by taking x and y average of the four corners.
        average = np.sum(pts, axis=0) / len(pts)
        cent_x = int(average[0][0])
        cent_y = int(average[0][1])
        self.center = [cent_x, cent_y]

        # Warp card into 200x300 flattened image using perspective transform
        self.warp = flattener(image, pts, w, h)

        # Grab corner of warped card image and do a 4x zoom
        # corner = self.warp[0:CORNER_HEIGHT, 0:CORNER_WIDTH]
        # corner_zoom = cv2.resize(qcorner, (0, 0), fx=4, fy=4)

        # Sample known white pixel intensity to determine good threshold level
        #     white_level = Qcorner_zoom[15,int((CORNER_WIDTH*4)/2)]
        #     thresh_level = white_level - CARD_THRESH
        #     if (thresh_level <= 0):
        #         thresh_level = 1
        #     retval, query_thresh = cv2.threshold(Qcorner_zoom, thresh_level, 255, cv2. THRESH_BINARY_INV)

        # Split in to top and bottom half (top shows rank, bottom shows suit)
        #     Qrank = query_thresh[20:185, 0:128]
        #     Qsuit = query_thresh[186:336, 0:128]

        # Find rank contour and bounding rectangle, isolate and find largest contour
        #     Qrank_cnts, hier = cv2.findContours(Qrank, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #     Qrank_cnts = sorted(Qrank_cnts, key=cv2.contourArea,reverse=True)

        #     # Find bounding rectangle for largest contour, use it to resize query rank
        #     # image to match dimensions of the train rank image
        #     if len(Qrank_cnts) != 0:
        #         x1,y1,w1,h1 = cv2.boundingRect(Qrank_cnts[0])
        #         Qrank_roi = Qrank[y1:y1+h1, x1:x1+w1]
        #         Qrank_sized = cv2.resize(Qrank_roi, (RANK_WIDTH,RANK_HEIGHT), 0, 0)
        #         card.rank_img = Qrank_sized

        #     # Find suit contour and bounding rectangle, isolate and find largest contour
        #     Qsuit_cnts, hier = cv2.findContours(Qsuit, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #     Qsuit_cnts = sorted(Qsuit_cnts, key=cv2.contourArea,reverse=True)

        #     # Find bounding rectangle for largest contour, use it to resize query suit
        #     # image to match dimensions of the train suit image
        #     if len(Qsuit_cnts) != 0:
        #         x2,y2,w2,h2 = cv2.boundingRect(Qsuit_cnts[0])
        #         Qsuit_roi = Qsuit[y2:y2+h2, x2:x2+w2]
        #         Qsuit_sized = cv2.resize(Qsuit_roi, (SUIT_WIDTH, SUIT_HEIGHT), 0, 0)
        #         card.suit_img = Qsuit_sized

    def top_left(self):
        return self.warp[70:95, 70:90]

    def draw(self, copy=False):
        """Draw the card name, center point, and contour on the camera image."""

        if copy:
            image = self.image.copy()
        else:
            image = self.image

        x = self.center[0]
        y = self.center[1]
        cv2.circle(image, (x, y), self.one_percent * 2, (255, 0, 0), -1)

        rank_name = self.best_rank_match
        suit_name = self.best_suit_match

        # Draw card name twice, so letters have black outline
        cv2.putText(image, (rank_name + ' of'), (x - 60, y - 10), font, 1, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, (rank_name + ' of'), (x - 60, y - 10), font, 1, (50, 200, 200), 2, cv2.LINE_AA)

        cv2.putText(image, suit_name, (x - 60, y + 25), font, 1, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, suit_name, (x - 60, y + 25), font, 1, (50, 200, 200), 2, cv2.LINE_AA)

        cv2.drawContours(image, self.contour, -1, (255, 0, 0), self.one_percent)

        # Can draw difference value for troubleshooting purposes
        # (commented out during normal operation)
        # r_diff = str(self.rank_diff)
        # s_diff = str(self.suit_diff)
        # cv2.putText(image,r_diff,(x+20,y+30),font,0.5,(0,0,255),1,cv2.LINE_AA)
        # cv2.putText(image,s_diff,(x+20,y+50),font,0.5,(0,0,255),1,cv2.LINE_AA)

        return image
