import os
import re
import pandas as pd
from datetime import datetime

def analyze_document(document_path):
    """
    Analyze the uploaded document for weed-related information.
    
    Args:
        document_path (str): Path to the uploaded document.
        
    Returns:
        dict: Analysis results and extracted information.
    """
    try:
        # Get file extension
        _, ext = os.path.splitext(document_path)
        ext = ext.lower()
        
        # Extract text based on file type
        if ext in ['.pdf']:
            # In a real application, this would use a PDF parser like PyPDF2 or pdfplumber
            # For demonstration, we'll simulate extracted text
            extracted_text = simulate_pdf_extraction()
            
        elif ext in ['.doc', '.docx']:
            # In a real application, this would use python-docx
            # For demonstration, we'll simulate extracted text
            extracted_text = simulate_docx_extraction()
            
        else:
            return {
                'status': 'error',
                'message': f'Unsupported file format: {ext}. Please upload PDF, DOC, or DOCX files.'
            }
        
        # Process the extracted text
        # In a real application, this would use NLP techniques
        analysis_results = process_document_text(extracted_text)
        
        return {
            'status': 'success',
            'document_path': document_path,
            'analysis': analysis_results
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error analyzing document: {str(e)}'
        }

def process_document_text(text):
    """
    Process the extracted text to identify weed-related information.
    
    Args:
        text (str): Extracted text from the document.
        
    Returns:
        dict: Processed information about weeds, growth stages, and remedies.
    """
    # In a real application, this would use NLP and ML techniques
    # For demonstration, we'll use simple pattern matching
    
    # Common weed types to look for
    weed_types = [
        "Dandelion", "Crabgrass", "Thistle", "Chickweed", "Bindweed",
        "Nutsedge", "Purslane", "Pigweed", "Wild Mustard", "Foxtail"
    ]
    
    # Growth stages to look for
    growth_stages = ["Seedling", "Vegetative", "Flowering", "Mature"]
    
    # Treatment methods to look for
    treatments = [
        "herbicide", "manual removal", "tilling", "mulching", "soil amendment",
        "organic control", "chemical control", "preventive measure"
    ]
    
    # Count occurrences
    weed_mentions = {}
    for weed in weed_types:
        count = len(re.findall(r'\b' + re.escape(weed) + r'\b', text, re.IGNORECASE))
        if count > 0:
            weed_mentions[weed] = count
    
    stage_mentions = {}
    for stage in growth_stages:
        count = len(re.findall(r'\b' + re.escape(stage) + r'\b', text, re.IGNORECASE))
        if count > 0:
            stage_mentions[stage] = count
    
    treatment_mentions = {}
    for treatment in treatments:
        count = len(re.findall(r'\b' + re.escape(treatment) + r'\b', text, re.IGNORECASE))
        if count > 0:
            treatment_mentions[treatment] = count
    
    # Extract potential field/location information
    # In a real application, this would use named entity recognition
    location_pattern = r'\b(field|garden|plot|area|section|zone)\s+([A-Za-z0-9-]+)\b'
    locations = re.findall(location_pattern, text, re.IGNORECASE)
    
    # Extract potential dates
    date_pattern = r'\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{1,2}-\d{1,2}-\d{2,4}\b'
    dates = re.findall(date_pattern, text)
    
    # Create summary of findings
    primary_weeds = sorted(weed_mentions.items(), key=lambda x: x[1], reverse=True)
    primary_stages = sorted(stage_mentions.items(), key=lambda x: x[1], reverse=True)
    primary_treatments = sorted(treatment_mentions.items(), key=lambda x: x[1], reverse=True)
    
    # Create simple sentences based on findings
    conclusions = []
    
    if primary_weeds:
        weed_text = f"The document primarily discusses {', '.join([w[0] for w in primary_weeds[:3]])}."
        conclusions.append(weed_text)
    
    if primary_stages:
        stage_text = f"Growth stages mentioned include {', '.join([s[0] for s in primary_stages])}."
        conclusions.append(stage_text)
    
    if primary_treatments:
        treatment_text = f"Recommended treatments include {', '.join([t[0] for t in primary_treatments[:3]])}."
        conclusions.append(treatment_text)
    
    if not conclusions:
        conclusions.append("No specific weed information was detected in the document.")
    
    return {
        'weed_mentions': weed_mentions,
        'growth_stages': stage_mentions,
        'treatments': treatment_mentions,
        'locations': locations,
        'dates': dates,
        'summary': ' '.join(conclusions)
    }

def simulate_pdf_extraction():
    """Simulate extracting text from a PDF for demonstration purposes."""
    return """
    Weed Management Report - Spring 2023
    
    Field Assessment:
    The field A12 was surveyed on 05/15/2023 and found to have moderate infestation of Dandelion and Crabgrass, 
    particularly in the southern section. Most weeds were in the Vegetative growth stage, with some early Flowering 
    specimens observed.
    
    Recommendations:
    For Dandelion control, manual removal is recommended for smaller areas, ensuring complete extraction of the taproot. 
    For larger areas, a selective herbicide application containing 2,4-D would be effective. Apply when plants are in the 
    active growing stage but before flowering.
    
    Crabgrass is best managed with pre-emergent herbicide application in early spring. For established plants, post-emergent 
    herbicides containing quinclorac can be effective. Maintain proper mowing height (3-4 inches) to shade soil and reduce 
    crabgrass germination.
    
    Prevention strategies:
    1. Maintain healthy soil with proper pH (6.0-7.0) and adequate fertility
    2. Use mulching in garden areas to suppress weed growth
    3. Implement proper irrigation practices to favor desirable plants over weeds
    4. Consider cover cropping in field section B3 during the fall/winter season
    
    Follow-up inspection scheduled for 06/20/2023.
    """

def simulate_docx_extraction():
    """Simulate extracting text from a DOCX for demonstration purposes."""
    return """
    Weed Management Plan - Garden Zone C
    
    Survey Date: 03/10/2023
    
    Identified Species:
    - Thistle (Mature stage): Dense patches in northwest corner
    - Bindweed (Vegetative stage): Spreading along fence line
    - Nutsedge (Seedling stage): Emerging in recently irrigated areas
    
    Treatment Recommendations:
    
    For Thistle:
    The mature Thistle requires immediate attention. Organic control methods include digging out the entire root system and 
    applying mulch to prevent regrowth. For chemical control, a spot treatment with clopyralid-based herbicide will be effective.
    
    For Bindweed:
    This persistent perennial requires ongoing management. Begin with manual removal of all visible parts, followed by mulching 
    with landscape fabric. Chemical control using dicamba may be necessary for severe infestations.
    
    For Nutsedge:
    Early intervention is critical. Improve drainage in affected areas, as Nutsedge thrives in wet conditions. Remove young plants 
    by hand, ensuring to extract the tubers. Herbicides containing halosulfuron can be applied for larger infestations.
    
    Soil Amendment Plan:
    - Add compost to improve soil structure
    - Adjust pH to 6.5 using lime application
    - Implement proper irrigation scheduling to prevent overwatering
    
    Follow-up treatments should be conducted every 2-3 weeks until weed pressure is significantly reduced.
    """ 