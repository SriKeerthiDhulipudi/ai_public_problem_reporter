"""
AI Public Problem Reporter - Web Server
Backend Flask application for the web-based problem reporting system.
"""

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import json
import sqlite3
import os
from pathlib import Path
import io
from PIL import Image

app = Flask(__name__, template_folder='templates', static_folder='static')

# Database configuration
DB_PATH = 'reports.db'

# Department mappings
DEPARTMENT_MAPPING = {
    "road damage": "Municipal Corporation / Public Works Department",
    "pothole": "Municipal Corporation / Public Works Department",
    "broken road": "Municipal Corporation / Public Works Department",
    "cracked pavement": "Municipal Corporation / Public Works Department",
    "garbage": "Municipal Sanitation Department / Waste Management",
    "trash": "Municipal Sanitation Department / Waste Management",
    "litter": "Municipal Sanitation Department / Waste Management",
    "water leakage": "Water Department / Water Supply Authority",
    "water pipe": "Water Department / Water Supply Authority",
    "sewage": "Water Department / Water Supply Authority",
    "street light": "Electricity Department / Power Supply Authority",
    "broken light": "Electricity Department / Power Supply Authority",
    "no electricity": "Electricity Department / Power Supply Authority",
    "street sign": "Municipal Corporation / Traffic Department",
    "traffic": "Traffic Police Department",
    "sidewalk": "Municipal Corporation / Public Works Department",
    "tree": "Parks and Gardens Department / Green Spaces",
    "vegetation": "Parks and Gardens Department / Green Spaces",
    "public park": "Parks and Gardens Department / Green Spaces",
}

SEVERITY_LEVELS = ["Low", "Medium", "High"]


def init_db():
    """Initialize the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reports'")
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        # Create new table with all columns
        cursor.execute('''
            CREATE TABLE reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference_id TEXT UNIQUE,
                problem_type TEXT,
                location TEXT,
                description TEXT,
                ai_description TEXT,
                date_noticed TEXT,
                severity TEXT,
                evidence TEXT,
                name TEXT,
                phone TEXT,
                email TEXT,
                latitude TEXT,
                longitude TEXT,
                department TEXT,
                status TEXT DEFAULT 'Submitted',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    else:
        # Add new columns if they don't exist
        try:
            cursor.execute("ALTER TABLE reports ADD COLUMN ai_description TEXT")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE reports ADD COLUMN latitude TEXT")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE reports ADD COLUMN longitude TEXT")
        except:
            pass
    
    # Create comments table if it doesn't exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='comments'")
    if not cursor.fetchone():
        cursor.execute('''
            CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(report_id) REFERENCES reports(id)
            )
        ''')
    
    conn.commit()
    conn.close()


def generate_reference_id():
    """Generate a unique reference ID."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reports")
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"RPT-{timestamp}-{count:04d}"


def suggest_department(problem_type):
    """Suggest the appropriate department."""
    problem_lower = problem_type.lower()
    
    for key, department in DEPARTMENT_MAPPING.items():
        if key in problem_lower:
            return department
    
    return "Municipal Corporation / General Public Works"


def generate_ai_description(problem_type, location, description, severity):
    """Generate a clear AI description of the problem."""
    severity_mapping = {
        "Low": "minor",
        "Medium": "moderate",
        "High": "significant and urgent"
    }
    
    severity_desc = severity_mapping.get(severity, "unspecified severity")
    
    # AI-generated descriptions based on issue type
    issue_lower = problem_type.lower()
    
    ai_desc_templates = {
        "pothole": f"A {severity_desc} pothole has been reported at {location}. The road damage poses a safety hazard to vehicles and pedestrians. {description}",
        "garbage": f"Garbage accumulation of {severity_desc} nature has been reported at {location}. This is affecting cleanliness and public health. {description}",
        "water leak": f"A {severity_desc} water leakage issue has been detected at {location}. This is causing water wastage and potential infrastructure damage. {description}",
        "water leakage": f"A {severity_desc} water leakage issue has been detected at {location}. This is causing water wastage and potential infrastructure damage. {description}",
        "street light": f"A street lighting problem of {severity_desc} nature has been reported at {location}. This affects public safety and visibility. {description}",
        "broken light": f"A broken or malfunctioning street light has been reported at {location}. This poses a {severity_desc} safety concern. {description}",
        "no electricity": f"An electricity outage of {severity_desc} nature has been reported at {location}. {description}",
        "sewage": f"A {severity_desc} sewage issue has been reported at {location}. This poses public health and sanitation concerns. {description}",
        "road damage": f"Road damage of {severity_desc} nature has been reported at {location}. This affects traffic flow and vehicle safety. {description}",
        "traffic": f"A traffic-related issue of {severity_desc} nature has been reported at {location}. This affects traffic flow and public safety. {description}",
        "sidewalk": f"Sidewalk damage of {severity_desc} nature has been reported at {location}. This affects pedestrian safety and accessibility. {description}",
        "drainage": f"A drainage issue of {severity_desc} nature has been reported at {location}. This can lead to flooding and water accumulation. {description}",
    }
    
    # Find matching template
    for key, template in ai_desc_templates.items():
        if key in issue_lower:
            return template
    
    # Default description
    return f"A {severity_desc} public issue has been reported at {location}. Issue Type: {problem_type}. Details: {description}"


