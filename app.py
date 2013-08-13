from flask import Flask, render_template, request, redirect
import pymongo
import os
from bson import ObjectId, json_util
import json
import urllib
from datetime import datetime

app = Flask(__name__)

db = pymongo.MongoClient(os.getenv('MONGOHQ_URL')).hajku


@app.route('/', methods=["GET"])
def write_hajku():
    return render_template("index.html")


@app.route('/submit', methods=["POST"])
def submit_hajku():
    if request.method == "POST":
        hajku = {}

        for line in ["line1", "line2", "line3"]:
            hajku[line] = str(request.form[line])

        hajku["created_on"] = datetime.utcnow()
        hajku["author"] = str(request.form["author"])
        hajku["title"] = str(request.form["title"])

        objectid = db.haikus.save(hajku)
        print str(objectid)

        return redirect("/view?hajku=%s" % str(objectid))


@app.route('/view', methods=["GET"])
def view_hajku():
    objid = request.args.get("hajku")

    myhaiku = db.haikus.find_one({"_id": ObjectId(objid)})
    if not myhaiku:
        return redirect("/")

    haiku = {}
    for line in ["line1", "line2", "line3"]:
        haiku[line] = myhaiku[line]
        print line

    haiku["author"] = myhaiku["author"] if "author" in myhaiku else None
    haiku["title"] = myhaiku["title"] if "title" in myhaiku else None

    return render_template("view.html", haiku=haiku)
    #return json.dumps(myhaiku, default=json_util.default)

if __name__ == '__main__':
    app.debug = True
    app.run()
