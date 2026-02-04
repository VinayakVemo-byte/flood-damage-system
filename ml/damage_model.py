import torch
from torchvision import models, transforms
from PIL import Image
import torch.nn.functional as F

model = models.resnet18(weights=None)
model.conv1 = torch.nn.Conv2d(6,64,7,2,3,bias=False)
model.fc = torch.nn.Linear(512,4)

model.load_state_dict(torch.load("models/damage.pth", map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

labels = ["No Damage","Minor","Major","Destroyed"]

def predict_damage(before, after):

    b = transform(Image.open(before).convert("RGB"))
    a = transform(Image.open(after).convert("RGB"))

    x = torch.cat([b,a],0).unsqueeze(0)

    with torch.no_grad():
        out = model(x)
        probs = F.softmax(out, dim=1)

    cls = torch.argmax(probs,1).item()
    confidence = probs[0][cls].item()

    # Low confidence fallback
    if confidence < 0.40:
        return "Uncertain"

    return labels[cls]
