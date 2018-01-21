# deepmersion
![deepmersion](https://raw.githubusercontent.com/PetarV-/deepmersion/master/logo-scaled.png?token=AD_VHMMLyhlkxYhD6SdQPOo38S976D_2ks5abWcXwA%3D%3D)

own your surroundings

## Motivation
Maintaining focus in today's world can often be extremely hard, with numerous distractions left, right and centre
often impeding one's capability to achieve the truly important objectives _(cf. performing well at hackathons)_. One incredible
resource for dealing with these issues are ambiental sound generators - the proper sound, in conjunction with noise-cancellation headphones,
can present an incredible boost to one's productivity indeed.

Unfortunately, we have found that existing solutions for ambient sound generations either restrict users to a certain fixed
sound ([rainymood.com](https://rainymood.com)), or an elaborate interface for manually mixing a multitude of sounds ([asoftmurmur.com](https://asoftmurmur.com)).
These options thus either give the user too little or too much choice---the former's imposed sound choice might not always be appropriate, while the
latter might cause significant time to be spent tuning the sound, thus inadvertently causing an additional distraction (as at least one of the creators
of this repository has experienced personally!).

Here we present [**deepmersion.com**](http://deepmersion.com)---a prototype of the **_'one ambient sound generator to rule them all'_**, simultaneously
leveraging _three state-of-the-art neural network architectures_ to provide the user with the **optimal level of choice**.

## High-level outline
The key principle of _immersion_ in sound requires, in our opinion, either for one to disengage other senses (e.g. by closing their eyes), or
for the sound to **reflect a distilled version of one's surroundings**, keeping the auditory experience coherent with the perceived world, and thus
feeling less artificial. As our primary use case involves productivity-boosting (although other applications of deepmersion are, of course, more than possible),
the first option can be quickly discarded. Therefore, _we would ideally want the generated ambient sound to match the context of the user's surroundings_.
Deepmersion was built with this as its primary objective---especially, making it way simpler to do so compared to the extensive manual fine-tuning offered by
existing solutions. The user is able to provide an image to our system (for our preferred use case, this image will be a shot of the user's immediate
surroundings), and the system will respond with an appropriate ambient sound that captures the content of the image.

## Internals overview
When an image is submitted to the system, its content is analysed by two state-of-the-art neural networks for object and scene recognition:

* VGG-16 ([Simonyan and Zisserman, 2014](https://arxiv.org/abs/1409.1556)) for extracting the most prominent objects on an image (pre-trained on the ImageNet dataset - 1000 object classes);
* Places-365-CNN ([Zhou et al., 2017](http://ieeexplore.ieee.org/document/7968387/)) for extracting the scene characteristics of an image (pre-trained on the Places2 dataset - 365 scene classes).

These are capable of extracting robust high-level image features. In order to match the image with appropriate sounds, a database of ambiental sounds is constructed---in our case, we have constructed
a dataset of various superimpositions of the basic sounds from [A Soft Murmur](https://asoftmurmur.com). These sounds are then fed through a SoundNet neural network architecture
([Aytar et al., 2016](https://arxiv.org/abs/1610.09001)), which is trained to predict content (objects and scenes) in videos _while only having access to the sound information_. It has been pre-trained
on hundreds of gigabytes of MP3 files, and therefore also offers a robust representation of auditory features. The most appropriate sound is then chosen based on the Kullback-Leibler (KL) divergence between
the predictions of the image networks and the predictions of the SoundNet.

All models have been expressed in the PyTorch framework, enabling seamless integration with Python workflows.

## Additional features

## License
MIT
