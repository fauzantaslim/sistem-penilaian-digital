import os
import torch
from torchvision.transforms import functional as F
from PIL import Image, ImageDraw, ImageFont
from model import get_model
import argparse

def sort_boxes(boxes):
    """
    Urutkan bounding box dari atas ke bawah.
    Jika sejajar (selisih ymin kecil), urutkan dari kiri ke kanan.
    """
    # boxes shape: (N, 4) -> [xmin, ymin, xmax, ymax]
    boxes_list = boxes.tolist()
    # add index
    boxes_with_idx = [(i, b) for i, b in enumerate(boxes_list)]
    
    # Sort by ymin first
    # We define a threshold for 'same line' (e.g., 20 pixels)
    # But a simple sort by ymin is usually enough if answers are cleanly stacked
    boxes_with_idx.sort(key=lambda x: (x[1][1], x[1][0]))
    return boxes_with_idx

def run_inference(image_path, model_path, output_dir, conf_threshold=0.5):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    
    model = get_model(num_classes=2)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    img = Image.open(image_path).convert("RGB")
    img_tensor = F.to_tensor(img).unsqueeze(0).to(device)

    with torch.no_grad():
        predictions = model(img_tensor)[0]

    # Filter by confidence
    boxes = predictions['boxes']
    scores = predictions['scores']
    
    keep = scores > conf_threshold
    boxes = boxes[keep]
    scores = scores[keep]

    # Sort boxes
    sorted_boxes = sort_boxes(boxes)

    # Visualization
    draw = ImageDraw.Draw(img)
    
    print(f"Found {len(sorted_boxes)} answer areas.")
    
    for i, (orig_idx, bbox) in enumerate(sorted_boxes):
        xmin, ymin, xmax, ymax = bbox
        score = scores[orig_idx].item()
        
        # Draw box
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=3)
        
        # Draw label
        text = f"Jawaban {i+1} ({score:.2f})"
        # Draw text background
        draw.rectangle([(xmin, ymin-15), (xmin + len(text)*6, ymin)], fill="red")
        draw.text((xmin, ymin-15), text, fill="white")
        
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(image_path)
    out_path = os.path.join(output_dir, f"detected_{base_name}")
    img.save(out_path)
    print(f"Saved detection result to {out_path}")
    
    return sorted_boxes, img

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='Path to input image')
    parser.add_argument('--model', type=str, default='../checkpoints/best_model.pth', help='Path to model checkpoint')
    parser.add_argument('--output', type=str, default='../outputs/detections', help='Output directory')
    parser.add_argument('--conf', type=float, default=0.5, help='Confidence threshold')
    
    args = parser.parse_args()
    run_inference(args.image, args.model, args.output, args.conf)
