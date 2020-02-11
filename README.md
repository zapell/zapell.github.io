# Color From Greyscale Photos

This project focused on aligning RBG image channels to create a color image from black and white photos.

The motivation comes from Russian photographer Sergei Mikhailovich Prokudin-Gorskii (1863-1944), via a project invented by Russian-American vision researcher, Alexei A. Efros (1975-present).  Sergei was a visionary who believed in a future with color photography. During his lifetime, he traveled across the Russian Empire taking photographs through custom color filters at the whim of the czar. To capture color for the photographers of the future, he decided to take three separate black-and-white pictures of every scene, each with a red, green, or blue color filter in front of the camera.


## Part 1
The main objective was to transform the 3 channel black and white image  
![this](https://github.com/zapell/eecs442_p1/blob/master/00125v.jpg)


to  
![color image](https://github.com/zapell/eecs442_p1/blob/master/00125aligned.jpg)


This involved calculating the best offset by holding one of the color channels constant and figuring out how much in the x and y direction the image needed to be moved.

Another example of a picture of Efros himself  
![1](https://github.com/zapell/eecs442_p1/blob/master/efros_tableau.jpg)   
![2](https://github.com/zapell/eecs442_p1/blob/master/aligned_efros_tableau.jpg)

## Part 2
For small images this offset algorithm is quick enough, but for large images it can be extremely inefficient.  To fix this problem I implemented an image pyramid where each level downsamples the last by a factor of 4.  I calculated the offset at each level and aligned the image through the pyramid.  This method allows a much larger coverage of offsets between channels more efficiently than a brute force search would.  

A large image of scenic Seoul  
![here](https://github.com/zapell/eecs442_p1/blob/master/seoul_tableau.jpg)  
does not lose any of its beauty through the pyramid algorithm.  
![aligned](https://github.com/zapell/eecs442_p1/blob/master/seoul_aligned.jpg)
