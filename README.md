# ECE-750-Project
<h1 align="center">Enhancing Human-Robot Interaction in Healthcare: A Study on Nonverbal Communication Cues and Trust Dynamics with NAO Robot Caregivers</h1>

<p align="center">
  <strong>S M Taslim Uddin Raju</strong><br>
  Department of Electrical and Computer Engineering<br>
  University of Waterloo, Waterloo, ON, Canada<br>
  <a href="mailto:smturaju@uwaterloo.ca">smturaju@uwaterloo.ca</a>
</p>

## Abstract
<div align="justify">
Captioning Whole Slide Images (WSIs) for pathological analysis is an essential but not extensively explored aspect of computer-aided pathological diagnosis. Challenges arise from insufficient datasets and the effectiveness of model training. Generating automatic caption reports for various gastric adenocarcinoma images is another challenge. In this paper, we introduce a hybrid method referred to as TransUAAE-CapGen to generate histopathological captions from WSI patches. The TransUAAE-CapGen architecture consists of a hybrid UNet-based Advereasrial Autoencoder (AAE) for feature extraction and a transformer for caption generation. The hybrid UNet-based AAE extracted complex tissue properties from histopathological patches, transforming them into low-dimensional embeddings. The embeddings are then fed into the transformer to generate concise captions. Our proposed method is validated using the PatchGastricADC22 dataset. The TransUAAE-CapGen model provides the best estimated accuracy of  BLEU-4 = 86.8%, METEOR = 59.6%, a ROUGE = 89.3%, and CIDEr = 7.72%. Experimental analysis indicates that the TransUAAE-CapGen architecture outperforms the traditional LSTM-based model for the caption generation task. Our findings reveal that the proposed architecture can effectively generate accurate and precise reports for medical image analysis.
</div>

<div align="center">
    <img src="Image/Fig1.png" alt="Alt text" title="Hover text" height="500" width="500"/>
    <p><em>Figure 1: Webot simulation of old age home or apartment with Nao robot as caregiver for monitoring the health condition of elderly people.</em></p>
</div>
