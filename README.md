# deepmersion
![deepmersion][https://raw.githubusercontent.com/PetarV-/deepmersion/master/frontend/deepmersion/src/logo.svg?token=AD_VHLCxnBNot5T5gdEoJYtcdhdFa-0Xks5abWVIwA%3D%3D]

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
existing solutions.

## License
MIT
