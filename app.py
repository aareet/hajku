from flask import Flask, render_template, request, redirect
import pymongo
import os
from bson import ObjectId
import json
import urllib
from datetime import datetime

app = Flask(__name__)

db = pymongo.MongoClient(os.getenv('MONGOHQ_URL')).hajkus

@app.route('/', methods=["GET"])
def write_hajku():
    return render_template("index.html")


@app.route('/submit', methods=["POST"])
def submit_hajku():
    if request.method == "POST":
        hajku = {}
        hajku["line1"] = request.form["line1"]
        hajku["line2"] = request.form["line2"]
        hajku["line3"] = request.form["line3"]
        hajku["created_on"] = datetime.utcnow()
        
        objectid = db.haikus.save(hajku)
        print str(objectid)

        return redirect("/view?hajku=%s" % str(objectid))

@app.route('/view', methods=["GET"])
def view_hajku():
    objid = request.args.get("hajku")

    return objid

if __name__ == '__main__':
    app.debug = True
    app.run()
