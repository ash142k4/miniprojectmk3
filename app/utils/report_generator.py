import os
import json
from datetime import datetime

def generate_report(analysis_results):
    """
    Generate a detailed report based on document analysis results.
    
    Args:
        analysis_results (dict): Results from document analysis.
        
    Returns:
        str: Path to the generated report file.
    """
    try:
        # Create reports directory if it doesn't exist
        reports_dir = 'app/static/reports'
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate a unique filename for the report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"weed_report_{timestamp}.html"
        report_path = os.path.join(reports_dir, report_filename)
        
        # Extract analysis data
        if 'analysis' in analysis_results:
            analysis = analysis_results['analysis']
        else:
            analysis = analysis_results  # If analysis is directly passed
            
        # Generate HTML report
        html_content = _generate_html_report(analysis, timestamp)
        
        # Write the HTML report to file
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        return report_path
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return None

def _generate_html_report(analysis, timestamp):
    """
    Generate HTML content for the weed analysis report.
    
    Args:
        analysis (dict): Analysis data.
        timestamp (str): Timestamp for the report.
        
    Returns:
        str: HTML content for the report.
    """
    # Format the date for display
    date_str = datetime.now().strftime('%B %d, %Y')
    
    # Extract data from analysis
    weed_mentions = analysis.get('weed_mentions', {})
    growth_stages = analysis.get('growth_stages', {})
    treatments = analysis.get('treatments', {})
    locations = analysis.get('locations', [])
    dates = analysis.get('dates', [])
    summary = analysis.get('summary', 'No summary available.')
    
    # Create the HTML content
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weed Analysis Report | {date_str}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .report-container {{
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 30px;
                margin-bottom: 20px;
            }}
            .header {{
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 15px;
                margin-bottom: 25px;
            }}
            h1 {{
                color: #2E7D32;
                margin: 0;
            }}
            h2 {{
                color: #388E3C;
                margin-top: 30px;
                margin-bottom: 15px;
                padding-bottom: 5px;
                border-bottom: 1px solid #ddd;
            }}
            .date {{
                color: #666;
                font-style: italic;
            }}
            .summary {{
                background-color: #F1F8E9;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #8BC34A;
                margin: 20px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .chart-section {{
                margin: 30px 0;
            }}
            .chart-container {{
                height: 250px;
                margin: 20px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
            }}
            .recommendations {{
                background-color: #E8F5E9;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 40px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="report-container">
            <div class="header">
                <h1>Weed Analysis Report</h1>
                <p class="date">Generated on {date_str}</p>
            </div>
            
            <div class="summary">
                <h2>Executive Summary</h2>
                <p>{summary}</p>
            </div>
            
            <h2>Detected Weed Species</h2>
    """
    
    if weed_mentions:
        html += """
            <table>
                <thead>
                    <tr>
                        <th>Weed Type</th>
                        <th>Frequency</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for weed, count in sorted(weed_mentions.items(), key=lambda x: x[1], reverse=True):
            html += f"""
                    <tr>
                        <td>{weed}</td>
                        <td>{count}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        """
    else:
        html += "<p>No specific weed species detected in the document.</p>"
    
    html += """
        <h2>Growth Stages</h2>
    """
    
    if growth_stages:
        html += """
            <table>
                <thead>
                    <tr>
                        <th>Growth Stage</th>
                        <th>Frequency</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for stage, count in sorted(growth_stages.items(), key=lambda x: x[1], reverse=True):
            html += f"""
                    <tr>
                        <td>{stage}</td>
                        <td>{count}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        """
    else:
        html += "<p>No growth stage information detected in the document.</p>"
    
    html += """
        <h2>Treatment Methods</h2>
    """
    
    if treatments:
        html += """
            <table>
                <thead>
                    <tr>
                        <th>Treatment Method</th>
                        <th>Frequency</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for treatment, count in sorted(treatments.items(), key=lambda x: x[1], reverse=True):
            html += f"""
                    <tr>
                        <td>{treatment}</td>
                        <td>{count}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        """
    else:
        html += "<p>No treatment methods detected in the document.</p>"
    
    html += """
        <h2>Locations and Dates</h2>
    """
    
    if locations:
        html += """
            <table>
                <thead>
                    <tr>
                        <th>Location Type</th>
                        <th>Identifier</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for loc_type, identifier in locations:
            html += f"""
                    <tr>
                        <td>{loc_type.capitalize()}</td>
                        <td>{identifier}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        """
    else:
        html += "<p>No specific location information detected in the document.</p>"
    
    if dates:
        html += """
            <h3>Relevant Dates</h3>
            <ul>
        """
        
        for date in dates:
            html += f"<li>{date}</li>"
        
        html += """
            </ul>
        """
    
    # Add recommendations section based on detected weeds
    html += """
        <div class="recommendations">
            <h2>Recommendations</h2>
    """
    
    if weed_mentions:
        primary_weeds = sorted(weed_mentions.items(), key=lambda x: x[1], reverse=True)[:3]
        html += "<ul>"
        
        for weed, _ in primary_weeds:
            if weed == "Dandelion":
                html += """
                    <li><strong>Dandelion Control:</strong> Use a weeding tool to remove the entire root. For larger areas, 
                    consider selective herbicides containing 2,4-D applied when plants are actively growing.</li>
                """
            elif weed == "Crabgrass":
                html += """
                    <li><strong>Crabgrass Management:</strong> Apply pre-emergent herbicides in early spring before soil 
                    temperatures reach 55°F. For established plants, use post-emergent herbicides containing quinclorac.</li>
                """
            elif weed == "Thistle":
                html += """
                    <li><strong>Thistle Removal:</strong> Dig out the entire root system for small areas. For larger infestations, 
                    use broadleaf herbicides containing clopyralid or 2,4-D when plants are actively growing.</li>
                """
            elif weed == "Chickweed":
                html += """
                    <li><strong>Chickweed Control:</strong> Hand-pull plants before they seed and apply mulch in garden areas. 
                    Consider post-emergent herbicides containing dicamba for larger areas.</li>
                """
            elif weed == "Bindweed":
                html += """
                    <li><strong>Bindweed Management:</strong> Persistent removal of all above-ground growth to starve the roots. 
                    Cover with landscape fabric in garden areas and apply herbicides containing dicamba for severe infestations.</li>
                """
            elif weed == "Nutsedge":
                html += """
                    <li><strong>Nutsedge Control:</strong> Improve drainage in affected areas. Hand-pull plants ensuring removal 
                    of tubers. For severe cases, use herbicides containing halosulfuron.</li>
                """
            else:
                html += f"""
                    <li><strong>{weed} Management:</strong> Implement integrated weed management practices including proper 
                    identification, manual removal, and appropriate herbicide selection based on the growth stage.</li>
                """
        
        html += "</ul>"
    else:
        html += """
            <p>No specific weed species were identified in the document. For general weed management:</p>
            <ul>
                <li>Maintain healthy soil with proper pH and adequate fertility</li>
                <li>Use mulch in garden areas to suppress weed growth</li>
                <li>Implement proper irrigation practices to favor desirable plants over weeds</li>
                <li>Consider using pre-emergent herbicides in early spring for annual weed control</li>
            </ul>
        """
    
    html += """
        </div>
        
        <div class="footer">
            <p>This report was generated automatically by the Weed Detection Application.</p>
            <p>Report ID: WD-{timestamp}</p>
        </div>
    </div>
    </body>
    </html>
    """.format(timestamp=timestamp)
    
    return html 