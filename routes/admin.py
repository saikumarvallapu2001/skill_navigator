@admin_bp.route('/add_college', methods=['POST'])
@login_required
@admin_required
def add_college():
    college_name = request.form.get('college_name')
    college_location = request.form.get('college_location')
    college_website = request.form.get('college_website')
    
    new_college = College(name=college_name, location=college_location, website=college_website)
    db.session.add(new_college)
    db.session.commit()
    
    flash('College added successfully!', 'success')
    return redirect(url_for('admin.manage_colleges')) 