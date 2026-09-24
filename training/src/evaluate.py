import os
import torch
from torch.utils.data import DataLoader
from dataset import AnswerAreaDataset
from model import get_model
from torchmetrics.detection.mean_ap import MeanAveragePrecision
from pprint import pprint

def collate_fn(batch):
    return tuple(zip(*batch))

def evaluate():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(f"Evaluating on device: {device}")

    # Use test dataset
    dataset_test_dir = os.path.join("..", "..", "datasets", "skripsi ameng.v2i.coco", "test")
    dataset_test_ann = os.path.join(dataset_test_dir, "_annotations.coco.json")

    test_dataset = AnswerAreaDataset(root_dir=dataset_test_dir, ann_file=dataset_test_ann)
    test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers=0, collate_fn=collate_fn)

    model = get_model(num_classes=2)
    model_path = os.path.join("..", "checkpoints", "best_model.pth")
    if not os.path.exists(model_path):
        print(f"Error: Model checkpoint not found at {model_path}")
        return
        
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    metric = MeanAveragePrecision(box_format='xyxy', iou_type='bbox')

    print("Running evaluation on test set...")
    with torch.no_grad():
        for images, targets in test_loader:
            images = list(img.to(device) for img in images)
            
            # Predict
            preds = model(images)
            
            # Move targets to device
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
            
            metric.update(preds, targets)

    print("\nEvaluation Results (Test Set):")
    results = metric.compute()
    
    # Print formatted results
    print(f"mAP (IoU=0.50:0.95): {results['map'].item():.4f}")
    print(f"mAP (IoU=0.50)     : {results['map_50'].item():.4f}")
    print(f"mAP (IoU=0.75)     : {results['map_75'].item():.4f}")
    print(f"mAR (maxDets=100)  : {results['mar_100'].item():.4f}")

if __name__ == '__main__':
    evaluate()
