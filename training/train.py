import os
import torch
from torch.utils.data import DataLoader
from src.dataset import AnswerAreaDataset
from src.model import get_model
from tqdm import tqdm

EPOCHS = 10
BATCH_SIZE = 2
LEARNING_RATE = 0.005
NUM_WORKERS = 0

def collate_fn(batch):
    return tuple(zip(*batch))

def train():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(f"Using device: {device}")

    # Use absolute paths or paths relative to the project root
    dataset_train_dir = os.path.join("..", "datasets", "skripsi ameng.v2i.coco", "train")
    dataset_train_ann = os.path.join(dataset_train_dir, "_annotations.coco.json")
    
    dataset_valid_dir = os.path.join("..", "datasets", "skripsi ameng.v2i.coco", "valid")
    dataset_valid_ann = os.path.join(dataset_valid_dir, "_annotations.coco.json")

    # For now, we will use basic torchvision transforms (already handled in dataset.py default)
    train_dataset = AnswerAreaDataset(root_dir=dataset_train_dir, ann_file=dataset_train_ann)
    valid_dataset = AnswerAreaDataset(root_dir=dataset_valid_dir, ann_file=dataset_valid_ann)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS, collate_fn=collate_fn)
    valid_loader = DataLoader(valid_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, collate_fn=collate_fn)

    model = get_model(num_classes=2)
    model.to(device)

    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=LEARNING_RATE, momentum=0.9, weight_decay=0.0005)
    
    # A simple learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

    print("Starting training...")
    best_val_loss = float('inf')
    
    for epoch in range(EPOCHS):
        model.train()
        epoch_loss = 0
        
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}")
        for images, targets in progress_bar:
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
            
            epoch_loss += losses.item()
            progress_bar.set_postfix(loss=losses.item())
            
        lr_scheduler.step()
        avg_train_loss = epoch_loss / len(train_loader)
        print(f"Epoch {epoch+1} - Avg Train Loss: {avg_train_loss:.4f}")
        
        # Note: torchvision Faster R-CNN doesn't return loss when in eval() mode.
        # So we evaluate by keeping it in train() mode but with torch.no_grad()
        # This is a bit of a workaround to get validation loss.
        model.train() 
        val_loss = 0
        with torch.no_grad():
            for images, targets in valid_loader:
                images = list(image.to(device) for image in images)
                targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
                
                loss_dict = model(images, targets)
                losses = sum(loss for loss in loss_dict.values())
                val_loss += losses.item()
                
        avg_val_loss = val_loss / len(valid_loader)
        print(f"Epoch {epoch+1} - Avg Valid Loss: {avg_val_loss:.4f}")
        
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), os.path.join("checkpoints", "best_model.pth"))
            print(f"-> Saved new best model with val_loss: {best_val_loss:.4f}")
            
    print("Training finished.")
    torch.save(model.state_dict(), os.path.join("checkpoints", "last_model.pth"))

if __name__ == '__main__':
    train()
