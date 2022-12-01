from PIL import Image
import numpy as np
import colorsys
from dsu import dsuRoot, dsuMerge

# Difference function (Euclidean distance)


def diffRGB(pixels, p1, p2):
    dr = (int(pixels[p1[0]][p1[1]][0]) - int(pixels[p2[0]][p2[1]][0]))
    dg = (int(pixels[p1[0]][p1[1]][1]) - int(pixels[p2[0]][p2[1]][1]))
    db = (int(pixels[p1[0]][p1[1]][2]) - int(pixels[p2[0]][p2[1]][2]))
    return dr*dr + dg*dg + db*db

# Set the image background to white


def mstThreshold(image, threshold=200, innerRadius=0, outerRadius=2, joinForeground=True):

    pixels = np.array(image)
    oldPixels = pixels
    imageHeight = pixels.shape[0]
    imageWidth = pixels.shape[1]
    pixelCount = imageHeight * imageWidth

    # Construct edges

    edges = np.zeros(pixelCount*(outerRadius)
                     * 2, 'int32, int32, int32')

    i = 0
    # to traverse each and every point on the image grid
    for r in range(0, imageHeight):
        for c in range(0, imageWidth):
            # index of the current pixel, r*imageWidth gives the row number and c gives the column number
            j = r*imageWidth + c

            for d in range(innerRadius, outerRadius):
                if r > d:  # it makes sense to scan only when the pixel is within the image
                    # jdown is the index of the pixel below the current pixel
                    jup = (r-d-1)*imageWidth + c
                    edges[i] = (j, jup, diffRGB(pixels, (r, c), (r-d-1, c)))
                    i += 1

                if c > d:
                    # d-1 affects column iterator here and not row as column condition satisfied here
                    jleft = r*imageWidth + c - d - 1
                    # edge = (index,left pixel index,weight)
                    edges[i] = (j, jleft, diffRGB(pixels, (r, c), (r, c-d-1)))
                    i += 1

    np.resize(edges, i)

    # Kruskal's MST algorithm with threshold to find minimum spanning forests

    # here x[2] is the third element of the tuple of the edges array
    edges = np.array(sorted(edges, key=lambda x: x[2]))

    # returns evenly spaced values within a given interval, ie, Id of the parent of each pixel
    parent = np.arange(0, pixelCount)
    mergedCount = 0

    for i in range(0, edges.size):
        # threashold is the max weight ,aka the difference between two pixels color
        if edges[i][2] > threshold:
            break
        if dsuRoot(parent, edges[i][0]) != dsuRoot(parent, edges[i][1]):
            dsuMerge(parent, edges[i][0], edges[i][1])
            mergedCount += 1

    # Calculate sum and frequency of pixels for each segment

    colorSum = {}
    colorCount = {}
    maxFreq = -1

    for i in range(0, pixelCount):  # iterate over all pixels or forests
        r = int(i / imageWidth)
        c = int(i % imageWidth)
        cRed = oldPixels[r][c][0]
        cGreen = oldPixels[r][c][1]
        cBlue = oldPixels[r][c][2]
        root = dsuRoot(parent, i)
        cSum = colorSum.get(root, (0, 0, 0))  # set default value to 0,0,0

        # include nodes color in the sum
        colorSum[root] = (cSum[0]+cRed, cSum[1]+cGreen, cSum[2]+cBlue)
        # update number of nodes in that tree
        colorCount[root] = colorCount.get(root, 0) + 1
        if maxFreq == -1 or colorCount[root] > colorCount[maxFreq]:
            maxFreq = root

    # Assign average segment color to each segment's pixels, except for background, which is set to white

    for i in range(0, pixelCount):
        r = int(i / imageWidth)
        c = int(i % imageWidth)
        root = dsuRoot(parent, i)

        if root == maxFreq:
            pixels[r][c][0] = 255
            pixels[r][c][1] = 255
            pixels[r][c][2] = 255
        else:
            if joinForeground:
                rootColorSum = colorSum[root]
                rootColorCount = colorCount[root]

                pixels[r][c][0] = rootColorSum[0] / float(rootColorCount)
                pixels[r][c][1] = rootColorSum[1] / float(rootColorCount)
                pixels[r][c][2] = rootColorSum[2] / float(rootColorCount)

    print('=== mstThreshold ===')
    print('Pixel count: ', pixelCount)
    print('Edge count: ', edges.size)
    print('Merged edges count: ', mergedCount)
    # aka number of root nodes= pixelcount-mergedcount
    print('Number of clusters: ', pixelCount-mergedCount)

    return Image.fromarray(pixels)
