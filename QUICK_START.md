# 🚀 Quick Start Guide - Staff Rostering System

## Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the System
Open your browser and go to: **http://localhost:5000**

## Login Credentials

### Admin Access (Full Control)
- **Username**: `admin`
- **Password**: `aliyan123`
- **Can**: Edit roster, approve leaves, download Excel

### User Access (View & Apply)
- **Username**: `user`
- **Password**: `user123`
- **Can**: View roster, apply for leave

## 📊 What You'll See

1. **Roster Tab**: Monthly schedule with color-coded shifts
2. **Leave Applications Tab**: Apply for leave and track status
3. **Statistics Tab**: View shift counts and overtime tracking
4. **Rules & Info Tab**: Complete system documentation

## 🎯 Quick Actions

### As Admin:
1. ✏️ **Edit Shift**: Click any shift cell in roster → Select new shift → Save
2. ✅ **Approve Leave**: Go to Leave Applications → Click Approve/Reject
3. 📥 **Download Excel**: Click "Download Excel" button in header

### As User:
1. 📝 **Apply Leave**: Leave Applications → Click "+ Apply Leave" → Fill form
2. 👀 **View Roster**: See your schedule in Roster tab
3. 📊 **Check Priority**: Your leave applications show priority score

## 🔧 System Features at a Glance

### Shift Patterns
- **Base**: Day → Night → Off → Off
- **Pulled 1st Off**: Day → Night → Night(OT) → Off → Day
- **Pulled 2nd Off**: Day → Night → Off → Day(OT) → Day

### Leave Priority
- Based on leave history (fewer leaves = higher priority)
- Earlier applications get bonus points
- Emergency leaves processed immediately

### Replacement Rules
- ✅ Can pull: Staff with Day/Off previous day
- ❌ Cannot pull: Staff with Night shift previous day
- System auto-finds best replacement

## 📁 Excel Export Contains

1. **Main Roster** - Color-coded monthly schedule
2. **Leave Applications** - All requests with status
3. **Daily Statistics** - Shift counts per day
4. **Overtime Tracking** - Who was pulled and comp offs owed
5. **Legend** - All shift codes explained

## 💡 Pro Tips

1. **Admin**: Check Statistics tab regularly to monitor shift distribution
2. **User**: Apply for planned leave early for better priority score
3. **Both**: Download Excel for offline reference
4. **Admin**: Use Rules & Info tab to understand all system logic

## ❓ Common Questions

**Q: How is leave priority calculated?**
A: Base score (100 - recent leaves × 10) + time bonus (days since applied × 2)

**Q: What happens with emergency leave?**
A: System automatically finds replacement following all rules and updates roster

**Q: Can I change shifts manually?**
A: Yes, if you're an admin. Just click the shift cell and select new value.

**Q: How many people per shift?**
A: Target is 8 people in day shift and 8 in night shift

**Q: What is overtime (OT)?**
A: When staff are pulled from their off day to cover emergency leave

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't login | Check credentials (admin/aliyan123 or user/user123) |
| Roster not loading | Delete roster_data.json and restart app |
| Excel won't download | Check openpyxl is installed |
| Session expired | Login again (sessions last 1 hour) |

## 📞 Need Help?

1. Check the **Rules & Info** tab in the application
2. Read the complete **README.md** file
3. Press F12 to see console logs for errors

---

**Ready to use!** The system auto-generates initial roster data on first run. 🎉
