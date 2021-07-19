import json
import datetime

__package__ = None

def load(filename):

    try:
        with open (filename) as f:
            db = json.load(f)

            return db
    except:
        print("File does not exist")
        

def get_project_count(db):
    sum = 0
    for project in db:
        sum += 1
    return sum


def get_project(db, id):

    for project in db:
        if id == project["project_id"]:
            return project
    return None


def search(db, sort_by="start_date", sort_order="desc", techniques=None, search=None, search_fields=None):

    result_list = []

    if search != None:
        if search_fields != None:
            for project in db:
                for field in search_fields:
                    if search.casefold() in str(project[field]).casefold():
                        result_list.append(project)
                        break
        else:
            for project in db:
                for field in project.values():
                    if search in str(field):
                        result_list.append(project)
                        break
    else:
        result_list = db

    if techniques != None:

        for tech in techniques:
            result_list = [project for project in result_list if tech in project["techniques_used"]]
            
    
    if sort_order == "desc":
        order_l = True
    else:
        order_l = False
        
    if sort_by == "start_date" or sort_by == "end_date":
        i = lambda x : datetime.datetime.strptime(x[sort_by], "%Y-%m-%d")
        result_list = sorted(result_list, reverse = order_l, key=i)

    else:
        result_list = sorted(result_list, reverse = order_l, key=lambda x : x[sort_by])
    
    return result_list

    

def get_techniques(db):

    tech_list = []

    for project in db:
        for technique in project["techniques_used"]:
            if technique not in tech_list:
                tech_list.append(technique)

    sorted_tech_list = sorted(tech_list, key=str.lower)

                
    return sorted_tech_list
    

def get_technique_stats(db):

    tech_dict = {}

    techniques = get_techniques(db)

    for tech in techniques:
        tech_dict[tech] = []
        for project in db:
            if tech in project["techniques_used"]:
                tech_dict[tech].append({"id" : project["project_id"], "name" : project["project_name"]})

    return tech_dict
                                    


