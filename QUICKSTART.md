# Quick Start Guide

Get up and running with the AI Public Problem Reporter in 2 minutes!

## Installation (30 seconds)

1. **Check Python is installed**

   ```bash
   python --version
   ```

   Should show Python 3.7 or higher. If not installed, download from python.org

2. **No other setup needed!** No packages to install.

## Running the Application (60 seconds)

### On Windows:

```bash
python problem_reporter.py
```

### On Mac/Linux:

```bash
python3 problem_reporter.py
```

## First Time Usage

1. **Start the application** - Follow the command above
2. **Answer 7 simple questions** - Takes about 2-3 minutes
3. **Review your report** - Appears on screen
4. **Find your report** - Saved in `reports/` folder
5. **Submit to authorities** - Email or print the report

## What You'll Be Asked

| Step | Question                 | Example                              |
| ---- | ------------------------ | ------------------------------------ |
| 1    | Type of problem?         | "Pothole", "Garbage", "Street light" |
| 2    | Where is it?             | "Main Street, near hospital"         |
| 3    | Describe it              | "Large pothole, 2 feet wide"         |
| 4    | When noticed?            | "Today", "Yesterday", "03/14/2026"   |
| 5    | How serious?             | "Low", "Medium", or "High"           |
| 6    | More details? (optional) | Photos, videos, etc.                 |
| 7    | Your info? (optional)    | Name, phone, email                   |

## Example Session

```
AI PUBLIC PROBLEM REPORTER
==========================

STEP 1: What type of problem?
Enter the type of problem: pothole

STEP 2: Where is the problem?
Enter the exact location: Main Street, Ward 5

STEP 3: Describe the problem
Enter detailed description: Large pothole, about 2 feet wide

STEP 4: When was it noticed?
Enter when problem was noticed: Today

STEP 5: What is the severity?
Select severity (Low/Medium/High): High

STEP 6: Additional evidence (press Enter to skip)
Enter additional information: Causes vehicles to swerve

STEP 7: Your contact details (all optional)
Your name: Raj Kumar
Phone: 9876543210
Email: raj@email.com

[REPORT DISPLAYS HERE]

✓ Report saved successfully!
```

## Finding Your Reports

Reports are saved to the `reports/` folder:

- **Text format** (for printing): `report_pothole_20260314_102345.txt`
- **JSON format** (for processing): `report_pothole_20260314_102345.json`

## What to Do Next

### Option 1: Submit Via Email

1. Open the text report file
2. Copy content
3. Email to relevant department with subject line:
   ```
   Public Issue Report - [Issue Type] - [Your Area]
   ```

### Option 2: Submit In Person

1. Print the report
2. Visit the department office
3. Submit with reference copy

### Option 3: Government Portal

1. Find report file
2. Upload to municipal/government portal
3. Get reference number

### Option 4: Track for Follow-up

1. Keep report file
2. Note down issue location
3. Check back in 1 week
4. If resolved: great!
5. If not: file another report or escalate

## Common Issue Types & Departments

| Problem              | Department                    |
| -------------------- | ----------------------------- |
| Pothole, Road damage | Public Works / Municipal Corp |
| Garbage piling up    | Sanitation / Waste Management |
| Water leak           | Water Supply Department       |
| Street light off     | Electricity Department        |
| Broken sidewalk      | Public Works                  |
| Dead tree            | Parks & Gardens               |

**Don't know which department?**
The tool suggests the right one automatically!

## Tips for Better Reports

✅ **DO:**

- Be specific about location (street name, landmark)
- Describe what you see clearly
- Mention if it's a safety issue
- Be honest about severity

❌ **DON'T:**

- Use vague locations like "near my house"
- Exaggerate the problem
- Include opinions instead of facts
- Report issues outside your area

## Troubleshooting

**"Python not found"**

- Install Python from python.org or use app store

**"Permission denied"**

- On Mac/Linux: Try `python3` instead of `python`
- Check file permissions

**"Can't find reports"**

- Look in `reports/` subfolder
- Check file was created with today's date

**"Need to edit report after creation"**

- Open the text file with any text editor
- Edit and save before submitting

## Keyboard Shortcuts

- **Ctrl+C** - Cancel/exit at any time (won't save)
- **Enter** - Move to next question
- **Backspace** - Edit your input before pressing Enter

## Report Multiple Issues

After submitting first report, the tool asks:

```
Would you like to report another issue? (yes/no)
```

Type `yes` to continue reporting!

## Share Reports

The reports folder can be shared with:

- Local authority
- NGO working on civic issues
- Community group
- Social media (for awareness)
- Friends/neighbors affected

## Advanced Usage

For customizing departments and issue types, see: `CUSTOMIZATION.md`

For example reports and use cases, see: `EXAMPLES.md`

For detailed documentation, see: `README.md`

## Getting Help

**Inside the application:**

- Follow the on-screen instructions
- Press Enter to skip optional fields
- Ctrl+C to cancel at any time

**Error messages:**

- Read the error carefully
- Go back and re-enter information
- Check spelling and format

**Questions:**

- Refer to README.md
- Check EXAMPLES.md for sample reports
- See CUSTOMIZATION.md for advanced setups

## Success Stories

After submitting your report:

1. ✓ Your issue is documented
2. ✓ Authorities are aware of the problem
3. ✓ You've helped community improvement
4. ✓ Others may benefit from the same fix

## Ready to Go!

You now have everything needed to report public problems professionally!

```bash
python problem_reporter.py
```

**Start reporting now and make your community better!** 🚀

---

Questions or stuck? Review the full README.md or EXAMPLES.md for more information.
