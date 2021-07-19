#!/usr/bin/env python3

import data
import flask
from flask import render_template, request, redirect, url_for
app = flask.Flask("projektportfolio")
previous_search = {"sort_by" : "start_date", "selected_techniques" : [], "search" :"", "selected_search_fields" : [], "sort_order" : "desc"}



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list/", methods=["GET", "POST"])
def p_list():
    db = data.load("data.json")
    techs = data.get_techniques(db)
    field_list = ["start_date", "end_date", "course_name", "group_size", "academic_credits", "project_name", "course_id", "project_id"]
    order_list = ["ascending", "descending"]
    global previous_search
    field_search = None

    if request.args.get("search") != None:
        previous_search["search"]  = request.args.get("search", default="")

    if request.args.get("field") != None :
        previous_search["sort_by"] = request.args.get("field")

    if request.args.get("order") != None :
        previous_search["sort_order"] = request.args.get("order")
        print(previous_search["sort_order"])

    if request.method == "POST":
        previous_search["selected_techniques"] = request.form.getlist("tech")
        previous_search["selected_search_fields"] = request.form.getlist("search_field")

    if previous_search["selected_search_fields"] == [] :
        field_search = None
    else:
        field_search = previous_search["selected_search_fields"]

    found = data.search(db,
                        search=previous_search["search"],
                        sort_by=previous_search["sort_by"],
                        techniques = previous_search["selected_techniques"],
                        search_fields = field_search,
                        sort_order=previous_search["sort_order"])

    return render_template("projekt.html",
                           techniques=techs,
                           projects = found,
                           fields = field_list,
                           orders = order_list,
                           search = previous_search["search"],
                           checked_tech = previous_search["selected_techniques"],
                           checked_field = previous_search["sort_by"],
                           checked_search_fields = previous_search["selected_search_fields"],
                           checked_order = previous_search["sort_order"])


@app.route("/techniques/", methods=["GET","POST"])
def technique():
    db = data.load("data.json")
    techs = data.get_techniques(db)
    checked_tech=[]
    if request.method == "POST":
        checked_tech= request.form.getlist("tech")

    found = data.search(db, techniques = checked_tech)
    return render_template("techniques.html", projects = found, techniques=techs, checked_tech = request.form.getlist("tech"))

@app.route("/project/<int:proj_id>/")
def id_page(proj_id):
    db = data.load("data.json")
    project_valid = data.get_project(db,proj_id)
    if project_valid:
        return render_template("project_template.html", project = data.get_project(db,proj_id))
    else:
        return render_template("error.html", false_id = proj_id),404
