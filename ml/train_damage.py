import os,time
import torch
import pandas as pd
from torchvision import models,transforms
from PIL import Image
from torch.utils.data import Dataset,DataLoader
from tqdm import tqdm

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:",device)
if device.type=="cuda":
    print("GPU:",torch.cuda.get_device_name(0))

class XBD(Dataset):

    def __init__(self):
        self.df=pd.read_csv("data/xbd/flood_labels.csv").sample(3000)
        self.t=transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.df)

    def __getitem__(self,i):

        while True:

            base=self.df.iloc[i,0]
            y=float(self.df.iloc[i,1])

            b=f"data/xbd/before/{base}_pre_disaster.png"
            a=f"data/xbd/after/{base}_post_disaster.png"

            if os.path.exists(b) and os.path.exists(a):

                x1=self.t(Image.open(b).convert("RGB"))
                x2=self.t(Image.open(a).convert("RGB"))

                return torch.cat([x1,x2],0), torch.tensor([y],dtype=torch.float32)

            i=(i+1)%len(self.df)

ds=XBD()
dl=DataLoader(ds,batch_size=8,shuffle=True)

model=models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.conv1=torch.nn.Conv2d(6,64,7,2,3,bias=False)
model.fc=torch.nn.Linear(512,1)
model.to(device)

loss_fn=torch.nn.MSELoss()
opt=torch.optim.Adam(model.parameters(),1e-4)

EPOCHS=10

global_start=time.time()

for e in range(EPOCHS):

    epoch_start=time.time()
    total_loss=0

    print(f"\nEpoch {e+1}/{EPOCHS}")

    bar=tqdm(dl)

    for x,y in bar:

        x,y=x.to(device),y.to(device)

        pred=model(x)
        loss=loss_fn(pred,y)

        opt.zero_grad()
        loss.backward()
        opt.step()

        total_loss+=loss.item()

        bar.set_description(f"Loss {loss.item():.4f}")

    avg=total_loss/len(dl)

    epoch_time=time.time()-epoch_start
    elapsed=time.time()-global_start
    remaining=(elapsed/(e+1))*(EPOCHS-(e+1))

    print(f"Epoch Loss: {avg:.4f}")
    print(f"Epoch Time: {epoch_time:.1f}s")
    print(f"Estimated Remaining: {remaining/60:.1f} min")

os.makedirs("models",exist_ok=True)
torch.save(model.state_dict(),"models/damage.pth")

print("\nFlood regression model saved")
