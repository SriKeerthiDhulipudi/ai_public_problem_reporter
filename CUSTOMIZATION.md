# Configuration and Customization Guide

This guide explains how to customize the AI Public Problem Reporter for your region or organization.

## Quick Start Customization

### Adding New Issue Types

Edit the `DEPARTMENT_MAPPING` dictionary in `problem_reporter.py`:

```python
DEPARTMENT_MAPPING = {
    # Road Issues
    "road damage": "Municipal Corporation / Public Works Department",
    "pothole": "Municipal Corporation / Public Works Department",

    # YOUR CUSTOM CATEGORIES HERE:
    "street furniture": "Your Department Name",
    "public toilet": "Sanitation Department",
    "bus shelter": "Transport Department",
}
```

**How it works:**

- Key: Issue type (lowercase)
- Value: Recommended department

## Regional Customization

### For India

Default configuration includes Indian departments:

- Municipal Corporation (Nagar Palika)
- Electricity Department (DISCOM)
- Water Supply Authority (Jal Board)
- Municipal Sanitation (Swachh Bharat)

### For Other Countries

Replace department names with your regional authorities:

```python
# Example: Australia
DEPARTMENT_MAPPING = {
    "pothole": "Local Council / Roads Department",
    "garbage": "Local Council / Waste Services",
    "street light": "Local Council / Infrastructure",
}

# Example: USA
DEPARTMENT_MAPPING = {
    "pothole": "Public Works Department",
    "garbage": "Sanitation Department",
    "street light": "Utilities Department",
}
```

## Advanced Customization

### Modify Severity Levels

Change how severity is defined:

```python
SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]
```

Then update the severity descriptions:

```python
def get_severity(self) -> str:
    print("\nSeverity levels:")
    print("  • Low: Minor issue")
    print("  • Medium: Moderate issue")
    print("  • High: Urgent issue")
    print("  • Critical: Immediate danger")
```

### Change Report Format

Modify the `generate_report()` method to customize the output:

```python
def generate_report(self, data: dict) -> str:
    """Generate custom formatted report."""
    report = []
    report.append("CITIZEN COMPLAINT FORM")  # Custom title
    report.append(f"Category: {data['problem_type']}")  # Different labels
    # ... customize as needed
    return "\n".join(report)
```

### Add Report Sections

Add new fields by:

1. Create a new `get_*` method:

```python
def get_witnesses(self) -> str:
    """Collect witness information."""
    print("\nAny witnesses to the incident?")
    return input("Enter witness details (optional): ").strip() or "None"
```

2. Call it in the `run()` method:

```python
witnesses = self.get_witnesses()
```

3. Add to data dict:

```python
data = {
    # ... existing fields
    'witnesses': witnesses,
}
```

4. Include in report:

```python
report.append(f"Witnesses:        {data.get('witnesses', 'None')}")
```

## Department Mapping Examples

### Comprehensive Default Setup

```python
DEPARTMENT_MAPPING = {
    # Roads
    "road": "Municipal Corporation",
    "highway": "National Highway Authority",
    "footpath": "Municipal Corporation",

    # Utilities
    "electricity": "Power Supply Company",
    "water": "Water Supply Board",
    "gas": "Gas Supply Department",

    # Environment
    "pollution": "Environmental Department",
    "construction": "Building Control Authority",
    "noise": "Police / Environmental Board",

    # Emergency
    "fire": "Fire Department",
    "accident": "Police Department",
    "flood": "Disaster Management",
}
```

## Multi-language Support

Add language support to prompts:

```python
LANGUAGES = {
    'en': {
        'welcome': 'Welcome to Problem Reporter',
        'type': 'What is the problem type?',
    },
    'hi': {
        'welcome': 'समस्या रिपोर्टर में स्वागत है',
        'type': 'समस्या का प्रकार क्या है?',
    }
}

def get_language(self):
    """Choose language for interface."""
    print("Select language / भाषा चुनें:")
    print("1. English")
    print("2. हिंदी")
    # ... implement language selection
```

## Environment-Specific Settings

### For Organization Use

```python
ORGANIZATION_HEADER = "XYZ Municipal Corporation"
ORGANIZATION_EMAIL = "complaints@xyzmc.gov.in"
SUBMISSION_INSTRUCTIONS = """
Submit this report to:
- Email: complaints@xyzmc.gov.in
- Website: www.xyzmc.gov.in/complaints
- Mobile App: XYZ MC Citizen Portal
"""

def generate_report(self, data: dict) -> str:
    report = []
    report.append(f"OFFICIAL COMPLAINT - {ORGANIZATION_HEADER}")
    # ... rest of report
```

### For NGO Use

```python
ORGANIZATION_HEADER = "Community Action Group"
SUBMISSION_INSTRUCTIONS = """
This report will be:
1. Documented in our database
2. Shared with relevant authorities
3. Tracked for follow-up
4. Used for advocacy and analysis
"""
```

## Adding Photo/Evidence Storage

Enhance the application to handle media:

```python
def handle_evidence_media(self) -> str:
    """Store photo or video evidence."""
    photo_path = input("Photo file path (optional): ").strip()
    if photo_path and Path(photo_path).exists():
        # Copy to reports folder
        filename = Path(photo_path).name
        dest = self.report_dir / f"evidence_{filename}"
        # ... copy logic
        return str(dest)
    return "Not provided"
```

## Database Integration

Save reports to database instead of files:

```python
def save_to_database(self, data: dict):
    """Save report to database."""
    import sqlite3

    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports
        (problem_type, location, description, severity, contact)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['problem_type'], data['location'],
          data['description'], data['severity'], data['contact']['email']))
    conn.commit()
```

## Testing Your Customization

After making changes:

1. **Test the interface**:

   ```bash
   python problem_reporter.py
   ```

2. **Verify reports generate correctly**

3. **Check output formatting**

4. **Test all edge cases**:
   - Empty inputs
   - Very long descriptions
   - Special characters
   - Different severity levels

## Troubleshooting Customization

**Issue**: Department not mapping correctly

- **Solution**: Check spelling in DEPARTMENT_MAPPING
- Use lowercase keys: `"street light"` not `"Street Light"`

**Issue**: Report format is broken

- **Solution**: Ensure all f-strings have matching braces
- Check data dictionary has all required keys

**Issue**: New field doesn't appear

- **Solution**: Verify added to both data dict and report generation

## Deployment Customization

### For Local Use

Keep as-is, customize department names only.

### For Organization Distribution

- Add organization branding
- Pre-set department contact info
- Add organizational guidelines
- Include tracking codes

### For Government Portal

- Enable JSON export for database import
- Add reference number system
- Integrate with existing systems
- Support batch submissions

## Best Practices

✓ Always test changes before deployment
✓ Keep backups of original code
✓ Document all customizations
✓ Version your configurations
✓ Get feedback from potential users
✓ Ensure accessibility for all users

---

**Customize to fit your community's needs!**