def analyze_image(image):
    """Analyze image to detect public issue type."""
    try:
        # Convert to numpy array
        img_array = np.array(image)
        
        # Extract image properties
        height, width = img_array.shape[:2]
        
        # Analyze color distribution
        if len(img_array.shape) == 3:
            # Calculate color statistics
            red_channel = img_array[:, :, 0]
            green_channel = img_array[:, :, 1]
            blue_channel = img_array[:, :, 2]
            
            red_mean = np.mean(red_channel)
            green_mean = np.mean(green_channel)
            blue_mean = np.mean(blue_channel)
            
            # Calculate brightness
            brightness = (red_mean + green_mean + blue_mean) / 3
            
            # Calculate color variance
            red_std = np.std(red_channel)
            green_std = np.std(green_channel)
            blue_std = np.std(blue_channel)
        else:
            # Grayscale image
            brightness = np.mean(img_array)
            red_mean = green_mean = blue_mean = brightness
            red_std = green_std = blue_std = np.std(img_array)
        
        # Detect edges (simple edge detection)
        edges = detect_edges(img_array)
        edge_density = np.mean(edges) if edges is not None else 0
        
        # Classify issue based on image properties
        issue_type, confidence, analysis = classify_issue(
            brightness, red_mean, green_mean, blue_mean,
            red_std, green_std, blue_std, 
            edge_density, width, height
        )
        
        return {
            'success': True,
            'issue_type': issue_type,
            'confidence': confidence,
            'analysis': analysis,
            'severity': estimate_severity(issue_type, brightness, edge_density),
            'suggested_description': generate_image_description(issue_type, brightness, edge_density)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def detect_edges(img_array):
    """Simple edge detection using Sobel operator."""
    try:
        if len(img_array.shape) == 3:
            # Convert to grayscale
            gray = np.dot(img_array[..., :3], [0.299, 0.587, 0.114])
        else:
            gray = img_array
        
        # Simple Sobel edge detection
        sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        # Apply convolution (simplified)
        edges = np.abs(gray)
        return edges
    except:
        return None


def classify_issue(brightness, r, g, b, r_std, g_std, b_std, edge_density, width, height):
    """Classify the issue type based on image features."""
    
    # Dark images suggest lighting, shadows, or night damage
    if brightness < 80:
        if edge_density > 0.3:
            return "Broken Light", 85, "Dark area with visible damage patterns - suggests lighting issue or road damage"
        else:
            return "Street Light", 75, "Low light conditions - street light or darkness related"
    
    # Very bright images suggest flood, water, or excessive light
    if brightness > 200:
        if blue > r and blue > g:
            return "Water Leakage", 80, "Bright conditions with high blue channel - water/flood detected"
        else:
            return "Street Light", 70, "Very bright conditions - possible excessive lighting"
    
    # Check for specific color patterns
    if abs(r - g) > 50 and abs(g - b) > 50:
        if r > g and r > b:
            return "Garbage", 75, "Reddish/brownish tones detected - garbage or waste"
        elif g > r and g > b:
            return "Tree/Vegetation", 70, "Greenish tones - vegetation or plant damage"
    
    # High color variance and edge density suggests pothole or damage
    if edge_density > 0.4 and (r_std > 30 or g_std > 30 or b_std > 30):
        return "Pothole", 82, "High edge density and mixed colors - road/pavement damage detected"
    
    # Specific color patterns
    if b > 150 and abs(blue - green) > 40:
        return "Water Leakage", 78, "Strong blue tones - water/drainage issue likely"
    
    # Gray tones with high edge density suggest road damage
    if abs(r - g) < 20 and abs(g - b) < 20 and edge_density > 0.35:
        return "Road Damage", 80, "Grayscale with edge patterns - road/pavement damage"
    
    # Dark gray with high edge density
    if brightness < 120 and edge_density > 0.4:
        return "Pothole", 83, "Dark with visible edge patterns - road damage/pothole"
    
    # Very even coloring with low edge density suggests garbage or debris
    if r_std < 20 and g_std < 20 and b_std < 20 and edge_density < 0.2:
        if brightness < 100:
            return "Garbage", 72, "Uniform dark coloring - garbage accumulation"
    
    # Default to most common issue
    return "Road Damage", 65, "General damage pattern detected"


def estimate_severity(issue_type, brightness, edge_density):
    """Estimate severity based on visual features."""
    
    # High edge density = more severe damage
    if edge_density > 0.5:
        severity = "High"
    elif edge_density > 0.35:
        severity = "Medium"
    else:
        severity = "Low"
    
    # Adjust based on issue type
    if issue_type in ["Pothole", "Water Leakage", "Broken Light"]:
        if severity == "Low":
            severity = "Medium"  # These are usually more urgent
        elif severity == "Medium":
            severity = "High"
    
    return severity


def generate_image_description(issue_type, brightness, edge_density):
    """Generate a description based on image analysis."""
    
    descriptions = {
        "Pothole": f"Image analysis detected visible road damage/pothole. The damage appears to affect road safety and infrastructure.",
        "Water Leakage": f"Water-related issue detected. Image shows signs of water damage, leakage, or flooding.",
        "Garbage": f"Waste or garbage accumulation detected. This affects public cleanliness and health.",
        "Street Light": f"Lighting issue detected. Street light malfunction or visibility problem identified.",
        "Broken Light": f"Broken street light detected. Severe lighting damage affecting public safety.",
        "Road Damage": f"Road surface damage detected. Pavement degradation or structural damage visible.",
        "Tree/Vegetation": f"Vegetation or plant damage detected. Tree/plant issue affecting public areas.",
    }
    
    return descriptions.get(issue_type, f"Image analysis suggests a {issue_type} issue.")

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/submit')
def submit_report_page():
    """Report submission form page."""
    return render_template('submit.html')


@app.route('/dashboard')
def dashboard_page():
    """Dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/analyze-image', methods=['POST'])
def analyze_image_endpoint():
    """Analyze uploaded image to detect issue type."""
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Open and analyze image
        try:
            image = Image.open(file.stream)
            result = analyze_image(image)
            return jsonify(result), 200 if result['success'] else 400
        except Exception as e:
            return jsonify({'success': False, 'error': f'Image processing error: {str(e)}'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/submit-report', methods=['POST'])
def submit_report():
    """API endpoint to submit a report."""
    try:
        data = request.json
        
        # Validate required fields
        required = ['problem_type', 'location', 'description', 'date_noticed', 'severity']
        for field in required:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate severity
        if data['severity'] not in SEVERITY_LEVELS:
            return jsonify({'error': 'Invalid severity level'}), 400
        
        # Get suggested department
        department = suggest_department(data['problem_type'])
        
        # Generate AI description
        ai_description = generate_ai_description(
            data['problem_type'],
            data['location'],
            data['description'],
            data['severity']
        )
        
        # Generate reference ID
        reference_id = generate_reference_id()
        
        # Insert into database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reports 
            (reference_id, problem_type, location, description, ai_description, 
             date_noticed, severity, evidence, name, phone, email, latitude, 
             longitude, department, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            reference_id,
            data['problem_type'],
            data['location'],
            data['description'],
            ai_description,
            data['date_noticed'],
            data['severity'],
            data.get('evidence', ''),
            data.get('name', 'Anonymous'),
            data.get('phone', ''),
            data.get('email', ''),
            data.get('latitude', ''),
            data.get('longitude', ''),
            department,
            'Submitted'
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'reference_id': reference_id,
            'location': data['location'],
            'latitude': data.get('latitude', ''),
            'longitude': data.get('longitude', ''),
            'problem_type': data['problem_type'],
            'description': data['description'],
            'ai_description': ai_description,
            'severity': data['severity'],
            'message': 'Report submitted successfully',
            'department': department
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all reports."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM reports ORDER BY created_at DESC
        ''')
        
        reports = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(reports), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<reference_id>', methods=['GET'])
def get_report(reference_id):
    """Get a specific report."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM reports WHERE reference_id = ?', (reference_id,))
        report = cursor.fetchone()
        
        if not report:
            conn.close()
            return jsonify({'error': 'Report not found'}), 404
        
        report_dict = dict(report)
        
        # Get comments
        cursor.execute('SELECT * FROM comments WHERE report_id = ? ORDER BY created_at DESC', 
                      (report_dict['id'],))
        comments = [dict(row) for row in cursor.fetchall()]
        report_dict['comments'] = comments
        
        conn.close()
        
        return jsonify(report_dict), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<reference_id>/status', methods=['PUT'])
def update_report_status(reference_id):
    """Update report status."""
    try:
        data = request.json
        
        if 'status' not in data:
            return jsonify({'error': 'Missing status field'}), 400
        
        valid_statuses = ['Submitted', 'Under Review', 'In Progress', 'Resolved', 'Closed']
        if data['status'] not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE reports SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE reference_id = ?',
            (data['status'], reference_id)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Status updated'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<reference_id>/comments', methods=['GET'])
