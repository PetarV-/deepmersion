import io
import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision.models.vgg import vgg16
from torchvision import transforms as trn
from torch.nn import functional as F
from PIL import Image

vgg_model_cache = vgg16(pretrained=True)

def classify_objects(img_name):
    global vgg_model_cache

    if vgg_model_cache is None:
        model = vgg16(pretrained=True)
        vgg_model_cache = model
    else:
        model = vgg_model_cache

    if torch.cuda.is_available():
        model = model.cuda()
    model.eval()

    # load the image transformer
    centre_crop = trn.Compose([
            trn.Resize((256,256)),
            trn.CenterCrop(224),
            trn.ToTensor(),
            trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # load the class label
    file_name = 'categories_imagenet.txt'

    img = Image.open(io.BytesIO(img_name))
    input_img = V(centre_crop(img).unsqueeze(0))

    if torch.cuda.is_available():
        input_img = input_img.cuda()
    logit = model.forward(input_img)
    h_x = F.softmax(logit, 1).data.squeeze()
    print(h_x)
    return h_x


#classify_objects(open('cafe.jpg', "rb").read())
