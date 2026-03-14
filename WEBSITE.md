# AI Public Problem Reporter - Complete Website

A full-featured web application for citizens to report public issues to local authorities with tracking, analytics, and administration capabilities.

## 🌐 Website Features

### For Citizens

✨ **Easy Issue Reporting** - Multi-step form to report public problems
✨ **Smart Routing** - Automatically routes to correct department
✨ **Track Reports** - Real-time dashboard to monitor issue status
✨ **Community Impact** - See statistics on issues being resolved
✨ **Search & Filter** - Find specific reports easily
✨ **Comments & Updates** - Receive and add updates

### For Administrators

📊 **Analytics Dashboard** - View statistics and trends
📋 **Report Management** - Assign, update status, track progress
🏢 **Department Management** - Route to appropriate departments
📈 **Data Export** - Export reports in CSV/JSON formats
⚙️ **System Settings** - Configure departments and issue types

## 📦 Project Structure

```
ai_public_problem_reporter/
├── server.py                   # Flask backend application
├── requirements.txt            # Python dependencies
├── reports.db                  # SQLite database (created automatically)
├── templates/                  # HTML templates
│   ├── index.html             # Home page
│   ├── submit.html            # Report submission form
│   └── dashboard.html         # Reports dashboard
└── static/                     # Static files
    ├── style.css              # Styling
    └── script.js              # JavaScript
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install Flask directly:

```bash
pip install Flask==2.3.3
```

### 2. Run the Server

```bash
python server.py
```

You should see:

```
Starting AI Public Problem Reporter Web Server...
Visit: http://localhost:5000
```

### 3. Open in Browser

Open your web browser and go to:

```
http://localhost:5000
```

## 🌍 Website Pages

### Home Page (`/`)

- Hero section promoting the service
- Feature highlights
- Common issue types
- How it works explanation
- Community impact statistics
- Call to action

### Report Submission (`/submit`)

- 7-step guided form
- Issue type selection
- Location entry
- Detailed description
- Date and severity
- Optional evidence
- Contact information
- Professional report generation
- Success confirmation

### Dashboard (`/dashboard`)

- All submitted reports
- Real-time statistics
- Search functionality
- Severity and status filters
- Report details view
- Comments and updates
- Status tracking

## 📡 API Endpoints

### Report Management

| Method | Endpoint                   | Description          |
| ------ | -------------------------- | -------------------- |
| POST   | `/api/submit-report`       | Submit new report    |
| GET    | `/api/reports`             | Get all reports      |
| GET    | `/api/reports/<id>`        | Get specific report  |
| PUT    | `/api/reports/<id>/status` | Update report status |
| GET    | `/api/search`              | Search reports       |

### Comments

| Method | Endpoint                     | Description  |
| ------ | ---------------------------- | ------------ |
| GET    | `/api/reports/<id>/comments` | Get comments |
| POST   | `/api/reports/<id>/comments` | Add comment  |

### Analytics

| Method | Endpoint          | Description    |
| ------ | ----------------- | -------------- |
| GET    | `/api/statistics` | Get statistics |
| GET    | `/api/export/csv` | Export as CSV  |

### Configuration

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/api/departments` | Get all departments |

## 🗄️ Database Schema

### Reports Table

```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_id TEXT UNIQUE,              -- Unique report ID
    problem_type TEXT,                     -- Issue type
    location TEXT,                         -- Issue location
    description TEXT,                      -- Detailed description
    date_noticed TEXT,                     -- When noticed
    severity TEXT,                         -- Low/Medium/High
    evidence TEXT,                         -- Photos/videos info
    name TEXT,                             -- Reporter name
    phone TEXT,                            -- Reporter phone
    email TEXT,                            -- Reporter email
    department TEXT,                       -- Assigned department
    status TEXT,                           -- Current status
    created_at TIMESTAMP,                  -- Submission time
    updated_at TIMESTAMP                   -- Last update time
);
```

### Comments Table

```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER,                     -- Reference to report
    comment TEXT,                          -- Comment text
    created_at TIMESTAMP                   -- Creation time
);
```

## 🎨 Customization

### Change Department Mappings

Edit `DEPARTMENT_MAPPING` in `server.py`:

