# CVLab

![alt tag](https://github.com/g4rr3t/ComputerVisionLab/blob/master/CVLab.PNG)  <br><br>

This project is part of a doctoral assignment to explore computer vision 
algorithms. Udacity's Intro to Computer Vision course provided the background and intuition behind many of the CV algorithms presented in this project. CVLab also implements many of the examples found in
<a href="https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_table_of_contents_imgproc/py_table_of_contents_imgproc.html">opencv-python tutorials</a>.<br>
Many of the examples had to be modified somewhat to run with Kivy, the python GUI library used. <br>

Project progress is recorded <a href="https://garretmoore.wordpress.com/">here</a> in my blog.<br>

main.py is the entry point to this python project.<br>

For guidance on how to use CVLab, <a href="https://github.com/g4rr3t/ComputerVisionLab/tree/master/walkthroughs">walkthroughs</a> are provided.

# Python Dependencies: <br>
Developed and tested in Python 3.4 <br>
Kivy (1.9.1) <https://kivy.org/docs/installation/installation.html> <br>
opencv-python <br>
matplotlib <br>
numpy <br>
os <br>
threading <br>

# Known Issue:
When closing CVLab by pressing x in the top right, Kivy makes an abort call to a Windows driver which isn't handled properly, causing the program to always crash on exit when using a Windows executable.  I have installed-reinstalled Kivy about 10 times now using different methods to try to resolve this without any success.