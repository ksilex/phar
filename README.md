# P-HAR: Porn Human Action Recognition

This is just a fun, side-project to see how State-of-the-art (SOTA) Human Action Recognition (HAR) models fare in the pornographic domain. HAR is a relatively new, active field of research in the deep learning domain, its goal being the identification of human actions from various input streams (e.g. video or sensor).

The pornography domain is interesting from a technical perspective because of its difficulties. Light variations, occlusions, and a great different camera positions make position (action) recognition inherently hard. We can have two identical positions and yet be captured in such a different camera angle to entirely confuse the model in its predictions.

This repository uses three different input streams in order to get the best possible results: rgb frames, skeleton, and audio. Correspondingly three different models are trained on these input streams and their results are merged through late fusion.

The best current accuracy reached by this multi-model model currently is **75.64%**, which is promising considering the small training set. This result will be improved in the future. The models work on spatio-temporal data, meaning that they processes video clips rather than single images. This is an inherently superior way of performing action recognition.

Currently, 17 actions are supported. You can find the complete list [here](resources/annotations/annotations.txt).

## Motivation & Usages

The idea behind this project is to try and apply the latest deep learning techniques (i.e. human action recognition) in the pornographic domain.

Once we have detailed information about the kind of actions/positions that are happening in a video a number of uses-cases can apply:

1. Improving the recommender system
2. Automatic tag generator
3. Automatic timestamp generator (when does an action start and finish)
4. Cutting content out (for example non-sexual content)

## Supported Features

First download the HAR models here. Then move them to their corresponding locations inside the `checkpoints/har` folder.

### Video Demo

Input a video and get a demo with the top predictions every X seconds.
`python tools/demo/multimodial_demo.py demos/subclip_subclip_561.mp4 demo2.mp4`

### Timestamp Generator

Same but gives json output.

### Tag Generator

`python tools/top_tags.py demo.json`

### Content Filtering

TODO

## Installation

