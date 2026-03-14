# AI Public Problem Reporter

A citizen-friendly application designed to help report public issues to local authorities with structured, professional reports.

## Features

✓ **Interactive Guided Interface** - Step-by-step collection of information
✓ **Automatic Department Mapping** - Suggests the right authority for each issue type  
✓ **Multiple Report Formats** - Generates both readable text and JSON reports
✓ **Professional Reports** - Creates formatted reports suitable for government submission
✓ **Report History** - Saves all reports locally for your records
✓ **User-Friendly** - No technical knowledge required

## Issue Types Supported

The application handles reports for:

- **Road Issues**: Potholes, damaged roads, cracked pavement
- **Sanitation**: Garbage, trash, litter
- **Water**: Leaks, sewage issues
- **Electricity**: Broken street lights, no power
- **Infrastructure**: Broken signs, damaged sidewalks
- **Parks**: Tree/vegetation issues

## Installation

1. **Ensure Python 3.7+ is installed**

2. **No external dependencies needed!** This application uses only Python standard library.

## Usage

### Run the Application

```bash
python problem_reporter.py
```

### Follow the Interactive Prompts

The application will ask for:

1. **Type of Problem** - What's the issue?
2. **Exact Location** - Where is it?
3. **Description** - Details about the problem
4. **Date Noticed** - When was it first spotted?
5. **Severity Level** - Low, Medium, or High
6. **Additional Evidence** - Photos, videos, or extra info (optional)
7. **Contact Details** - Name, phone, email (optional)

### Generated Report

After providing information, you'll see:

- A professionally formatted report
- Recommended government department
- Reports saved in `reports/` folder

## Output Files

Reports are saved in two formats:

### Text Report (`report_*.txt`)

A readable, printable report suitable for submission to authorities:

```
PUBLIC ISSUE REPORT
-------------------
Issue Type:        Road damage
Location:          Main Street, near City Center
Description:       Large pothole causing traffic hazard
Date Reported:     Today
Severity Level:    High
Additional Notes:  Pothole is about 2 feet wide

Recommended Department:
Municipal Corporation / Public Works Department
```

### JSON Report (`report_*.json`)

Structured data format for digital processing and databases.

## Example Usage Scenarios

### Scenario 1: Report a Pothole

```
Type: Road damage
Location: Main Street, Ward 5, near traffic light
Description: 2x1.5 ft pothole, water pooling inside
Severity: High
Department: Municipal Corporation
```

### Scenario 2: Report Garbage Accumulation

```
Type: Garbage
Location: Park Road, Bus Stand Area
Description: Trash overflow, covers entire sidewalk
Severity: High
Department: Municipal Sanitation Department
```

### Scenario 3: Report Broken Street Light

```
Type: Street light
Location: Elm Avenue, opposite school gate
Description: Light hasn't worked for 3 weeks
Severity: Medium
Department: Electricity Department
```

## Report Management

All reports are automatically saved to the `reports/` folder with timestamps:

- Easy to locate and retrieve
- Share via email with authorities
- Keep for your records
- Track multiple complaints

## Department Mappings

The system intelligently maps issues to departments:

| Issue Type           | Recommended Department               |
| -------------------- | ------------------------------------ |
| Pothole, Road damage | Municipal Corporation / Public Works |
| Garbage, Litter      | Municipal Sanitation Department      |
| Water leaks          | Water Department / Water Supply      |
| Street lights        | Electricity Department               |
| Signs, Sidewalk      | Municipal Corporation                |
| Parks, Trees         | Parks and Gardens Department         |

## Tips for Better Reports

1. **Be Specific**: Provide exact location details and street names
2. **Be Descriptive**: Explain the problem clearly and mention safety concerns
3. **Be Honest**: Report actual issues that need attention
4. **Provide Evidence**: Mention any photos or videos if available
5. **Follow Up**: Track if authorities take action within 7-10 days

## Next Steps After Reporting

1. Keep a copy of your report
2. Submit to the recommended department:
   - Email
   - Visit office in person
   - Through government portal
3. Get a reference number if submitting officially
4. Follow up if no action taken

## Troubleshooting

**Issue**: Application won't start

- **Solution**: Ensure Python 3.7+ is installed: `python --version`

**Issue**: Can't find reports

- **Solution**: Reports are in the `reports/` subfolder in the same directory

**Issue**: Text appears corrupted

- **Solution**: Ensure your terminal supports UTF-8 encoding

## Customization

You can modify the `DEPARTMENT_MAPPING` dictionary in the code to:

- Add new issue types
- Update department names for your region
- Add more specific locations

## Contributing

To improve this tool:

- Suggest new issue categories
- Report bugs
- Propose UI improvements
- Share successful report submissions

## License

This tool is designed for public use and citizen empowerment.

## Support

For issues or suggestions, document them using this very tool!

---

**Making Communities Better, One Report at a Time**
