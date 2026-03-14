"""
AI Public Problem Reporter
Helps citizens report public issues to local authorities with structured reports.
"""

import json
from datetime import datetime
from pathlib import Path


class ProblemReporter:
    """Main class to handle problem reporting and report generation."""
    
    # Department mapping for different issue types
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
    
    def __init__(self):
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)
    
    def get_problem_type(self) -> str:
        """Collect the type of problem from user."""
        print("\n" + "="*60)
        print("STEP 1: What type of problem do you want to report?")
        print("="*60)
        print("\nCommon issues:")
        print("  • Road damage, potholes, cracked pavement")
        print("  • Garbage, trash, litter")
        print("  • Water leakage, sewage issues")
        print("  • Street light not working")
        print("  • Broken traffic signs")
        print("  • Damaged sidewalk")
        print("  • Tree/vegetation issues")
        
        problem_type = input("\nEnter the type of problem: ").strip()
        if not problem_type:
            print("Error: Problem type cannot be empty!")
            return self.get_problem_type()
        return problem_type
    
    def get_location(self) -> str:
        """Collect the exact location of the issue."""
        print("\n" + "="*60)
        print("STEP 2: Where is the problem located?")
        print("="*60)
        print("\nProvide as much detail as possible:")
        print("  • Street name, area, ward number")
        print("  • Nearby landmarks or famous buildings")
        print("  • GPS coordinates (optional)")
        
        location = input("\nEnter the exact location: ").strip()
        if not location:
            print("Error: Location cannot be empty!")
            return self.get_location()
        return location
    
    def get_description(self) -> str:
        """Collect detailed description of the problem."""
        print("\n" + "="*60)
        print("STEP 3: Describe the problem in detail")
        print("="*60)
        print("\nProvide a clear description including:")
        print("  • What is the exact problem?")
        print("  • How big or extensive is it?")
        print("  • Is it affecting people or causing danger?")
        print("  • Any specific measurements (e.g., pothole size)")
        
        description = input("\nEnter detailed description: ").strip()
        if not description:
            print("Error: Description cannot be empty!")
            return self.get_description()
        return description
    
    def get_date_noticed(self) -> str:
        """Collect when the problem was first noticed."""
        print("\n" + "="*60)
        print("STEP 4: When was the problem first noticed?")
        print("="*60)
        print("\nFormat: Today, Yesterday, DD/MM/YYYY, or approximate date")
        
        date_noticed = input("\nEnter when problem was noticed: ").strip()
        if not date_noticed:
            print("Error: Date cannot be empty!")
            return self.get_date_noticed()
        return date_noticed
    
    def get_severity(self) -> str:
        """Collect severity level of the issue."""
        print("\n" + "="*60)
        print("STEP 5: What is the severity level?")
        print("="*60)
        print("\nSeverity levels:")
        print("  • Low: Minor issue, not urgent (e.g., minor litter)")
        print("  • Medium: Moderate issue requiring action (e.g., small pothole)")
        print("  • High: Urgent/dangerous (e.g., large pothole, no street light)")
        
        while True:
            severity = input("\nSelect severity (Low/Medium/High): ").strip().capitalize()
            if severity in self.SEVERITY_LEVELS:
                return severity
            print(f"Error: Please enter one of {self.SEVERITY_LEVELS}")
    
    def get_additional_evidence(self) -> str:
        """Collect optional additional evidence or notes."""
        print("\n" + "="*60)
        print("STEP 6: Additional evidence or notes (Optional)")
        print("="*60)
        print("\nYou can add:")
        print("  • Photo location or description (if available)")
        print("  • Video description")
        print("  • Previous reports about same issue")
        print("  • Any other relevant information")
        print("  (Press Enter to skip)")
        
        evidence = input("\nEnter additional information: ").strip()
        return evidence if evidence else "None"
    
    def get_contact_details(self) -> dict:
        """Collect optional contact details."""
        print("\n" + "="*60)
        print("STEP 7: Contact Details (Optional)")
        print("="*60)
        print("\nTo help authorities follow up with you:")
        print("  (All fields are optional)")
        
        contact = {}
        contact['name'] = input("Your name (or Anonymous): ").strip() or "Anonymous"
        contact['phone'] = input("Phone number (optional): ").strip() or "Not provided"
        contact['email'] = input("Email address (optional): ").strip() or "Not provided"
        
        return contact
    
    def suggest_department(self, problem_type: str) -> str:
        """Suggest the appropriate department based on problem type."""
        problem_lower = problem_type.lower()
        
        # Check for direct matches
        for key, department in self.DEPARTMENT_MAPPING.items():
            if key in problem_lower:
                return department
        
        # If no match found, return generic suggestion
        return "Municipal Corporation / General Public Works"
    
    def generate_report(self, data: dict) -> str:
        """Generate the structured report."""
        report = []
        report.append("\n" + "="*60)
        report.append("PUBLIC ISSUE REPORT")
        report.append("="*60)
        report.append("")
        report.append(f"Issue Type:        {data['problem_type']}")
        report.append(f"Location:          {data['location']}")
        report.append(f"Description:       {data['description']}")
        report.append(f"Date Reported:     {data['date_noticed']}")
        report.append(f"Severity Level:    {data['severity']}")
        report.append(f"Additional Notes:  {data['evidence']}")
        report.append("")
        report.append("-"*60)
        report.append(f"Recommended Department:")
        report.append(f"{data['department']}")
        report.append("-"*60)
        report.append("")
        report.append("CITIZEN CONTACT INFORMATION")
        report.append("-"*60)
        report.append(f"Name:               {data['contact']['name']}")
        report.append(f"Phone:              {data['contact']['phone']}")
        report.append(f"Email:              {data['contact']['email']}")
        report.append("")
        report.append(f"Report Generated:  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        report.append("="*60)
        
        return "\n".join(report)
    
    def save_report(self, report: str, problem_type: str) -> str:
        """Save the report to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{problem_type.replace(' ', '_')}_{timestamp}.txt"
        filepath = self.report_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(filepath)
    
    def save_json_report(self, data: dict) -> str:
        """Save the report in JSON format for easy processing."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{data['problem_type'].replace(' ', '_')}_{timestamp}.json"
        filepath = self.report_dir / filename
        
        json_data = {
            **data,
            'report_generated': datetime.now().isoformat(),
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def run(self):
        """Main function to run the problem reporter."""
        print("\n" + "╔" + "="*58 + "╗")
        print("║" + " "*15 + "AI PUBLIC PROBLEM REPORTER" + " "*17 + "║")
        print("║" + " "*18 + "Report Public Issues Easily" + " "*14 + "║")
        print("╚" + "="*58 + "╝")
        print("\nThis tool helps you report public problems to local authorities.")
        print("Your input will generate a structured report.")
        
        try:
            # Collect all information
            problem_type = self.get_problem_type()
            location = self.get_location()
            description = self.get_description()
            date_noticed = self.get_date_noticed()
            severity = self.get_severity()
            evidence = self.get_additional_evidence()
            contact = self.get_contact_details()
            department = self.suggest_department(problem_type)
            
            # Prepare data
            data = {
                'problem_type': problem_type,
                'location': location,
                'description': description,
                'date_noticed': date_noticed,
                'severity': severity,
                'evidence': evidence,
                'contact': contact,
                'department': department,
            }
            
            # Generate and display report
            report = self.generate_report(data)
            print(report)
            
            # Save reports
            txt_path = self.save_report(report, problem_type)
            json_path = self.save_json_report(data)
            
            print("\n✓ Report saved successfully!")
            print(f"  Text format: {txt_path}")
            print(f"  JSON format: {json_path}")
            
            print("\n" + "="*60)
            print("NEXT STEPS:")
            print("="*60)
            print(f"1. Submit this report to: {department}")
            print("2. Keep a copy for your records")
            print("3. Follow up with authorities in 7-10 days if no action")
            print("4. You can share the report via email or in person")
            print("="*60)
            
            # Ask if user wants to submit another report
            another = input("\nWould you like to report another issue? (yes/no): ").strip().lower()
            if another in ['yes', 'y']:
                self.run()
            else:
                print("\nThank you for reporting! Together we can improve our community.")
                print("="*60 + "\n")
        
        except KeyboardInterrupt:
            print("\n\nReport cancelled by user.")
        except Exception as e:
            print(f"\nError occurred: {e}")
            print("Please try again.")


def main():
    """Entry point for the application."""
    reporter = ProblemReporter()
    reporter.run()


if __name__ == "__main__":
    main()