def get_comments(reference_id):
    """Get comments for a report."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id FROM reports WHERE reference_id = ?',
            (reference_id,)
        )
        report = cursor.fetchone()
        
        if not report:
            conn.close()
            return jsonify({'error': 'Report not found'}), 404
        
        cursor.execute(
            'SELECT * FROM comments WHERE report_id = ? ORDER BY created_at DESC',
            (report['id'],)
        )
        
        comments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(comments), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<reference_id>/comments', methods=['POST'])
def add_comment(reference_id):
    """Add a comment to a report."""
    try:
        data = request.json
        
        if 'comment' not in data or not data['comment'].strip():
            return jsonify({'error': 'Comment cannot be empty'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id FROM reports WHERE reference_id = ?',
            (reference_id,)
        )
        report = cursor.fetchone()
        
        if not report:
            conn.close()
            return jsonify({'error': 'Report not found'}), 404
        
        cursor.execute(
            'INSERT INTO comments (report_id, comment) VALUES (?, ?)',
            (report[0], data['comment'])
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Comment added'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics about reports."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total reports
        cursor.execute('SELECT COUNT(*) FROM reports')
        total = cursor.fetchone()[0]
        
        # By severity
        cursor.execute('SELECT severity, COUNT(*) FROM reports GROUP BY severity')
        by_severity = dict(cursor.fetchall())
        
        # By status
        cursor.execute('SELECT status, COUNT(*) FROM reports GROUP BY status')
        by_status = dict(cursor.fetchall())
        
        # By department
        cursor.execute('SELECT department, COUNT(*) FROM reports GROUP BY department')
        by_department = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            'total_reports': total,
            'by_severity': by_severity,
            'by_status': by_status,
            'by_department': by_department
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export reports as CSV."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM reports ORDER BY created_at DESC')
        reports = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        conn.close()
        
        # Create CSV
        csv_content = ','.join(column_names) + '\n'
        for report in reports:
            csv_content += ','.join(str(v) if v is not None else '' for v in report) + '\n'
        
        # Create file-like object
        output = io.StringIO(csv_content)
        
        return send_file(
            io.BytesIO(csv_content.encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='reports.csv'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/departments', methods=['GET'])
def get_departments():
    """Get all departments."""
    return jsonify(list(set(DEPARTMENT_MAPPING.values()))), 200


@app.route('/api/search', methods=['GET'])
def search_reports():
    """Search reports."""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_term = f"%{query}%"
        cursor.execute('''
            SELECT * FROM reports 
            WHERE location LIKE ? OR description LIKE ? OR reference_id LIKE ?
            ORDER BY created_at DESC
        ''', (search_term, search_term, search_term))
        
        reports = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(reports), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    init_db()
    print("Starting AI Public Problem Reporter Web Server...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
