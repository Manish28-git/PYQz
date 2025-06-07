import os
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, send_from_directory, current_app
)
from werkzeug.utils import secure_filename
from .models import Paper
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    q = request.args.get('q', '').strip()
    if q:
        papers = Paper.query.filter(
            Paper.title.ilike(f'%{q}%') |
            Paper.subject.ilike(f'%{q}%') |
            Paper.academic_year.ilike(f'%{q}%')
        ).order_by(Paper.academic_year.desc(), Paper.uploaded_at.desc()).all()
    else:
        papers = Paper.query.order_by(Paper.academic_year.desc(), Paper.uploaded_at.desc()).all()

    papers_by_year = {}
    for p in papers:
        papers_by_year.setdefault(p.academic_year, []).append(p)

    return render_template('index.html', papers_by_year=papers_by_year, q=q)

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    years = [f"{y-1}-{y}" for y in range(2018, 2026)]
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subject = request.form.get('subject', '').strip()
        academic_year = request.form.get('academic_year')
        file = request.files.get('file')

        if not (title and subject and academic_year and file):
            flash('All fields are required.', 'danger')
            return redirect(request.url)
        if not file.filename.lower().endswith('.pdf'):
            flash('Only PDF files allowed.', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        year_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], academic_year)
        os.makedirs(year_folder, exist_ok=True)
        file.save(os.path.join(year_folder, filename))

        paper = Paper(
            title=title,
            subject=subject,
            academic_year=academic_year,
            filename=filename
        )
        db.session.add(paper)
        db.session.commit()
        flash('Paper uploaded successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('upload.html', years=years)

@main.route('/download/<academic_year>/<filename>')
def download(academic_year, filename):
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], academic_year)
    return send_from_directory(folder, filename, as_attachment=True)

@main.route('/delete/<int:paper_id>', methods=['POST'])
def delete_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], paper.academic_year, paper.filename)
    try:
        if os.path.exists(path):
            os.remove(path)
        db.session.delete(paper)
        db.session.commit()
        flash('Paper deleted.', 'success')
    except Exception as e:
        flash(f'Error deleting paper: {e}', 'danger')
    return redirect(url_for('main.index'))
