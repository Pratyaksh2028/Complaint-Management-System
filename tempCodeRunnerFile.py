from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime

app = Flask(__name__)
app.secret_key = 'bca_project_secret_key_2026' # Change this to any random string

# ==========================================
# DATABASE CONNECTION (UPDATED WITH YOUR PASS)
# ==========================================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sHINCHAn2028",  # Your specific password applied here
        database="cms_project_db"
    )

# Helper function to log activity for the 'activity-audit.html'
def log_activity(user_id, action, ip_address):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO activity_audit (user_id, action_details, ip_address) VALUES (%s, %s, %s)", 
                       (user_id, action, ip_address))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Logging error: {e}")

# ==========================================
# AUTHENTICATION DECORATORS
# ==========================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Administrator access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# AUTH ROUTES
# ==========================================

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('admin_dashboard') if session['role'] == 'admin' else url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Check password (handles plain text for the seed admin and hashed for new users)
        if user and (check_password_hash(user['password'], password) or (user['password'] == password and user['role'] == 'admin')):
            session['user_id'] = user['id']
            session['fullname'] = user['fullname']
            session['role'] = user['role']
            
            log_activity(user['id'], "User logged in", request.remote_addr)
            
            return redirect(url_for('admin_dashboard') if user['role'] == 'admin' else url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone', '')
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (fullname, email, password, phone) VALUES (%s, %s, %s, %s)", 
                           (fullname, email, hashed_password, phone))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error:
            flash('Email already exists.', 'error')
        finally:
            cursor.close()
            conn.close()
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_activity(session['user_id'], "User logged out", request.remote_addr)
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# ==========================================
# USER ROUTES
# ==========================================

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    complaints = cursor.fetchall()
    
    # Count stats for the dashboard
    cursor.execute("SELECT COUNT(*) as total FROM complaints WHERE user_id = %s", (session['user_id'],))
    total = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as resolved FROM complaints WHERE user_id = %s AND status = 'Resolved'", (session['user_id'],))
    resolved = cursor.fetchone()['resolved']
    
    cursor.close()
    conn.close()
    return render_template('dashboard.html', complaints=complaints, total=total, resolved=resolved)

@app.route('/add-complaint', methods=['GET', 'POST'])
@login_required
def add_complaint():
    if request.method == 'POST':
        category = request.form['category']
        subject = request.form['subject']
        description = request.form['description']
        priority = request.form.get('priority', 'Medium')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO complaints (user_id, category, subject, description, priority) VALUES (%s, %s, %s, %s, %s)",
                       (session['user_id'], category, subject, description, priority))
        conn.commit()
        log_activity(session['user_id'], f"Filed complaint: {subject}", request.remote_addr)
        cursor.close()
        conn.close()
        
        flash('Your complaint has been filed.', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('add-complaint.html')

# ==========================================
# ADMIN ROUTES
# ==========================================

@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, u.fullname 
        FROM complaints c 
        JOIN users u ON c.user_id = u.id 
        ORDER BY c.created_at DESC
    """)
    all_complaints = cursor.fetchall()
    
    # Simple stats for admin
    cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE status = 'Pending'")
    pending_count = cursor.fetchone()['count']
    
    cursor.close()
    conn.close()
    return render_template('admin-dashboard.html', complaints=all_complaints, pending_count=pending_count)

@app.route('/update-complaint/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_complaint(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        status = request.form['status']
        remark = request.form['admin_remark']
        cursor.execute("UPDATE complaints SET status = %s, admin_remark = %s WHERE id = %s", (status, remark, id))
        conn.commit()
        
        # Notify user
        cursor.execute("SELECT user_id FROM complaints WHERE id = %s", (id,))
        uid = cursor.fetchone()['user_id']
        cursor.execute("INSERT INTO notifications (user_id, message) VALUES (%s, %s)", 
                       (uid, f"Update on Complaint #{id}: Status is now {status}"))
        conn.commit()
        
        flash('Status updated.', 'success')
        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT c.*, u.fullname FROM complaints c JOIN users u ON c.user_id = u.id WHERE c.id = %s", (id,))
    complaint = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update-complaint.html', complaint=complaint)

# ==========================================
# ADDITIONAL UTILITIES
# ==========================================

@app.route('/activity-audit')
@admin_required
def activity_audit():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT a.*, u.fullname FROM activity_audit a LEFT JOIN users u ON a.user_id = u.id ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('activity-audit.html', logs=logs)

@app.route('/notifications')
@login_required
def notifications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    notifs = cursor.fetchall()
    cursor.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s", (session['user_id'],))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('notifications.html', notifications=notifs)

@app.route('/profile-settings', methods=['GET', 'POST'])
def profile_settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        new_name = request.form.get('fullname')
        # Update the database
        cursor.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_name, session['user_id']))
        conn.commit()
        # Update the session so the UI changes immediately
        session['user_name'] = new_name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile_settings'))

    # This part fixes the 'user is undefined' error
    cursor.execute("SELECT fullname, email FROM users WHERE id = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return render_template('profile-settings.html', user=user_data)

@app.route('/user-management')
def user_management():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all users from the database so the admin can see them
    cursor.execute("SELECT id, fullname, email, role, created_at FROM users")
    all_users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('user-management.html', users=all_users)

@app.route('/toggle-role/<int:user_id>')
def toggle_role(user_id):
    # Security: Only admins can access this
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check current role of the user being targeted
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    target_user = cursor.fetchone()

    if target_user:
        # Toggle: If admin -> make user | If user -> make admin
        new_role = 'admin' if target_user['role'] == 'user' else 'user'
        cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
        conn.commit()
        flash(f"User role updated to {new_role} successfully!", "success")

    cursor.close()
    conn.close()
    return redirect(url_for('user_management'))

@app.route('/system-reports')
def system_reports():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Count complaints by Status
    cursor.execute("SELECT status, COUNT(*) as count FROM complaints GROUP BY status")
    status_stats = cursor.fetchall()

    # 2. Count complaints by Category
    cursor.execute("SELECT category, COUNT(*) as count FROM complaints GROUP BY category")
    category_stats = cursor.fetchall()

    # 3. Total Users for the report header
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    return render_template('system-reports.html', 
                           status_stats=status_stats, 
                           category_stats=category_stats,
                           total_users=total_users)

if __name__ == '__main__':
    app.run(debug=True)