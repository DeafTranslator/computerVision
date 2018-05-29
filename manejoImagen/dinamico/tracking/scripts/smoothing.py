# import enum
from cv2 import blur, GaussianBlur, medianBlur, bilateralFilter

def enum(**enums):
    return type('Enum', (), enums)

filters = enum(AVERAGING = 0,
    GAUSSIAN = 1,
    MEDIA = 2,
    BILATERAL = 3)

def smoothing(filterType, img, kSize = (5,5), sigma = 0):
    if filterType is filters.AVERAGING:
        return blur(img,kSize)
    elif filterType is filters.GAUSSIAN:
        return GaussianBlur(img,kSize,sigma)
    elif filterType is filters.MEDIA:
        return medianBlur(img, kSize)
    else:
        return bilateralFilter(img, 9,75,75)
