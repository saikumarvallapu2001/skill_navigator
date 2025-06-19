from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Interlist
from extensions import db
from sqlalchemy import distinct

user = Blueprint('user', __name__)

@user.route('/search-colleges')
@login_required
def user_search_colleges():
    # Get filter parameters
    state = request.args.get('state', '')
    district = request.args.get('district', '')
    stream = request.args.get('stream', '')
    college_type = request.args.get('college_type', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query
    query = Interlist.query

    # Apply filters
    if state:
        query = query.filter(Interlist.State_name == state)
    if district:
        query = query.filter(Interlist.District_Name == district)
    if stream:
        query = query.filter(Interlist.Stream == stream)
    if college_type:
        query = query.filter(Interlist.College_Nature_Type == college_type)

    # Get unique values for filters
    states = db.session.query(distinct(Interlist.State_name)).order_by(Interlist.State_name).all()
    states = [state[0] for state in states if state[0]]

    districts = []
    if state:
        districts = db.session.query(distinct(Interlist.District_Name))\
            .filter(Interlist.State_name == state)\
            .order_by(Interlist.District_Name).all()
        districts = [district[0] for district in districts if district[0]]

    streams = db.session.query(distinct(Interlist.Stream)).order_by(Interlist.Stream).all()
    streams = [stream[0] for stream in streams if stream[0]]

    college_types = db.session.query(distinct(Interlist.College_Nature_Type))\
        .order_by(Interlist.College_Nature_Type).all()
    college_types = [type[0] for type in college_types if type[0]]

    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    colleges = pagination.items

    return render_template('user/college_search.html',
                         colleges=colleges,
                         pagination=pagination,
                         states=states,
                         districts=districts,
                         streams=streams,
                         college_types=college_types,
                         selected_state=state,
                         selected_district=district,
                         selected_stream=stream,
                         selected_type=college_type)

@user.route('/api/districts/<state>')
@login_required
def get_districts(state):
    districts = db.session.query(distinct(Interlist.District_Name))\
        .filter(Interlist.State_name == state)\
        .order_by(Interlist.District_Name).all()
    return jsonify([district[0] for district in districts if district[0]])

@user.route('/discover-skills')
@login_required
def user_discover_skills():
    return render_template('user/discover_skills.html') 