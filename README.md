# DigitalComicReader
An effort to make a decent open-source digital comic reader, with a focus on automatic panel detection and ordering for enhanced reading experience

## Goals
- Library organization and visualization
- Panel detection and ordering
- Cross platform, Windows/Linux/OSX, iOS/Android

## Library organization and visualization
- Ability to add directories and recursively search the space for usable files, create thumbnails, display in a reasonable way
- Ability to sort by various fields


## Panel detection and ordering

Currently working on the details of panel detection and ordering.
Have achieved decent panel detection using the following:

1. Background segmentation by using a relaxed connected component search with seeds on the border of the image. 
Relaxed in this context means that a pixel is considered connected if it is within a threshold of the value of the current pixel, rather than needing to have the same value.
2. Convert to binary foreground/background image
3. Clean up small connections between panels using morphological erosion and dilation with a 3x3 square mask
4. Take convex hulls of each panel assuming they're a rectangle. 
Need to take a basic linear geometric convex hull to account for non-rectangles

![alt text](https://github.com/TravisTag/DigitalComicReader/raw/master/images/readmeimages/16out.png)

Using a non-white background:

![alt text](https://github.com/TravisTag/DigitalComicReader/raw/master/images/readmeimages/62out.png)


Tasks to be completed:
- Panel ordering: given the corners and sizes of panels, determine the correct ordering
  - One idea is to use only the coordinates for the top-left corners of the rectangles (or rectangular convex hull). Cluster the y-values to create "rows", then go left to right within each row, starting from the top. This seems to accurately capture the reading process of comic panels.
      - Clustering can be done using kernel density esimation, or another 1-dimensional "clustering" method
      - Clustering will also take care of differences in y-values of a few pixels due to the morphological operations
- Recognition of non-paneled areas. i.e. find areas of the page that are not covered by recognized "panels" and consider them as panels. A first step towards recognizing non-traditional panel art.
- Text recognition: use an open-source library for text recognition and utilize this to discover speech bubbles, possibly through connected components
- Possible parameter optimization method for panel detection. Likely a brute force search over a small area through the parameter space for things like background variance threshold, dilation/erosion size and iterations, etc.


## Implementation tasks
- Image display scale calculation
- Animation between panels
