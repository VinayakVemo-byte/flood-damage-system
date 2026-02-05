import torch
from torchvision import models,transforms
from PIL import Image

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

model=models.resnet18(weights=None)
model.conv1=torch.nn.Conv2d(6,64,7,2,3,bias=False)
model.fc=torch.nn.Linear(512,1)

model.load_state_dict(torch.load("models/damage.pth",map_location=device))
model.to(device)
model.eval()

t=transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

def predict_flood(before_path,after_path):

    x1=t(Image.open(before_path).convert("RGB"))
    x2=t(Image.open(after_path).convert("RGB"))

    x=torch.cat([x1,x2],0).unsqueeze(0).to(device)

    with torch.no_grad():
        y=model(x).item()

    return round(max(0,min(100,y)),2)
