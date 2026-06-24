import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import db, LasbcaEntry

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lasbca_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
with app.app_context():
    db.create_all()
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to handle secure file saving
def save_uploaded_file(file_field_name):
    file = request.files.get(file_field_name)
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        # Unique timestamp can be added here if files share identical names
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None

@app.route('/add', methods=['GET', 'POST'])
def add_info():
    if request.method == 'POST':
        # Grab text inputs via matching HTML "name" tags
        cn_data = request.form.get('cn')
        address_data = request.form.get('address')
        contravention_data = request.form.get('contravention')
        action_data = request.form.get('action_taken')
        
        # Process and save both files independently
        pic1 = save_uploaded_file('picture_1')
        pic2 = save_uploaded_file('picture_2')

        # Insert record into database
        new_record = LasbcaEntry(
            cn=cn_data,
            address=address_data,
            contravention=contravention_data,
            action_taken=action_data,
            picture_1_filename=pic1,
            picture_2_filename=pic2
        )
        db.session.add(new_record)
        db.session.commit()
        
        return redirect(url_for('admin_dashboard'))

    return render_template('input.html')

@app.route('/dashboard')
def admin_dashboard():
    all_logs = LasbcaEntry.query.order_by(LasbcaEntry.id.desc()).all()
    return render_template('view.html', database_entries=all_logs)

if __name__ == '__main__':
    app.run(debug=True)
