import os
import json
import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms.functional as TF

class AnswerAreaDataset(Dataset):
    def __init__(self, root_dir, ann_file, transforms=None):
        self.root_dir = root_dir
        self.transforms = transforms
        
        with open(ann_file, 'r') as f:
            self.coco = json.load(f)
            
        self.images = self.coco['images']
        self.annotations = self.coco['annotations']
        
        # Map image_id to annotations
        self.img_to_anns = {}
        for ann in self.annotations:
            img_id = ann['image_id']
            if img_id not in self.img_to_anns:
                self.img_to_anns[img_id] = []
            self.img_to_anns[img_id].append(ann)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_info = self.images[idx]
        img_id = img_info['id']
        file_name = img_info['file_name']
        img_path = os.path.join(self.root_dir, file_name)
        
        img = Image.open(img_path).convert("RGB")
        
        anns = self.img_to_anns.get(img_id, [])
        boxes = []
        labels = []
        
        for ann in anns:
            # COCO bbox format: [xmin, ymin, width, height]
            # Faster R-CNN expects: [xmin, ymin, xmax, ymax]
            xmin, ymin, w, h = ann['bbox']
            xmax = xmin + w
            ymax = ymin + h
            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(1) # answer_area is 1
            
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        image_id = torch.tensor([img_id])
        
        if len(boxes) == 0:
            boxes = torch.empty((0, 4), dtype=torch.float32)
        
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0]) if len(boxes) > 0 else torch.empty((0,), dtype=torch.float32)
        iscrowd = torch.zeros((len(labels),), dtype=torch.int64)
        
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            # In a real implementation with albumentations, 
            # you'd need to convert PIL to numpy and handle bbox transformations here.
            # For simplicity, we just use basic torchvision transforms if any.
            img = self.transforms(img)
        else:
            img = TF.to_tensor(img)

        return img, target
