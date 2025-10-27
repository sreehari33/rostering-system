# Staff Rostering System - Complete Solution

## Overview
A comprehensive web-based staff rostering system with intelligent leave management, automatic replacements, and Excel export functionality.

## 🎯 Key Features

### 1. **Intelligent Shift Pattern Management**
- **Base Pattern**: Day → Night → Off → Off (repeating cycle)
- **Pulled after 1st Off**: Day → Night → Night(OT) → Off → Day
- **Pulled after 2nd Off**: Day → Night → Off → Day(OT) → Day
- Automatic pattern adjustment when staff are pulled for emergency coverage

### 2. **Smart Leave Priority System**
- Priority calculation based on:
  - Leave history (fewer recent leaves = higher priority)
  - Application timing (earlier applications get bonus points)
  - Emergency vs. planned leave differentiation
- Automatic conflict resolution using priority scores

### 3. **Intelligent Replacement Logic**
- **Rules for pulling staff**:
  - ✅ Can pull: Staff who had Day shift or Off on previous day
  - ❌ Cannot pull: Staff who had Night shift on previous day
  - 🎯 Priority: Based on recent pull history and comp offs owed
- Automatic replacement for emergency/sick leaves
- Maintains 8 people per shift (day and night)

### 4. **Comprehensive Excel Export**
The system generates a multi-sheet Excel file with:
- **Sheet 1**: Main Roster with color-coded shifts
- **Sheet 2**: Leave Applications with status tracking
- **Sheet 3**: Daily Statistics (shift counts, leaves, etc.)
- **Sheet 4**: Overtime & Compensatory Off Tracking
- **Sheet 5**: Legend with all shift codes and meanings

### 5. **Dual User Access**
- **Admin** (username: `admin`, password: `aliyan123`):
  - View and edit entire roster
  - Approve/reject leave applications
  - Manual shift adjustments
  - Full system access
  
- **User** (username: `user`, password: `user123`):
  - View roster
  - Apply for leaves
  - Track own leave applications
  - Read-only access to roster

## 📋 Shift Codes Explained

| Code | Description | Type | Color |
|------|-------------|------|-------|
| D | Day Shift (Regular) | Working | Yellow |
| N | Night Shift (Regular) | Working | Green |
| O | Off Day | Rest | Gray |
| D (OT) | Day Shift + Overtime | Working + OT | Orange (Bold Border) |
| N (OT) | Night Shift + Overtime | Working + OT | Light Green (Bold Border) |
| P/L | Planned Leave | Leave | Light Blue |
| S/L | Sick Leave | Leave | Light Red |
| E/L | Emergency Leave | Leave | Red |
| C/L | Casual Leave | Leave | Peach |
| C/O | Compensatory Off | Rest | Yellow |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Local Development Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
python app.py
```

3. **Access the System**
- Open browser and go to: `http://localhost:5000`
- Login with credentials:
  - Admin: `admin` / `aliyan123`
  - User: `user` / `user123`

### Production Deployment (Render/Heroku)

1. **For Render**:
   - Use the included `render.yaml` configuration
   - Push to GitHub
   - Connect repository to Render
   - Auto-deploy will handle the rest

2. **For Heroku**:
   - Use the included `Procfile.txt` (rename to `Procfile`)
   - Set environment variables if needed
   - Deploy using Git

## 📊 System Rules & Logic

### Leave Application Rules

1. **Planned Leave**:
   - Should be applied at least 7 days in advance
   - Higher priority if fewer recent leaves taken
   - Requires admin approval

2. **Emergency/Sick Leave**:
   - Processed immediately
   - Automatic replacement finding
   - System pulls available staff following rules

3. **Priority Calculation**:
   ```
   Base Priority = 100 - (Recent Leaves × 10)
   Time Bonus = Days Since Applied × 2 (max 20 points)
   Total Priority = Base Priority + Time Bonus
   ```

### Replacement Selection Logic

When someone takes emergency leave:

1. **Check Eligibility**:
   - Must be off on the day needing coverage
   - Previous day must NOT be night shift
   - Previous day must be day shift or off

