### EECS 442 Research Project
The final project for the course was independent research on any topic of interest in computer vision.  My group decided to look into Optimal Character Recognition.  We built a complete OCR pipeline to process pdf text files and convert them to images and classify the characters using a Convolutional Neural Network.  This pipeline was tested on different fonts and with different CNN architectures.

#### Abstract
*Our goal in this paper is to propose an optical character recognition (OCR) pipeline that can correctly read an image only PDF file utilizing a Convolutional Neural Network (CNN) trained on a computer alphanumeric character dataset. Our proposed framework is essentially a three part pipeline.  We needed to read the PDF, build a model, and predict the PDF text.  The first part of the pipeline involves character recognition.  We achieved this by developing an algorithm that drew bounding boxes around individual characters in PDF files.  For the next part of the pipeline we built a CNN model and trained and validated it on the alphanumeric dataset.  To complete the pipeline, the model was used to predict the text of the PDF and the results were compared.  Our framework is capable of identifying characters of many different fonts successfully.  The proposed method shows performance of different models and different fonts.*
<br>
You can view our complete final paper [here](./EECS442_FinalProject.pdf). In it you can find the base CNN architecture and different iterations of layer and preprocessing experimentation.

Additionally, the [code](./CNN.ipynb) to train and build the CNN was created using Google Colab.
