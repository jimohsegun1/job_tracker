from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
# from models.job import Job
from app.models import Job
from app.models import db

job_bp = Blueprint('job', __name__)



@job_bp.route('/jobs')
@login_required
def view_jobs():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template('jobs.html', jobs=jobs)

@job_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_job():
    if request.method == 'POST':
        new_job = Job(
            title=request.form['title'],
            company=request.form['company'],
            date_applied=request.form['date_applied'],
            user_id=current_user.id
        )
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('job.view_jobs'))
    return render_template('add.html')

@job_bp.route('/edit/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('job.view_jobs'))
    if request.method == 'POST':
        job.title = request.form['title']
        job.company = request.form['company']
        job.date_applied = request.form['date_applied']
        db.session.commit()
        return redirect(url_for('job.view_jobs'))
    return render_template('edit.html', job=job)

@job_bp.route('/delete/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('job.view_jobs'))
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('job.view_jobs'))



# === REST API routes ===
@job_bp.route('/api/jobs', methods=['GET', 'POST'])
@jwt_required()
def api_jobs():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        jobs = Job.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': j.id,
            'title': j.title,
            'company': j.company,
            'date_applied': j.date_applied
        } for j in jobs])
    if request.method == 'POST':
        data = request.get_json()
        new_job = Job(title=data['title'], company=data['company'], user_id=user_id)
        db.session.add(new_job)
        db.session.commit()
        return jsonify({'message': 'Job created'}), 201

@job_bp.route('/api/jobs/<int:job_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def api_job_detail(job_id):
    user_id = get_jwt_identity()
    job = Job.query.filter_by(id=job_id, user_id=user_id).first()
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        job.title = data.get('title', job.title)
        job.company = data.get('company', job.company)
        db.session.commit()
        return jsonify({'message': 'Updated successfully'})

    if request.method == 'DELETE':
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})