This project is based on [MMAction2](https://github.com/open-mmlab/mmaction2). You can see the detailed installation steps [here](https://mmaction2.readthedocs.io/en/latest/install.html).

The following installation instructions are for ubuntu (hence should also work for Windows WSL). Check the links for details if you are interested in other operating systems.

1. Install Mim: `pip install git+https://github.com/open-mmlab/mim.git`
2. Install MMAction2: `mim install mmaction2 -f https://github.com/open-mmlab/mmaction2.git`
3. Install MMpose, [link](https://mmpose.readthedocs.io/en/latest/install.html)
4. Install MMDetection, [link](https://mmdetection.readthedocs.io/en/latest/get_started.html#installation)
5. Extra dependencies: `pip install -r requirements/extra.txt`

Of course, it is recommended that you have CUDA & CUDNN installed.

## Models

The SOTA results are archieved by late-fusing three models based on three input streams. This results in a significant improvements compared to only using an RGB-based model. Since more than one action might happen at the same time, it is best to consider the top 2 accuracy as a performance measurement. Hence, currently the multimodial model has a 75.64% accuracy. However, since the dataset is quite small and in total only ~50 experiments have been performed, there is a lot of room for improvement.

### Multi-Modial (Rgb + Skeleton + Audio)

Best performing models (performance & runtime wise) are timesformer for the RGB stream, poseC3D for the skeleton stream and resnet101 for the Audio stream. The results of this models are fused together based on fine-tuned weights about their importance in late-fusion.

Another approach would be to train a model with two of the input streams at a time (i.e. rgb+skeleton & rgb+audio) and then perhaps combine their results. But this wouldn't work due to the nature of the data. When it comes to the audio input streams, it can only be exploited for certain actions (e.g. deepthroat due to the gag reflex or anal due to a higher pitch), while for others it's not possible to derive any insight from their audio (e.g. missionary, doggy and cowgirl do not have any special characteristics to set them apart from an audio perspective).

Likewise the skeleton-based model can only be used in those instances where the pose estimation is accurate above a certain threshold. For example, for actions such as `scoop-up` or `the-snake` it's hard to get an accurate pose estimation given certain camera angles of the two actors due to the proximity of the human-body in the frame. This then influences the accuracy of the HAR model negatively. However, for actions such as doggy, cowgirl or missionary, the pose estimation is generally good enough to train a HAR model. In general, a more accurate pose estimation as well as more data is needed for this input stream.

#### Metrics

Accuracy | Weights
--- | ---
Top 1 Accuracy: 0.6329 <br> Top 2 Accuracy: 0.7564 <br> Top 3 Accuracy: 0.8035 <br> Top 4 Accuracy: 0.8384 <br> Top 5 Accuracy: 0.8646 | Rgb: 0.4 <br> Skeleton: 0.8 <br> Audio: 1.0

### RGB model - [TimeSformer](https://arxiv.org/abs/2102.05095)

The best results for an RGB model are achieved by the attention-based TimeSformer architecture. This model is also very fast in inference (~0.53s / 7s clips).

#### Metrics

Accuracy | Training Speed | Complexity
--- | --- | ---
top1_acc 0.5583 <br> top2_acc 0.6818 <br> top3_acc 0.7374 <br> top4_acc 0.7840 <br> top5_acc 0.8186 | Avg iter time: 0.3472 s/iter | Flops: 100.96 GFLOPs <br> Params: 121.27 M

#### Loss

![alt text](resources/plots/timesformer_loss.jpg)

#### Classes

17 annotations. See [annotations](resources/annotations/annotations.txt).

### Skeleton model - [PoseC3D](https://arxiv.org/abs/2104.13586)

The best results for a skeleton-based model are achieved by the CNN-based PoseC3D architecture. This model is also quite fast in inference (~3.3s / 7s clips).

#### Metrics

Accuracy | Training Speed | Complexity
--- | --- | ---
top1_acc 0.8130 <br> top2_acc 0.9191 <br> top3_acc 0.9748 | Avg iter time: 0.8616 s/iter| Flops: 17.83 GFLOPs <br> Params: 2.0 M

#### Loss

![alt text](resources/plots/posec3d_loss.jpg)

#### Classes

6 annotations. See [annotations](resources/annotations/annotations_pose.txt).

### Audio Model - Simple ResNet based on [Audiovisual SlowFast](https://arxiv.org/abs/2001.08740)

A simple ResNet 101, with some small tweaks, was used. This model definitely needs to be swapped with a better architecture. It is very fast in inference (0.05s / 7s audio clips).

#### Metrics

Accuracy | Training Speed
--- | ---
top1_acc 0.6867 <br> top2_acc 0.9038 <br> top3_acc 0.9663 | Avg iter time: 0.2747 s/iter

#### Loss

![alt text](resources/plots/audio_loss.jpg)

#### Classes

4 annotations. See [annotations](resources/annotations/annotations_audio.txt).

## Dataset

First things first, [here](https://www.womenshealthmag.com/sex-and-love/a19943165/sex-positions-guide/) is a list of definitions of the sex positions used in this project in case there is any confusion.

In general, a train/val split of 0.8/0.2 was used for all the datasets. The length of the clips in training & validation sets was 7 seconds. In total ~594 videos were annotated with a total of 2674 minutes. Check out the [annotation distribution](resources/annotation_distribution(min).json) in time (minutes) for each of the 17 classes for more information. The dataset was not perfectly annotated but the number of wrong annotations should be small and hence the drop in performance should be minimal.

In general, it can be said that this is a small dataset. Normally ~44 hours of footage would be enough for 17 actions. However, each position has a tremendous variety when it comes to camera perspectives, which makes the recognition task hard if there aren't enough samples. This would also mean that we should ideally have the same amount of footage for each different perspective. However, labeling the dataset was already very time-consuming and I didn't keep track of this point. A model trained on 3D poses might solve this problem. However, due to the fact that 3D pose estimation is less accurate than 2D pose estimation, and we already had problems with the accuracy of the latter, this hasn't been tried yet. However, ideally, if the dataset is big enough then the camera perspective problem should be naturally solved.

The dataset is also slightly imbalanced, which actually makes the rgb models slightly biased towards the positions (actions) that have more data.

### RGB

In total there are ~17.6K training clips and ~4.9k val clips. [This](resources/ann_dist_clip.jpg) plot shows the number of clips for each class. The RGB is considered the kernel input modality given that the audio modality is only applied to four classes and that the skeleton modality is rather fickle given the accuracy of 2D pose estimation. Various data augmentation techniques were applied such as rescaling, cropping, flipping, color inversion, gaussian blur, elastic transformation, affine transformation, etc. This further improves accuracy.

### (2D) Pose

Due to the variety of positions and camera angles, which make the pose estimation difficult, it's only possible to apply HAR on skeleton data only on a few of the actions. The clips generated were filtered based on two criteria:

1. The confidence of the pose information. Minimal confidence of 0.4 was chosen.

2. The number of frames in a clip that have a confidence higher than the minimal confidence score. Here a 0.4 rate was also used. In other words, if we have a 7s clip of 210 frames and only 70 frames have pose information with confidence higher than 0.4, then we exclude this clip from the pose dataset because only 33% of the frames have a confidence higher than 0.4 and our minimum threshold is 40%.

As a result, the pose dataset is significantly smaller than the original RGB dataset. Whereas there are about 4.9K testing clips for the RGB dataset, the pose dataset has only 815 clips. Therefore a bigger dataset is a must here.

### Audio

As a preliminary pre-processing step audios that are not loud enough were first pruned from the dataset.

In total there are about 5.9K training clips & 1.5K validation clips.

## Scripts' Docs

### Multimodial Demo

```shell
python tools/demo/multimodial_demo.py ${VIDEO_FILE} ${OUTPUT_FILE}
    [--det-config ${HUMAN_DETECTION_CONFIG_FILE}] \
    [--det-checkpoint ${HUMAN_DETECTION_CHECKPOINT}] \
    [--pose-config ${HUMAN_POSE_ESTIMATION_CONFIG_FILE}] \
    [--pose-checkpoint ${HUMAN_POSE_ESTIMATION_CHECKPOINT}] \
    [--skeleton-config ${SKELETON_BASED_ACTION_RECOGNITION_CONFIG_FILE}] \
    [--skeleton-checkpoint ${SKELETON_BASED_ACTION_RECOGNITION_CHECKPOINT}] \
    [--rgb-config ${RGB_BASED_ACTION_RECOGNITION_CONFIG_FILE}] \
    [--rgb-checkpoint ${RGB_BASED_ACTION_RECOGNITION_CHECKPOINT}] \
    [--audio-config ${AUDIO_BASED_ACTION_RECOGNITION_CONFIG_FILE}] \
    [--audio-checkpoint ${AUDIO_BASED_ACTION_RECOGNITION_CHECKPOINT}] \
    [--det-score-thr ${HUMAN_DETECTION_SCORE_THRE}] \
    [--label-maps ${LIST_OF_ACTION_ANNOTATION_FILES}] \
    [--num-processes ${NUM_PROC_USED_FOR_SUBCLIP_EXTRACTION}] \
    [--subclip-len ${PREDICTION_WINDOW}] \
    [--device ${DEVICE}] \
    [--coefficients ${COEFFICIENT_WEIGHTS}] \
    [--pose-score-thr ${POSE_ESTIMATION_SCORE_THRESHOLD}] \
    [--correct-rate ${RATE_OF_CORRECT_FRAMES_FOR_SKELETON_RECOGNITION}] \
    [--loudness-weights ${LOUDNESS_THRESHOLD_FOR_AUDIOS}] \
    [--topk ${TOP_K_ACCURACY}]
```

```shell
python tools/top_tags.py ${JSON_FILE}
    [--topk ${TOP_K_ACCURACY}]
    [--label-map ${ANNOTATION_FILE}]
```
