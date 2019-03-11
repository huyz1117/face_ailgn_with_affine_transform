import os
import cv2
import numpy as np
from scipy import misc
from skimage import transform as trans
if __name__ == '__main__':
    image_size = [224, 224]
    src = np.array([
        [30.2946, 51.6963],
        [65.5318, 51.5014],
        [48.0252, 71.7366],
        [33.5493, 92.3655],
        [62.7299, 92.2041]])
    src[:, 0] += 8.0
    src += 56
    for db in ['cp']:
        print('%s working' % db)
        if db == 'ca':
            image_ls = '../CA&CP/CALFW/images/images&landmarks/images&landmarks/images'
            landmarks_ls = '../CA&CP/CALFW/images/images&landmarks/images&landmarks/landmarks'
        else:
            image_ls = '../CA&CP/CPLFW_pairs_changed/images'
            landmarks_ls = '../CA&CP/CPLFW_pairs_changed/landmarks'
        fldpath = '../CA&CP/' + db + '-aligned'
        if not os.path.exists(fldpath):
            os.makedirs(fldpath)
        for _, _, filenames in os.walk(image_ls):
            for filename in filenames:
                imgpath = os.path.join(image_ls,filename)
                img = misc.imread(imgpath)
                (imgname, _) = os.path.splitext(filename)
                print(imgname)
                landmarkname = imgname + '_5loc_attri.txt'
                dst = np.loadtxt(os.path.join(landmarks_ls,landmarkname))
                # points = np.array(points)
                # dst = np.reshape(points,(5,2))
                tform = trans.SimilarityTransform()
                tform.estimate(dst, src)
                M = tform.params[0:2, :]
                warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)
                bgr = warped[..., ::-1]
                cv2.imwrite(os.path.join(fldpath,filename), bgr)
        print('%s finished' % db)