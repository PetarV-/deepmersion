import io
import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision.models.vgg import vgg16
from torchvision import transforms as trn
from torch.nn import functional as F
from PIL import Image

def classify_objects(img_name):
    model = vgg16(pretrained=True)
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

    # forward pass
    logit = model.forward(input_img)
    h_x = F.softmax(logit, 1).data.squeeze()
    return h_x
#classify_objects('cafe.jpg')
