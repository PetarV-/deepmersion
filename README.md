# deepmersion
<img src="https://raw.githubusercontent.com/PetarV-/deepmersion/master/logo-scaled.png?token=AD_VHMMLyhlkxYhD6SdQPOo38S976D_2ks5abWcXwA%3D%3D" width="200">

own your surroundings

## Motivation
Maintaining focus in the present can be extremely hard. Numerous distractions left, right and centre
often impede us to achieve the truly important objectives _(cf. performing well at hackathons)_. One incredible
resource for dealing with these issues are ambient sound generators - the proper sound, along with noise-cancellation headphones,
can plentifully boost one's productivity.

Unfortunately, we have found that existing solutions for generating ambient sounds either restrict users to one specific
sound ([rainymood.com](https://rainymood.com)), or have an elaborate interface for manually mixing a multitude of sounds ([asoftmurmur.com](https://asoftmurmur.com)).
These options give the user either too little or too much choice---the former's imposed sound choice might not always be appropriate to the surroundings, while the
latter might add significant time spent tuning the sound, inadvertently causing an additional distraction (as at least one of the creators
of this repository has experienced personally!).

We present [**deepmersion.com**](http://deepmersion.com)---a prototype of the **_'one ambient sound generator to rule them all'_**, simultaneously
leveraging _three state-of-the-art neural network architectures_ to provide the user with the **optimal level of choice**.

## High-level outline
We believe that the key principle of _immersion_ in sound requires either disengaging other senses (e.g. by closing their eyes), or
the sound **reflecting a distilled version of one's surroundings**. This keeps the auditory experience consistent with the perceived world, making it less artificial. The first option can be quickly discarded, since the primary use case of our app involves productivity-boosting (of course, other applications of deepmersion are more than possible). Therefore, _we would ideally want the generated ambient sound to match the user's surroundings_.
Deepmersion was built with this as primary objective---specifically, making it way simpler to do so compared to the extensive manual fine-tuning offered by
existing solutions. The user provides an image to our system (for our main use case, this will be a shot of the user's immediate
surroundings) and the system responds with an appropriate ambient sound that captures the content of the image.

We find this approach to be _optimal_ - there are no adjustment requirements from the user, with the sound generated still often being appropriate.

## Internals overview
When an image is submitted to the system, its content is analysed by two state-of-the-art neural networks for object and scene recognition:

* VGG-16 ([Simonyan and Zisserman, 2014](https://arxiv.org/abs/1409.1556)) for extracting the most prominent objects from an image (pre-trained on the ImageNet dataset - 1000 object classes);
* Places-365-CNN ([Zhou et al., 2017](http://ieeexplore.ieee.org/document/7968387/)) for extracting the scene characteristics of an image (pre-trained on the Places2 dataset - 365 scene classes).

These are capable of extracting robust high-level image features. In order to match the image with appropriate sounds, a database of ambient sounds is constructed---in our case, we have built
a dataset of superimpositions of the 10 basic sounds from [A Soft Murmur](https://asoftmurmur.com). These sounds are then fed through a SoundNet neural network architecture
([Aytar et al., 2016](https://arxiv.org/abs/1610.09001)), which is trained to predict content (objects and scenes) in videos _while only having access to the sound information_. It has been pre-trained
on hundreds of gigabytes of MP3 files, and therefore offers a robust representation of auditory features. The most appropriate sound is then chosen based on the Kullback-Leibler (KL) divergence between
the image network predictions and the SoundNet predictions.

All models have been expressed in the PyTorch framework, enabling seamless integration with Python workflows.

## Additional features

Aside from the basic functionality mentioned above, we have implemented several extensions:

- Our system is primarily accessed via a web browser (on both desktop and mobile), but we also provide a mobile application that immediately interfaces to a mobile phone's camera, for maximal convenience;
- We support _two_ modes of generating sounds: one that searches a fixed database of superimposed sounds, and one that creates a custom superimposed sound, dependent on how similar each basic sound is to the input image, as well as a single "chatter" slider (which controls the general volume level of each sound in the combination). Furthermore, the user may choose to disable either the object or scene features
(depending on the sort of focus desired when making decisions).
- In order to visualise the system's decisions (potentially paving the way to user feedback in the future), we incorporated the class activation mapping (CAM) algorithm ([Zhou et al., 2015](https://arxiv.org/abs/1512.04150))
to generate a heatmap of the most important regions of the given image in the networks' decision-making process.

Finally, keen users can find sufficient code in our repository to construct their own databases (of not necessarily ambient sounds!).

Further ideas and feedback are, of course, very welcome! _Own your surroundings_.

## License
MIT
