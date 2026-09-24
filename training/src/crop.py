import os
from PIL import Image

def crop_answers(image, sorted_boxes, output_dir, base_name):
    """
    image: PIL Image object
    sorted_boxes: list of tuples (original_index, [xmin, ymin, xmax, ymax])
    """
    os.makedirs(output_dir, exist_ok=True)
    crop_paths = []
    
    for i, (_, bbox) in enumerate(sorted_boxes):
        xmin, ymin, xmax, ymax = bbox
        
        # Crop image
        crop_img = image.crop((xmin, ymin, xmax, ymax))
        
        # Save
        filename = f"{base_name}_answer_{i+1}.jpg"
        out_path = os.path.join(output_dir, filename)
        crop_img.save(out_path)
        crop_paths.append(out_path)
        
    print(f"Saved {len(crop_paths)} cropped answers to {output_dir}")
    return crop_paths

if __name__ == '__main__':
    print("This module is meant to be imported and used within a pipeline.")
