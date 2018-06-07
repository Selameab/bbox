import numpy as np
import warnings
warnings.filterwarnings("ignore")

from bbox import BBox2D, BBox2DList
from bbox.metrics import jaccard_index


def naive_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # print(xA, yA, xB, yB)

    # compute the area of intersection rectangle
    interArea = (xB - xA + 1) * (yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # print(interArea)
    # print(boxAArea, boxBArea)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou


def test_jaccard_index_single():
    # sample bounxing boxes (x, y, w, h)
    bbox1 = [39, 63, 203, 112]
    bbox2 = [54, 66, 198, 114]

    a = BBox2DList([bbox1])
    b = BBox2DList([bbox2])
    iou = jaccard_index(a, b)

    bbox1[2], bbox1[3] = bbox1[2] + bbox1[0] - 1, bbox1[3] + bbox1[1] - 1
    bbox2[2], bbox2[3] = bbox2[2] + bbox2[0] - 1, bbox2[3] + bbox2[1] - 1

    gt_iou = naive_intersection_over_union(bbox1, bbox2)
    gt_iou = np.array([gt_iou])
    
    assert np.array_equal(iou.flatten(), gt_iou)

def test_jaccard_index():
    # bounding boxes of the form (x, y, w, h)
    bboxes_1 = [[39, 63, 203, 112], [49, 75, 203, 125], [31, 69, 201, 125], [50, 72, 197, 121], [35, 51, 196, 110]]
    bboxes_2 = [[54, 66, 198, 114], [42, 78, 186, 126], [18, 63, 235, 135], [54, 72, 198, 120], [36, 60, 180, 108]]

    a = BBox2DList(bboxes_1)
    b = BBox2DList(bboxes_2)

    iou = jaccard_index(a, b)
    
    gt_iou = np.zeros((len(bboxes_1), len(bboxes_2)))
    
    for i, x in enumerate(bboxes_1):
        for j, y in enumerate(bboxes_2):
            bx = [x[0], x[1], x[2]+x[0]-1, x[3]+x[1]-1]
            by = [y[0], y[1], y[2]+y[0]-1, y[3]+y[1]-1]
            gt_iou[i, j] = naive_intersection_over_union(bx, by)

    assert gt_iou.shape == iou.shape
    assert np.array_equal(gt_iou, iou)
