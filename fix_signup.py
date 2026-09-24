filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''        if db.users.find_one({"email": email}):
            flash("Email already registered.", "error")
            return redirect(url_for('signup'))'''

new_code = '''        try:
            if db.users.find_one({"email": email}):
                flash("Email already registered.", "error")
                return redirect(url_for('signup'))
        except Exception as e:
            flash("Database connection failed. Please check your internet or whitelist your IP in MongoDB Atlas.", "error")
            return redirect(url_for('signup'))'''

content = content.replace(old_code, new_code)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
