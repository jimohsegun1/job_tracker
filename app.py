from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory job storage
jobs = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        date_applied = request.form['date_applied']
        jobs.append({
            'title': title,
            'company': company,
            'date_applied': date_applied
        })
        return redirect(url_for('view_jobs'))
    return render_template('add.html')

@app.route('/jobs')
def view_jobs():
    return render_template('jobs.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
