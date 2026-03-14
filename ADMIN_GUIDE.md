# AI Public Problem Reporter - Administrator Guide

Complete guide for system administrators to manage and operate the problem reporter website.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Server Management](#server-management)
3. [Database Management](#database-management)
4. [Configuration](#configuration)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)
8. [Security](#security)
9. [Performance](#performance)
10. [Scaling](#scaling)

---

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Basic knowledge of command line
- 500 MB disk space minimum

### Initial Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create Configuration File** (optional)

   ```bash
   cp config.example.py config.py
   ```

3. **Initialize Database**

   ```python
   python manage.py init_db
   ```

4. **Start Server**
   ```bash
   python server.py
   ```

---

## Server Management

### Starting the Server

**Windows:**

```bash
run_server.bat
```

**macOS/Linux:**

```bash
bash run_server.sh
```

**Docker:**

```bash
docker run -p 5000:5000 problem-reporter:latest
```

**Gunicorn (Production):**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Monitoring Server Status

Check if server is running:

```bash
curl http://localhost:5000/
```

View active connections:

```bash
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000
```

### Stopping the Server

- Press `Ctrl+C` in terminal
- Or kill the process:

  ```bash
  # Windows
  taskkill /PID <PID> /F

  # macOS/Linux
  kill -9 <PID>
  ```

### Server Logs

View Flask development logs:

```bash
# Enable debug mode
FLASK_ENV=development python server.py

# View detailed logs
python server.py 2>&1 | tee server.log
```

For production logging:

```python
import logging
logging.basicConfig(filename='reports.log')
```

---

## Database Management

### Database File

Location: `reports.db` (SQLite)

### Backing Up Database

**Manual Backup:**

```bash
# Windows
copy reports.db reports.db.backup

# macOS/Linux
cp reports.db reports.db.backup
```

**Automated Backup Script:**

```python
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy('reports.db', f'backups/reports_{timestamp}.db')
    print(f"Backup created: reports_{timestamp}.db")

# Run daily
backup_database()
```

### Restoring from Backup

```bash
# Windows
copy reports.db.backup reports.db

# macOS/Linux
cp reports.db.backup reports.db
```

### Database Maintenance

**Check Database Integrity:**

```python
import sqlite3

conn = sqlite3.connect('reports.db')
cursor = conn.cursor()
cursor.execute('PRAGMA integrity_check')
result = cursor.fetchone()
print(result)
conn.close()
```

**Optimize Database:**

```python
conn = sqlite3.connect('reports.db')
cursor = conn.cursor()
cursor.execute('VACUUM')
cursor.execute('ANALYZE')
conn.commit()
conn.close()
```

### Exporting Data

**Export All Reports:**

```python
import sqlite3
import csv
from datetime import datetime

def export_reports():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports')

    rows = cursor.fetchall()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(f'export/reports_{timestamp}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([col[0] for col in cursor.description])
        writer.writerows(rows)

    conn.close()
    print(f"Exported {len(rows)} reports")

export_reports()
```

### Database Queries

**Get Report Count by Severity:**

```python
cursor.execute('SELECT severity, COUNT(*) FROM reports GROUP BY severity')
print(cursor.fetchall())
```

**Find High Priority Reports:**

```python
cursor.execute('SELECT * FROM reports WHERE severity = "High" AND status != "Resolved"')
high_priority = cursor.fetchall()
```

**Get Reports by Department:**

```python
cursor.execute('SELECT department, COUNT(*) FROM reports GROUP BY department')
print(cursor.fetchall())
```

---

## Configuration

### Environment Variables

Create `.env` file:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=sqlite:///reports.db
MAX_UPLOAD_SIZE=16777216
SECRET_KEY=your-secret-key-here
```

### Department Customization

Edit `server.py` - `DEPARTMENT_MAPPING`:

```python
DEPARTMENT_MAPPING = {
    "pothole": "Public Works Department",
    "garbage": "Sanitation Department",
    "water leak": "Water Authority",
    # Add your departments
}
```

### Issue Type Configuration

Update list in `templates/submit.html`:

```html
<datalist id="issue-suggestions">
  <option value="Your Issue Type 1"></option>
  <option value="Your Issue Type 2"></option>
</datalist>
```

### Severity Levels

Modify in `server.py`:

```python
SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]
```

### Color Scheme

Edit `static/style.css`:

```css
:root {
  --primary-color: #2563eb;
  --secondary-color: #10b981;
  --danger-color: #ef4444;
  /* Customize colors */
}
```

---

## Monitoring

### Key Metrics to Track

1. **Reports Submitted** - Total volume
2. **Resolution Time** - Average time to resolve
3. **Department Capacity** - Reports per department
4. **User Engagement** - Active reporters
5. **System Performance** - Response times

### Generate Reports

**Daily Summary:**

```python
from datetime import datetime, timedelta
import sqlite3

def daily_summary():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    yesterday = datetime.now() - timedelta(days=1)

    cursor.execute(
        'SELECT COUNT(*) FROM reports WHERE DATE(created_at) = DATE(?)',
        (yesterday,)
    )
    count = cursor.fetchone()[0]

    print(f"Reports submitted yesterday: {count}")
    conn.close()

daily_summary()
```

**Monthly Analytics:**

```python
def monthly_analytics():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    # Total reports
    cursor.execute('SELECT COUNT(*) FROM reports')
    total = cursor.fetchone()[0]

    # Resolved
    cursor.execute("SELECT COUNT(*) FROM reports WHERE status = 'Resolved'")
    resolved = cursor.fetchone()[0]

    # In progress
    cursor.execute("SELECT COUNT(*) FROM reports WHERE status = 'In Progress'")
    in_progress = cursor.fetchone()[0]

    print(f"Total: {total}, Resolved: {resolved}, In Progress: {in_progress}")
    conn.close()

monthly_analytics()
```

### Performance Monitoring

Monitor system resources:

```bash
# Check CPU/Memory usage
# Windows
wmic os get TotalVisibleMemorySize, FreePhysicalMemory

# macOS/Linux
free -h
```

---

## Troubleshooting

### Server Won't Start

**Port Already in Use:**

```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F

# Try different port
# Edit server.py: app.run(port=5001)
```

**Python Not Found:**

```bash
# Verify Python installation
python --version

# Add Python to PATH if needed
```

**Flask Import Error:**

```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Database Issues

**Database Locked:**

```bash
# Your system might be accessing it elsewhere
# Stop all Python processes and try again
```

**Database Corrupted:**

```bash
# Restore from backup
cp reports.db.backup reports.db

# Or delete and recreate
# (This will lose all data - only if no backup)
rm reports.db
python server.py  # Will recreate
```

### Performance Issues

**Slow Response Times:**

1. Check database size: `ls -lh reports.db`
2. Run database optimization: `VACUUM` and `ANALYZE`
3. Check server logs for errors
4. Monitor system resources

**High Memory Usage:**

1. Restart Flask server
2. Close other applications
3. Check for memory leaks in logs
4. Consider upgrading server hardware

### API Errors

**Submit Report Fails:**

1. Check form validation in browser console
2. Verify all required fields are filled
3. Check server logs for database errors
4. Test with curl: `curl -X POST http://localhost:5000/api/submit-report`

---

## Maintenance

### Regular Tasks

**Daily:**

- Monitor server status
- Check error logs
- Verify database integrity

**Weekly:**

- Backup database
- Review submitted reports
- Check system resources

**Monthly:**

- Run analytics report
- Archive old records (optional)
- Update documentation
- Review and address bug reports

### Updates

**Update Flask:**

```bash
pip install --upgrade Flask
```

**Update All Dependencies:**

```bash
pip install --upgrade -r requirements.txt
```

### Create Maintenance Window

```python
# Add to server.py
app.config['MAINTENANCE_MODE'] = False

@app.before_request
def check_maintenance():
    if app.config['MAINTENANCE_MODE']:
        return "Server under maintenance", 503
```

---

## Security

### Access Control

Add authentication:

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and password == 'secret':
        return username

@app.route('/admin')
@auth.login_required
def admin():
    return "Admin Panel"
```

### Data Protection

**Backup Encrypted:**

```bash
# Encrypt database file
gpg --symmetric reports.db

# Decrypt when needed
gpg reports.db.gpg
```

**Update Database Password** (if using MySQL):

```python
# In production, use database user with limited privileges
```

### HTTPS in Production

Use SSL certificate:

```python
# gunicorn with SSL
gunicorn --certfile=cert.pem --keyfile=key.pem server:app
```

---

## Performance

### Optimization Tips

1. **Database Indexes:**

   ```python
   cursor.execute('CREATE INDEX IF NOT EXISTS idx_severity ON reports(severity)')
   cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON reports(status)')
   cursor.execute('CREATE INDEX IF NOT EXISTS idx_department ON reports(department)')
   ```

2. **Caching:**

   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})

   @app.route('/api/statistics')
   @cache.cached(timeout=300)
   def get_statistics():
       # Returns cached data for 5 minutes
   ```

3. **Pagination:**

   ```python
   # Limit results returned
   ITEMS_PER_PAGE = 20

   cursor.execute('SELECT * FROM reports LIMIT ? OFFSET ?',
                 (ITEMS_PER_PAGE, offset))
   ```

### Load Testing

Test with multiple concurrent users:

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# Using wrk
wrk -c 10 -t 4 -d 30s http://localhost:5000/
```

---

## Scaling

### Horizontal Scaling

Run multiple instances:

```bash
# Instance 1
python server.py --port 5000

# Instance 2
python server.py --port 5001

# Use load balancer (nginx) to distribute
```

### Vertical Scaling

Upgrade server resources:

- Increase RAM
- Use faster CPU
- Upgrade storage
- Use SSD for database

### Database Scaling

Migrate to production database:

```python
# PostgreSQL (recommended for production)
DATABASE_URL = "postgresql://user:pass@localhost/reports_db"

# MySQL
DATABASE_URL = "mysql+pymysql://user:pass@localhost/reports_db"
```

---

## Emergency Procedures

### Emergency Backup

```bash
# Immediate backup
cp reports.db /mnt/backup/reports_$(date +%Y%m%d_%H%M%S).db
```

### Emergency Shutdown

```bash
# Graceful shutdown
kill -TERM <PID>

# Force shutdown
kill -9 <PID>
```

### Recovery Plan

1. Stop server
2. Restore from most recent backup
3. Verify database integrity
4. Restart server
5. Test functionality
6. Notify users if needed

---

## Support Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **Python Docs**: https://docs.python.org/3/
- **Common Issues**: See TROUBLESHOOTING.md

---

## Contact & Escalation

For urgent issues:

1. Check server logs
2. Review troubleshooting guide
3. Consult documentation
4. Contact development team

---

**System administration is crucial for maintaining a reliable service. Follow these guidelines to ensure optimal performance and data safety!** 🔧