```python
DEPARTMENT_MAPPING = {
    "pothole": "Your Department Name",
    "garbage": "Sanitation Department",
    # Add more
}
```

### Modify Issue Types

Update the datalist in `submit.html`:

```html
<datalist id="issue-suggestions">
  <option value="Your Issue Type"></option>
</datalist>
```

### Custom Styling

Edit `static/style.css` to customize colors and design.

## 📊 Statistics & Reporting

The dashboard shows:

- **Total Reports Submitted** - Overall count
- **By Severity** - High, Medium, Low breakdown
- **By Status** - Submitted, In Progress, Resolved
- **By Department** - Distribution across departments
- **Report Trends** - Timeline of submissions

## 🔒 Security Considerations

For production deployment, add:

1. **Authentication** - User login system
2. **HTTPS** - SSL/TLS encryption
3. **Input Validation** - Sanitize all inputs
4. **CSRF Protection** - Flask-WTF
5. **CORS Configuration** - Restrict origins
6. **Rate Limiting** - Prevent spam
7. **Database Backups** - Regular backups

## 🚀 Deployment Options

### Local Development

```bash
python server.py
```

### Production with Gunicorn

```bash
pip install gunicorn
gunicorn server:app
```

### Docker

```bash
docker build -t problem-reporter .
docker run -p 5000:5000 problem-reporter
```

### Azure App Service

1. Configure `server.py` for Azure
2. Use Azure Database for production
3. Deploy via GitHub Actions

### Heroku

```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
```

## 📱 Mobile Responsive

The website is fully responsive:

- ✓ Mobile phones (320px+)
- ✓ Tablets (768px+)
- ✓ Desktops (1200px+)
- ✓ Large screens (2000px+)

## ♿ Accessibility

Features include:

- ✓ ARIA labels and roles
- ✓ Keyboard navigation
- ✓ Screen reader support
- ✓ High contrast mode compatible
- ✓ WCAG 2.1 Level AA compliant

## 🧪 Testing

### Test the Submission Form

1. Visit `http://localhost:5000/submit`
2. Fill in details:
   - Problem Type: "Pothole"
   - Location: "Main Street"
   - Description: "Large pothole"
   - Date: "Today"
   - Severity: "High"
3. Submit
4. View on dashboard

### Test the Dashboard

1. Visit `http://localhost:5000/dashboard`
2. Search for reports
3. Click filters
4. View report details

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Windows - Find process using port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Try different port
python server.py  # Edit to use different port
```

### Flask Not Found

```bash
pip install Flask==2.3.3
```

### Database Lock

```bash
# Remove locked database
rm reports.db

# Database will be recreated on next run
```

### CORS Issues

- Check browser console for errors
- Ensure frontend and backend are on same domain

## 📞 API Examples

### Submit a Report

```python
curl -X POST http://localhost:5000/api/submit-report \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "Pothole",
    "location": "Main Street",
    "description": "Large pothole",
    "date_noticed": "Today",
    "severity": "High",
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

### Get All Reports

```python
curl http://localhost:5000/api/reports
```

### Get Statistics

```python
curl http://localhost:5000/api/statistics
```

## 🎓 Educational Use

Perfect for teaching:

- Web development (HTML/CSS/JS)
- Backend development (Flask/Python)
- Database design (SQLite)
- RESTful APIs
- Civic engagement
- Full-stack development

## 📈 Growth Roadmap

Future enhancements:

- Photo uploads
- Email notifications
- Multi-language support
- Mobile app
- AI-powered categorization
- Predictive analytics
- Integration with government systems
- Advanced reporting tools
- Real-time notifications

## 🤝 Contributing

Ways to improve:

- Report bugs
- Suggest features
- Submit pull requests
- Test across browsers
- Test with different databases
- Improve documentation

## 📄 License

Open source for public benefit.

---

## 🚀 Getting Started Now

1. **Install Flask**: `pip install -r requirements.txt`
2. **Run server**: `python server.py`
3. **Visit website**: `http://localhost:5000`
4. **Start reporting**: Click "Report Issue"

**Questions?** See [CUSTOMIZATION.md](CUSTOMIZATION.md) or [QUICKSTART.md](QUICKSTART.md)

---

**Making communities better through technology and citizen engagement! 🌍**
