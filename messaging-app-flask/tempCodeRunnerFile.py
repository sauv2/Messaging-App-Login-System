if 'user' in session:
        return redirect(url_for('mainpage', user=session['user']))