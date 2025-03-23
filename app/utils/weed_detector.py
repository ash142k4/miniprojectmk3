import os
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import torch

class WeedDetector:
    def __init__(self):
        """Initialize the weed detector with YOLOv8 model."""
        # Create models directory if it doesn't exist
        os.makedirs('app/models', exist_ok=True)
        
        # Path to the YOLOv8 model weights
        model_path = 'app/models/yolov8n.pt'
        
        # Download the model if it doesn't exist
        if not os.path.exists(model_path):
            # For demonstration, using the pretrained YOLOv8 model
            # In a real application, you would fine-tune this on weed data
            print("Downloading YOLOv8 model...")
            self.model = YOLO('yolov8n.pt')
            self.model.save(model_path)
        else:
            print("Loading existing YOLOv8 model...")
            self.model = YOLO(model_path)
        
        # Growth stage classifier would be a separate model in a real application
        self.growth_stages = ['Seedling', 'Vegetative', 'Flowering', 'Mature']
    
    def detect(self, image_path):
        """
        Detect weeds in the image using YOLOv8.
        
        Args:
            image_path (str): Path to the input image.
            
        Returns:
            dict: Detection results with bounding boxes and remedies.
        """
        try:
            # Run YOLOv8 inference
            results = self.model(image_path, conf=0.25)
            
            # Process the results
            detections = []
            for result in results:
                boxes = result.boxes.cpu().numpy()
                
                for i, box in enumerate(boxes):
                    # For demonstration purposes, we're checking if the detected object
                    # could be a weed (in real app, you'd use a model fine-tuned for weeds)
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    
                    # If the model detects plants or objects that could be weeds
                    # In a real app, the model would be specifically trained for weed types
                    weed_type = self._classify_weed_type(image_path, box.xyxy[0])
                    
                    # Only include if it's detected as a weed
                    if weed_type:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        detection = {
                            'id': i,
                            'weed_type': weed_type,
                            'confidence': confidence,
                            'bbox': [x1, y1, x2, y2],
                            'remedy': self._get_remedy(weed_type)
                        }
                        detections.append(detection)
            
            # Save the annotated image
            annotated_img_path = self._save_annotated_image(image_path, results)
            
            return {
                'detections': detections,
                'annotated_image': os.path.basename(annotated_img_path)
            }
            
        except Exception as e:
            print(f"Error during weed detection: {e}")
            return {'error': str(e)}
    
    def detect_growth_stage(self, image_path):
        """
        Detect the growth stage of plants in the image.
        
        Args:
            image_path (str): Path to the input image.
            
        Returns:
            dict: Growth stage detection results.
        """
        try:
            # In a real application, this would use a specialized model
            # For demonstration, we'll use a simulated approach
            
            # Run object detection first
            detection_results = self.detect(image_path)
            
            if 'error' in detection_results:
                return {'error': detection_results['error']}
            
            # Simulate growth stage classification
            # In a real app, this would analyze features of the detected plants
            image = cv2.imread(image_path)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Use color distribution as a simple heuristic for growth stage
            # (Real application would use a more sophisticated approach)
            green_lower = np.array([35, 50, 50])
            green_upper = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, green_lower, green_upper)
            
            # Calculate percentage of green pixels (simple feature)
            green_percentage = (np.sum(green_mask > 0) / (image.shape[0] * image.shape[1])) * 100
            
            # Determine growth stage based on green percentage (simplified logic)
            if green_percentage < 5:
                stage = self.growth_stages[0]  # Seedling
            elif green_percentage < 15:
                stage = self.growth_stages[1]  # Vegetative
            elif green_percentage < 25:
                stage = self.growth_stages[2]  # Flowering
            else:
                stage = self.growth_stages[3]  # Mature
            
            return {
                'growth_stage': stage,
                'confidence': min(0.9, max(0.6, green_percentage / 30)),  # Simulated confidence
                'features': {
                    'green_percentage': green_percentage,
                    'plant_count': len(detection_results.get('detections', [])),
                },
                'detections': detection_results
            }
            
        except Exception as e:
            print(f"Error during growth stage detection: {e}")
            return {'error': str(e)}
    
    def _classify_weed_type(self, image_path, bbox):
        """
        Classify the type of weed based on the cropped region.
        
        In a real application, this would use a specialized classifier.
        For demonstration, we're using a simplified approach.
        
        Args:
            image_path (str): Path to the input image.
            bbox (list): Bounding box coordinates [x1, y1, x2, y2].
            
        Returns:
            str: The classified weed type.
        """
        # Common weed types
        weed_types = [
            "Dandelion",
            "Crabgrass",
            "Thistle",
            "Chickweed",
            "Bindweed",
            "Nutsedge",
            "Purslane",
            "Pigweed",
            "Wild Mustard",
            "Foxtail"
        ]
        
        try:
            # Load the image
            img = cv2.imread(image_path)
            x1, y1, x2, y2 = map(int, bbox)
            
            # Crop the region
            crop = img[y1:y2, x1:x2]
            
            # In a real application, a dedicated weed classifier would be used here
            # For demonstration, we're using color features as a simple heuristic
            
            # Convert to HSV and get color features
            hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
            avg_hue = np.mean(hsv[:, :, 0])
            
            # Simple heuristic to assign weed type based on average hue
            # (In a real app, this would be a proper classifier)
            weed_index = int((avg_hue / 180) * len(weed_types))
            weed_index = max(0, min(weed_index, len(weed_types) - 1))
            
            return weed_types[weed_index]
            
        except Exception as e:
            print(f"Error in weed classification: {e}")
            return "Unknown Weed"
    
    def _get_remedy(self, weed_type):
        """
        Get recommended remedy for the detected weed type.
        
        Args:
            weed_type (str): The type of weed detected.
            
        Returns:
            dict: Remedy recommendations.
        """
        # Dictionary of common weed remedies (simplified)
        remedies = {
            "Dandelion": {
                "organic": "Pull by hand, making sure to remove the entire taproot. Use a dandelion puller tool for efficient removal.",
                "chemical": "Apply broadleaf herbicide containing 2,4-D or dicamba.",
                "prevention": "Maintain a dense, healthy lawn by proper watering, mowing, and fertilizing."
            },
            "Crabgrass": {
                "organic": "Pull young plants by hand before they seed. Apply corn gluten meal as a pre-emergent control.",
                "chemical": "Apply pre-emergent herbicides in early spring before soil temperatures reach 55°F.",
                "prevention": "Mow lawn at a higher height to shade soil and prevent crabgrass seed germination."
            },
            "Thistle": {
                "organic": "Dig out the entire root system. Repeatedly cutting the plant to deplete root reserves.",
                "chemical": "Apply broadleaf herbicide containing clopyralid or 2,4-D.",
                "prevention": "Maintain thick turf and proper soil fertility to prevent establishment."
            },
            "Chickweed": {
                "organic": "Hand-pull plants before they seed. Smother with mulch in garden areas.",
                "chemical": "Apply post-emergent herbicides containing dicamba or MCPP.",
                "prevention": "Avoid overwatering and improve soil drainage."
            },
            "Bindweed": {
                "organic": "Persistent removal of all above-ground growth to starve the roots. Cover with mulch or landscape fabric.",
                "chemical": "Apply herbicides containing dicamba or 2,4-D repeatedly.",
                "prevention": "Maintain thick turf and use landscape fabric in garden areas."
            },
            "Nutsedge": {
                "organic": "Hand-pull plants, taking care to remove all tubers. Cover area with thick mulch.",
                "chemical": "Apply herbicides specifically formulated for nutsedge control containing halosulfuron.",
                "prevention": "Avoid overwatering and improve soil drainage."
            },
            "Purslane": {
                "organic": "Hand-pull entire plants before they seed. Apply thick mulch in garden areas.",
                "chemical": "Apply pre-emergent herbicides in spring or post-emergent herbicides when plants are young.",
                "prevention": "Apply mulch to garden beds and maintain thick turf in lawn areas."
            },
            "Pigweed": {
                "organic": "Hand-pull plants before they seed. Use mulch to suppress growth.",
                "chemical": "Apply post-emergent herbicides containing glyphosate or 2,4-D.",
                "prevention": "Remove plants before they produce seeds. Maintain thick ground cover."
            },
            "Wild Mustard": {
                "organic": "Hand-pull plants before they flower and seed. Use vinegar-based herbicides on young plants.",
                "chemical": "Apply broadleaf herbicides containing 2,4-D or MCPA.",
                "prevention": "Remove plants before they seed and practice crop rotation in garden areas."
            },
            "Foxtail": {
                "organic": "Pull young plants by hand. Apply corn gluten meal as pre-emergent control.",
                "chemical": "Apply pre-emergent herbicides in spring before germination.",
                "prevention": "Mow at proper height and maintain thick, healthy turf."
            }
        }
        
        # Return remedy for the detected weed type, or a generic remedy if not found
        if weed_type in remedies:
            return remedies[weed_type]
        else:
            return {
                "organic": "Hand-pull weeds ensuring removal of the entire root system.",
                "chemical": "Apply a broad-spectrum herbicide according to manufacturer instructions.",
                "prevention": "Maintain healthy soil and plants to prevent weed establishment."
            }
    
    def _save_annotated_image(self, image_path, results):
        """
        Save the annotated image with detection results.
        
        Args:
            image_path (str): Path to the original image.
            results: YOLOv8 detection results.
            
        Returns:
            str: Path to the saved annotated image.
        """
        # Get the filename without extension
        filename = os.path.basename(image_path)
        name, ext = os.path.splitext(filename)
        
        # Path for the annotated image
        annotated_path = os.path.join('app/static/uploads', f"{name}_annotated{ext}")
        
        # Get the annotated image from results and save it
        for r in results:
            im_array = r.plot()  # Plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.save(annotated_path)  # Save image
        
        return annotated_path 