from flask import Flask, render_template, request, jsonify, send_file, session
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
app.secret_key = 'rostering_secret_key_2025'

DATA_FILE = 'roster_data.json'
EXCEL_FILE = 'roster.xlsx'

# Admin and User credentials
CREDENTIALS = {
    'admin': 'aliyan123',
    'user': 'user123'
}

def initialize_data():
    """Initialize roster data if not exists"""
    if not os.path.exists(DATA_FILE):
        employees = [
            {"name": "Namita Chowdhry", "emp_id": "85005100"},
            {"name": "Santhosh Rajaram Bathula(A320)", "emp_id": "85009008"},
            {"name": "Kaustubh B(B737)", "emp_id": "85002606"},
            {"name": "Vijay Gupta (B737)", "emp_id": "85002536"},
            {"name": "Manu Mohan (A320&B737)", "emp_id": "85005688"},
            {"name": "Macken Vaz(Tr)", "emp_id": "85003846"},
            {"name": "Karthikeyan(A320)", "emp_id": "85008568"},
            {"name": "Mahadev S. (A320)", "emp_id": "85005686"},
            {"name": "Vivek Chauhan (B737)", "emp_id": "85005699"},
            {"name": "Balamurugan Alagarsamy(A320)", "emp_id": "85008436"},
            {"name": "Jeet Pati (737)", "emp_id": "85011116"},
            {"name": "Siddique(Tr)", "emp_id": "85002426"},
            {"name": "Anal Kumar(Tr)", "emp_id": "85005698"},
            {"name": "Pravin C(A320)", "emp_id": "85002324"},
            {"name": "Dinesh S (8737)", "emp_id": "85003309"},
            {"name": "Maniraj S (A320)", "emp_id": "85008569"},
            {"name": "Ashish KS (A320&B737)", "emp_id": "85005689"},
            {"name": "Praful K (B737)", "emp_id": "85005689"},
            {"name": "Vivian Reginald Philip Pais (A320)", "emp_id": "85009317"},
            {"name": "Jefferson(A320)", "emp_id": "85008549"},
            {"name": "Abhimanyu (320)", "emp_id": "85007148"},
            {"name": "Vishnu Deva (A320)", "emp_id": "85008996"},
            {"name": "Janarthanan S(320)", "emp_id": "85005687"},
            {"name": "Ashish Kumar Verma(B737)", "emp_id": "85002951"},
            {"name": "Pravin J", "emp_id": "85002324"},
            {"name": "Vivek Pataskar(A320)", "emp_id": "85004114"},
            {"name": "Kshiteej S (8737)", "emp_id": "85002300"},
            {"name": "Prem (A320)", "emp_id": "85008783"},
            {"name": "Rashu(A320)", "emp_id": "85009429"},
            {"name": "Chetan kumar Gururani (A320)", "emp_id": "85008265"},
            {"name": "Yemuna BL", "emp_id": "85005685"},
            {"name": "Narender (A320)", "emp_id": "85004116"},
            {"name": "Sagar (A320)", "emp_id": "85008835"},
            {"name": "Soumee", "emp_id": "85005088"},
            {"name": "Nikita J(B737)", "emp_id": "85002171"}
        ]
        
        # Initialize roster for current month
        today = datetime.now()
        year = today.year
        month = today.month
        days_in_month = 31
        
        roster = {}
        patterns = [
            ["N/O", "O", "D", "N", "N/O", "D", "D"],  # Pattern 1
            ["N/O", "O", "D", "N", "N", "O", "S/L"],  # Pattern 2
            ["N", "O", "D", "D", "N/O", "O", "P/L"],  # Pattern 3
            ["N", "O", "D", "TRG", "TRG", "O", "D"],  # Pattern 4
            ["N/O", "O", "P/L", "P/L", "P/L", "P/L", "P/L"],  # Pattern 5
            ["N/O", "O", "D", "N", "N", "O", "D"],  # Pattern 6
            ["N", "O", "D", "N", "N/O", "D", "D"],  # Pattern 7
            ["N/O", "O", "C/O", "N3", "N", "N", "D"]  # Pattern 8
        ]
        
        for idx, emp in enumerate(employees):
            pattern = patterns[idx % len(patterns)]
            emp_roster = []
            for day in range(1, days_in_month + 1):
                shift = pattern[(day - 1) % len(pattern)]
                emp_roster.append(shift)
            roster[emp['emp_id']] = emp_roster
        
        data = {
            'employees': employees,
            'roster': roster,
            'leave_applications': [],
            'year': year,
            'month': month,
            'leave_history': {}
        }
        
        save_data(data)
        return data
    else:
        return load_data()

