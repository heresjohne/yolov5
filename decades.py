import numpy as np
import torch
import torchvision
from torchvision import datasets, models, transforms
import torch.utils.data as data
import multiprocessing
#from sklearn.metrics import confusion_matrix
import streamlit as st
import time
#Loading the testing images
#Loading the saved model

def decades(opt):
        EVAL_MODEL= './models/model.pth'
        model = torch.load(EVAL_MODEL,map_location ='cpu')

        model.eval()




        bs = 8
        EVAL_DIR='./test/'
        EVAL_DIR = opt

        # Prepare the eval data loader
        eval_transform=transforms.Compose([
                transforms.Resize(size=256),
                transforms.CenterCrop(size=224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])])
        eval_dataset=datasets.ImageFolder(root=EVAL_DIR, transform=eval_transform)
        eval_loader=data.DataLoader(eval_dataset, batch_size=bs, shuffle=True, pin_memory=True)
        #eval_loader = opt
        # Enable gpu mode, if cuda available
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # Number of classes and dataset-size
        num_classes=len(eval_dataset.classes)
        dsize=len(eval_dataset)
        # Class label names
        print(eval_dataset.classes)
        #st.header(f'{eval_dataset.classes}')
        class_names=['2000-2005','2005-2015','1995-2000','2015-2025','1975-1985','1985-1995']
#         if option == 0:
                
#         if option == 1:
#         if option == 2:
#         if option == 3:
#         if option == 4:
#         if option == 5:
                
                
        #class_names=['2000s', '2010s', '90s', '2020s', '70s', '80s']
        # Initialize the prediction and label lists
        predlist=torch.zeros(0,dtype=torch.long, device='cpu')
        lbllist=torch.zeros(0,dtype=torch.long, device='cpu')
        # Evaluate the model accuracy on the dataset
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in eval_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                count = 0
                for n in predicted: 
                  pred = str(predicted[count])
                  pred = pred.lstrip('tensor()')
                  pred = int(pred.rstrip(')'))
                  pred = class_names[pred]
                  #option = int(option)
                  #lbl = option

                  print('Predicted Decade is:', pred)
                  #print('Actual Decade is',lbl)
                  count +=1 
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                predlist=torch.cat([predlist,predicted.view(-1).cpu()])
                lbllist=torch.cat([lbllist,labels.view(-1).cpu()])
        # Overall accuracy
        print(predlist,lbllist)
        overall_accuracy=100 * correct / total
        option = st.selectbox('Which decade is this album from?',('1995-2000','1975-1985','1985-1995','2000-2005','2005-2015','2015-2025'))
        st.subheader(f'I think this album is from the following decade:{pred}. It actually is: {option}')

        print('Accuracy of the network on the {:d} test images: {:.2f}%'.format(dsize, 
            overall_accuracy))
        # Confusion matrix
        #conf_mat=confusion_matrix(lbllist.numpy(), predlist.numpy())
        #print('Confusion Matrix')
        #print('-'*16)
        #print(conf_mat,'\n')
