from flask import Flask, jsonify

import os
import io
import json
from flask import Flask, render_template, request, url_for

common = {
    'first_name': 'Joel',
    'last_name': 'Soto'
}

@app.route('/')
def index():
    return render_template('home.html', common=common)

@app.route('/projects') 
def projects():
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', common=common, projects=data, tag=tag)

@app.route('/reading')
def reading():
    data = get_static_json("static/files/reading.json")
    return render_template('reading.html', common=common, data=data)


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', common=common)


def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', common=common), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))
    
    

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