def load_data():
    """Load data from JSON file"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_leave_priority(emp_id, data):
    """Calculate leave priority based on history"""
    history = data.get('leave_history', {}).get(emp_id, [])
    # Higher priority for those who took less leave
    leave_count = len(history)
    base_priority = 100 - (leave_count * 5)
    return max(base_priority, 0)

def get_shift_type(shift_code):
    """Determine shift type from code"""
    if shift_code in ['D']:
        return 'day'
    elif shift_code in ['N', 'N/O', 'N3']:
        return 'night'
    else:
        return 'other'

def find_replacement(emp_id, date_idx, data):
    """Find replacement for emergency leave"""
    roster = data['roster']
    employees = data['employees']
    
    available = []
    for emp in employees:
        e_id = emp['emp_id']
        if e_id == emp_id:
            continue
        
        # Check previous day shift
        if date_idx > 0:
            prev_shift = roster[e_id][date_idx - 1]
            prev_type = get_shift_type(prev_shift)
            
            # Can only pull if they had day shift or off previous day
            if prev_type != 'night':
                current_shift = roster[e_id][date_idx]
                if current_shift in ['O', 'N/O']:  # If they're off
                    available.append(e_id)
    
    return available[0] if available else None

def count_shifts_by_type(date_idx, data):
    """Count day and night shifts for a date"""
    roster = data['roster']
    day_count = 0
    night_count = 0
    
    for emp_id, shifts in roster.items():
        shift = shifts[date_idx]
        shift_type = get_shift_type(shift)
        if shift_type == 'day':
            day_count += 1
        elif shift_type == 'night':
            night_count += 1
    
    return day_count, night_count

def generate_excel(data):
    """Generate Excel file with roster"""
    wb = Workbook()
    
    # Sheet 1: Main Roster
    ws_roster = wb.active
    ws_roster.title = "Roster"
    
    # Header styling
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Days in month
    year = data['year']
    month = data['month']
    days_in_month = 31
    
    # Header row 1: Day numbers
    ws_roster.cell(1, 1, "NAME").fill = header_fill
    ws_roster.cell(1, 1).font = header_font
    ws_roster.cell(1, 1).border = border
    ws_roster.cell(1, 2, "EMP ID").fill = header_fill
    ws_roster.cell(1, 2).font = header_font
    ws_roster.cell(1, 2).border = border
    
    for day in range(1, days_in_month + 1):
        cell = ws_roster.cell(1, day + 2, day)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = Alignment(horizontal='center')
    
    # Header row 2: Day names
    ws_roster.cell(2, 1, "").fill = header_fill
    ws_roster.cell(2, 1).border = border
    ws_roster.cell(2, 2, "").fill = header_fill
    ws_roster.cell(2, 2).border = border
    
    day_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    for day in range(1, days_in_month + 1):
        day_name = day_names[(day - 1) % 7]
        cell = ws_roster.cell(2, day + 2, day_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = Alignment(horizontal='center')
    
    # Employee data
    employees = data['employees']
    roster = data['roster']
    
    for idx, emp in enumerate(employees):
        row = idx + 3
        ws_roster.cell(row, 1, emp['name']).border = border
        ws_roster.cell(row, 2, emp['emp_id']).border = border
        
        emp_roster = roster.get(emp['emp_id'], [])
        for day in range(1, min(days_in_month + 1, len(emp_roster) + 1)):
            shift = emp_roster[day - 1] if day - 1 < len(emp_roster) else ""
            cell = ws_roster.cell(row, day + 2, shift)
            cell.border = border
            cell.alignment = Alignment(horizontal='center')
            
            # Color coding for shifts
            if shift == 'D':
                cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
            elif shift in ['N', 'N/O', 'N3']:
                cell.fill = PatternFill(start_color="C6E0B4", end_color="C6E0B4", fill_type="solid")
            elif shift == 'O':
                cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    
    # Adjust column widths
    ws_roster.column_dimensions['A'].width = 35
    ws_roster.column_dimensions['B'].width = 12
    from openpyxl.utils import get_column_letter
    for col in range(3, days_in_month + 3):
        ws_roster.column_dimensions[get_column_letter(col)].width = 6
    
    # Sheet 2: Leave Applications
    ws_leave = wb.create_sheet("Leave Applications")
    ws_leave.cell(1, 1, "Employee Name").fill = header_fill
    ws_leave.cell(1, 1).font = header_font
    ws_leave.cell(1, 2, "Employee ID").fill = header_fill
    ws_leave.cell(1, 2).font = header_font
    ws_leave.cell(1, 3, "From Date").fill = header_fill
    ws_leave.cell(1, 3).font = header_font
    ws_leave.cell(1, 4, "To Date").fill = header_fill
    ws_leave.cell(1, 4).font = header_font
    ws_leave.cell(1, 5, "Leave Type").fill = header_fill
    ws_leave.cell(1, 5).font = header_font
    ws_leave.cell(1, 6, "Status").fill = header_fill
    ws_leave.cell(1, 6).font = header_font
    ws_leave.cell(1, 7, "Priority").fill = header_fill
    ws_leave.cell(1, 7).font = header_font
    ws_leave.cell(1, 8, "Applied Date").fill = header_fill
    ws_leave.cell(1, 8).font = header_font
    
    leave_apps = data.get('leave_applications', [])
    for idx, leave in enumerate(leave_apps):
        row = idx + 2
        ws_leave.cell(row, 1, leave['emp_name'])
        ws_leave.cell(row, 2, leave['emp_id'])
        ws_leave.cell(row, 3, leave['from_date'])
        ws_leave.cell(row, 4, leave['to_date'])
        ws_leave.cell(row, 5, leave['leave_type'])
        ws_leave.cell(row, 6, leave['status'])
        ws_leave.cell(row, 7, leave.get('priority', 0))
        ws_leave.cell(row, 8, leave.get('applied_date', ''))
    
    ws_leave.column_dimensions['A'].width = 35
    ws_leave.column_dimensions['B'].width = 12
    ws_leave.column_dimensions['C'].width = 12
    ws_leave.column_dimensions['D'].width = 12
    ws_leave.column_dimensions['E'].width = 15
    ws_leave.column_dimensions['F'].width = 12
    ws_leave.column_dimensions['G'].width = 10
    ws_leave.column_dimensions['H'].width = 15
    
    # Sheet 3: Statistics
    ws_stats = wb.create_sheet("Statistics")
    ws_stats.cell(1, 1, "Shift Statistics").font = Font(bold=True, size=14)
    ws_stats.cell(3, 1, "Date").fill = header_fill
    ws_stats.cell(3, 1).font = header_font
    ws_stats.cell(3, 2, "Day Shift Count").fill = header_fill
    ws_stats.cell(3, 2).font = header_font
    ws_stats.cell(3, 3, "Night Shift Count").fill = header_fill
    ws_stats.cell(3, 3).font = header_font
    
    for day in range(1, days_in_month + 1):
        day_count, night_count = count_shifts_by_type(day - 1, data)
        ws_stats.cell(day + 3, 1, f"{year}-{month:02d}-{day:02d}")
        ws_stats.cell(day + 3, 2, day_count)
        ws_stats.cell(day + 3, 3, night_count)
    
    ws_stats.column_dimensions['A'].width = 15
    ws_stats.column_dimensions['B'].width = 18
    ws_stats.column_dimensions['C'].width = 18
    
    wb.save(EXCEL_FILE)
    return EXCEL_FILE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username in CREDENTIALS and CREDENTIALS[username] == password:
        session['user'] = username
        session['role'] = username
        return jsonify({'success': True, 'role': username})
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return jsonify({'success': True})

@app.route('/check-auth')
def check_auth():
    if 'user' in session:
        return jsonify({'authenticated': True, 'role': session['role']})
    return jsonify({'authenticated': False})

@app.route('/get-roster')
def get_roster():
    data = load_data()
    return jsonify(data)

@app.route('/update-shift', methods=['POST'])
def update_shift():
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    emp_id = request.json.get('emp_id')
    date_idx = request.json.get('date_idx')
    new_shift = request.json.get('shift')
    
    data = load_data()
    if emp_id in data['roster']:
        data['roster'][emp_id][date_idx] = new_shift
        save_data(data)
        generate_excel(data)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Employee not found'})

@app.route('/apply-leave', methods=['POST'])
def apply_leave():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = load_data()
    leave_data = request.json
    
    # Calculate priority
    priority = calculate_leave_priority(leave_data['emp_id'], data)
    
    leave_app = {
        'id': len(data['leave_applications']) + 1,
        'emp_id': leave_data['emp_id'],
        'emp_name': leave_data['emp_name'],
        'from_date': leave_data['from_date'],
        'to_date': leave_data['to_date'],
        'leave_type': leave_data['leave_type'],
        'reason': leave_data.get('reason', ''),
        'status': 'Pending',
        'priority': priority,
        'applied_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    data['leave_applications'].append(leave_app)
    save_data(data)
    generate_excel(data)
    
    return jsonify({'success': True, 'message': 'Leave application submitted'})

@app.route('/approve-leave', methods=['POST'])
def approve_leave():
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    leave_id = request.json.get('leave_id')
    action = request.json.get('action')
    
    data = load_data()
    
    for leave in data['leave_applications']:
        if leave['id'] == leave_id:
            leave['status'] = 'Approved' if action == 'approve' else 'Rejected'
            
            if action == 'approve':
                # Update roster with leave
                emp_id = leave['emp_id']
                from_date = datetime.strptime(leave['from_date'], '%Y-%m-%d')
                to_date = datetime.strptime(leave['to_date'], '%Y-%m-%d')
                
                current_date = from_date
                while current_date <= to_date:
                    day_idx = current_date.day - 1
                    if day_idx < len(data['roster'][emp_id]):
                        # Mark as leave based on type
                        if leave['leave_type'] == 'Sick Leave':
                            data['roster'][emp_id][day_idx] = 'S/L'
                            # Find replacement
                            replacement = find_replacement(emp_id, day_idx, data)
                            if replacement:
                                data['roster'][replacement][day_idx] = 'D (OT)'
                        elif leave['leave_type'] == 'Emergency Leave':
                            data['roster'][emp_id][day_idx] = 'E/L'
                            replacement = find_replacement(emp_id, day_idx, data)
                            if replacement:
                                data['roster'][replacement][day_idx] = 'D (OT)'
                        else:
                            data['roster'][emp_id][day_idx] = 'P/L'
                    
                    current_date += timedelta(days=1)
                
                # Update leave history
                if 'leave_history' not in data:
                    data['leave_history'] = {}
                if emp_id not in data['leave_history']:
                    data['leave_history'][emp_id] = []
                data['leave_history'][emp_id].append({
                    'from': leave['from_date'],
                    'to': leave['to_date'],
                    'type': leave['leave_type']
                })
            
            save_data(data)
            generate_excel(data)
            return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Leave application not found'})

@app.route('/download-excel')
def download_excel():
    data = load_data()
    generate_excel(data)
    return send_file(EXCEL_FILE, as_attachment=True, download_name='roster.xlsx')

if __name__ == '__main__':
    initialize_data()
    data = load_data()
    generate_excel(data)
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
