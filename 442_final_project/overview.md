### EECS 442 Research Project
The final project for the course was independent research on any topic of interest in computer vision.  My group decided to look into Optimal Character Recognition.  We built a complete OCR pipeline to process pdf text files and convert them to images and classify the characters using a Convolutional Neural Network.  This pipeline was tested on different fonts and with different CNN architectures.

#### Abstract
*Our goal in this paper is to propose an optical character recognition (OCR) pipeline that can correctly read an image only PDF file utilizing a Convolutional Neural Network (CNN) trained on a computer alphanumeric character dataset. Our proposed framework is essentially a three part pipeline.  We needed to read the PDF, build a model, and predict the PDF text.  The first part of the pipeline involves character recognition.  We achieved this by developing an algorithm that drew bounding boxes around individual characters in PDF files.  For the next part of the pipeline we built a CNN model and trained and validated it on the alphanumeric dataset.  To complete the pipeline, the model was used to predict the text of the PDF and the results were compared.  Our framework is capable of identifying characters of many different fonts successfully.  The proposed method shows performance of different models and different fonts.*

You can view our complete final paper [here](./EECS442_FinalProject.pdf). In it you can find the base CNN architecture and different iterations of layer and preprocessing experimentation.

#### Analysis
Our bounding box implementation extracts each character in a fairly homogeneous manner (128x128) with negligible errors. Our dataset of 62,000 images was broken into training, validation and testing sets. Our model was fairly robust and achieved an accuracy of 86%. After training our dataset with 40 epochs, we were able to minimize the loss to 0.26. 

Our Model  detects and classifies most characters perfectly, and seems to have problems with characterising between very similar characters such as the letter ‘o’ and the number 0, or the letter ‘e’ and the number 3. 

In addition to this, our model fails to classify punctuation at the moment. Although we can detect punctuation marks using our character detection pipeline, currently our classifier is not trained to classify those characters. This is something that could be solved quite easily by just expanding our training dataset to include punctuation marks such as commas, periods, quote marks etc.


#### Code
Additionally, the [code](./CNN.ipynb) to train and build the CNN was created using Google Colab.
