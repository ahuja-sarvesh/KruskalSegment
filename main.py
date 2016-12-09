from PIL import Image, ImageFilter, ImageEnhance
from mstsegment import mstThreshold

# PARAMETERS

# Image file must be in RGB color format, recommended size is between 200x200 to 800x800 pixels
imPath = "scan.jpg"
im = Image.open(imPath)

# Sensitivity to color differences, a higher threshold will tolerate more differences
threshold = 200

# Radius in which neighboring pixels will be considered
innerRadius = 0
outerRadius = 3

# If set to true, then will set foreground segments to average color of pixels in the segment
joinForeground = True

print 'Source image: ', imPath
print im.format, im.size, im.mode
print 'Segmentation threshold: ', threshold
print 'Inner/outer radius: ', innerRadius, outerRadius

# Set image background to white
im = mstThreshold(im, threshold, innerRadius, outerRadius, joinForeground)

# Show result
im.show()