2. **Calculate Pull Priority**:
   - Recent pulls count (more pulls = lower priority to be pulled again)
   - Compensatory offs owed (more owed = lower priority)
   - Selects person with lowest pull score (fairest to pull)

3. **Update Pattern**:
   - If pulled from first off: Gets Night(OT), then Off, then Day
   - If pulled from second off: Gets Day(OT), then Day
   - Compensatory off is tracked for future

### Shift Count Requirements

- **Day Shift**: 8 people required
- **Night Shift**: 8 people required
- System warns if counts fall below required levels
- Automatic replacement tries to maintain these counts

## 🖥️ Using the Web Application

### For Users

1. **View Roster**:
   - See entire month's schedule
   - Color-coded shifts for easy reading
   - Sticky headers for easy navigation

2. **Apply for Leave**:
   - Click "Apply Leave" button
   - Select employee, dates, and leave type
   - System calculates and shows priority score
   - Submit for admin approval

3. **Track Applications**:
   - View all leave applications
   - See status (Pending/Approved/Rejected)
   - View priority scores

### For Admins

1. **Edit Roster**:
   - Click any shift cell to edit
   - Choose new shift type
   - Changes save immediately

2. **Approve Leaves**:
   - View all pending applications
   - Sorted by priority (highest first)
   - Approve or reject with one click
   - System auto-updates roster and finds replacements

3. **Monitor Statistics**:
   - Daily shift counts
   - Leave statistics
   - Overtime tracking
   - Download Excel for detailed analysis

## 📁 File Structure

```
rostering-system/
│
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # Frontend UI
├── requirements.txt       # Python dependencies
├── roster_data.json       # Data storage (auto-generated)
├── roster.xlsx           # Excel export (auto-generated)
├── Procfile.txt          # For Heroku deployment
├── render.yaml           # For Render deployment
├── runtime.txt           # Python version
└── README.md             # This file
```

## 🔧 Technical Details

### Data Storage
- JSON file-based storage (roster_data.json)
- Persistent across restarts
- Includes: employees, roster, leaves, history, pulled staff, comp offs

### Session Management
- Secure session handling
- 1-hour session timeout
- Separate admin/user roles

### Excel Generation
- Real-time generation using openpyxl
- Color-coded cells
- Multiple sheets for different views
- Formatted headers and borders

## 🎨 Key Improvements Over Original

1. ✅ **Proper Shift Patterns**: Implemented correct D-N-O-O base pattern
2. ✅ **Smart Replacements**: Follows all rules for pulling staff
3. ✅ **Better Priority**: Comprehensive leave priority calculation
4. ✅ **Overtime Tracking**: Tracks who was pulled and comp offs owed
5. ✅ **Pattern Updates**: Automatic pattern adjustment after pulls
6. ✅ **Enhanced Excel**: 5 sheets with complete information
7. ✅ **Better UI**: Improved design with all rules explained
8. ✅ **Validation**: Ensures 8 people per shift requirement
9. ✅ **Statistics**: Daily breakdown of shift distribution
10. ✅ **Documentation**: Complete rules and information in-app

## 📝 Notes

- Roster is prepared for current month by default
- Can be extended to prepare for next month before 25th
- All changes sync to both JSON file and Excel export
- System prevents scheduling conflicts automatically
- Admin can override any automatic decision if needed

## 🐛 Troubleshooting

**Issue**: Cannot login
- **Solution**: Ensure credentials are correct (admin/aliyan123 or user/user123)

**Issue**: Roster not loading
- **Solution**: Check if roster_data.json exists, delete and restart to regenerate

**Issue**: Excel download not working
- **Solution**: Ensure openpyxl is installed, check write permissions

**Issue**: Session expired
- **Solution**: Session lasts 1 hour, simply login again

## 📞 Support

For issues or questions:
1. Check the "Rules & Info" tab in the application
2. Review this README
3. Check console logs (F12 in browser)

## 🔄 Future Enhancements (Optional)

- Email notifications for leave approvals
- Mobile app version
- Export to PDF
- Multi-month view
- Advanced analytics dashboard
- Shift swap functionality
- Integration with HR systems

---

**Version**: 2.0
**Last Updated**: October 2025
**Status**: Production Ready ✅
