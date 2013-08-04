from flask import Flask, render_template, request
import pymongo
import os
from bson import ObjectId
app = Flask(__name__)

db = pymongo.MongoClient(os.getenv('MONGOHQ_URL'))

@app.route('/', methods=["GET"])
def write_hajku():
    return render_template("index.html")

@app.route('/submit', methods=["POST"])
def submit_hajku():
    hajku = []
    if request.method == "POST":
         hajku["line1"] = request.form["line1"]
         hajku["line2"] = request.form["line2"]
         hajku["line3"] = request.form["line3"]

         respo = db.hajkus.save(hajku)
         return respo

@app.route('/view', methods=["GET"])
def view_hajku():
    objid = request.args.get("hajku")
 


if __name__ == '__main__':
    app.run()
