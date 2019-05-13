from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Toothpaste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    extract = db.Column(db.String(80), unique=True)

    def __init__(self, extract):
        self.extract = extract


class ToothpasteSchema(ma.Schema):
    class Meta:
        fields = 'extract',
        db.create_all()


toothpaste_schema = ToothpasteSchema()
toothpastes_schema = ToothpasteSchema(many=True)


@app.route("/user", methods=["POST"])
def add_user():
    extract = request.json['extract']

    new_toothpaste = Toothpaste(extract)

    db.session.add(new_toothpaste)
    db.session.commit()

    return toothpaste_schema.jsonify(new_toothpaste)


@app.route("/user", methods=["GET"])
def get_user():
    all_toothpastes = Toothpaste.query.all()
    result = toothpastes_schema.dump(all_toothpastes)
    return jsonify(result.data)


@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    toothpaste = Toothpaste.query.get(id)
    return toothpaste_schema.jsonify(toothpaste)


@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    toothpaste = Toothpaste.query.get(id)
    extract = request.json['extract']

    toothpaste.extract = extract

    db.session.commit()
    return toothpaste_schema.jsonify(toothpaste)


@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    toothpaste = Toothpaste.query.get(id)
    db.session.delete(toothpaste)
    db.session.commit()

    return toothpaste_schema.jsonify(toothpaste)


if __name__ == '__main__':
    app.run(debug=True)
