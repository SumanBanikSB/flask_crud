import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import CreateForm, UpdateForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '165486481641d68ae4sfe68a5f4c68edf4'

client = MongoClient("mongodb+srv://suman33banik:LlnpSsCmmU4rxlC5@cluster0.uindrbg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.my_database
collection = db.my_collection

@app.route('/')
def index():
    documents = list(collection.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return render_template('index.html', documents=documents)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        print("Form is valid!!")
        data = {"name": form.name.data, "age": form.age.data}
        result = collection.insert_one(data)
        flash('Document created successfully', 'success')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/read', methods=['GET'])
def read_all():
    documents = list(collection.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return jsonify(documents), 200

@app.route('/read/<id>', methods=['GET'])
def read_one(id):
    document = collection.find_one({"_id": ObjectId(id)})
    if document:
        document["_id"] = str(document["_id"])
        return jsonify(document), 200
    return jsonify({"error": "Document not found"}), 404

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    document = collection.find_one({"_id": ObjectId(id)})
    if not document:
        flash('Document not found', 'danger')
        return redirect(url_for('index'))
    
    form = UpdateForm()
    if form.validate_on_submit():
        data = {"name": form.name.data, "age": form.age.data}
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count:
            flash('Document updated successfully', 'success')
            return redirect(url_for('index'))
        flash('Document not found', 'danger')

    form.name.data = document["name"]
    form.age.data = document["age"]
    return render_template('update.html', form=form, document_id=id)

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        flash('Document deleted successfully', 'success')
    else:
        flash('Document not found', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
