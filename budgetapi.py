from flask import Flask, Request, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from sqlalchemy.engine import result
from flask_migrate import Migrate, MigrateCommand
from config import Config
import json



app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)




class BudgetItem(db.Model):
    __tablename__ = "budget"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(400), nullable=True)
    lineitems = db.relationship('LineItem', backref='budget')

    def __repr__(self):
        return f'{self.budget_name}'


class LineItem(db.Model):
    __tablename__ = "lineitem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.String(50), nullable=False)
    percent_of_total = db.Column(db.String(50), nullable=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)

    def __repr__(self):
        return f'{self.name} -- {self.cost}'


class LineItemSchema(ma.Schema):
    class Meta:
        model = LineItem
        fields = ('id', 'name', 'cost', 'percent_of_total', 'budget_id')


class BudgetSchema(ma.Schema):
    class Meta:
        model = BudgetItem
        fields = ('id', 'budget_name', 'description')


budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)

line_item_schema = LineItemSchema()
line_items_schema = LineItemSchema(many=True)


@app.route('/api/budgetitems', methods=['GET', 'POST'])
def budget_list():
    if request.method == 'GET':
        all_budgets = BudgetItem.query.all()
        result = budgets_schema.dump(all_budgets)
        return jsonify(result)

    elif request.method == 'POST':
        req_data = json.loads(request.data)
        name = req_data['budget_name']
        description = req_data['description']

        new_budget_item = BudgetItem()
        new_budget_item.budget_name = name
        new_budget_item.description = description

        db.session.add(new_budget_item)
        db.session.commit()
        return budget_schema.jsonify(new_budget_item)


@app.route('/api/budgetitems/<int:budget_id>', methods=['GET', 'PUT', 'DELETE'])
def budget_details(budget_id):
    if request.method == 'GET':
        budget = BudgetItem.query.get_or_404(budget_id)
        line_items = LineItem.query.filter_by(budget_id=budget_id)
        serialize_budget = budget_schema.dump(budget)
        serialize_line_item = line_items_schema.dump(line_items)
        serialize_budget['lineitems'] = serialize_line_item
        return jsonify(serialize_budget)

    elif request.method == 'PUT':
        budget = BudgetItem.query.get_or_404(budget_id)
        req_data = json.loads(request.data)

        if 'budget_name' in req_data:
            budget.budget_name = req_data['budget_name']

        if 'description' in req_data:
            budget.description = req_data['description']

        db.session.commit()
        return budget_schema.jsonify(budget)

    elif request.method == 'DELETE':
        budget = BudgetItem.query.get_or_404(budget_id)
        line_items = LineItem.query.filter_by(budget_id=budget_id)
        for item in line_items:
            db.session.delete(item)
            db.session.commit()
        db.session.delete(budget)
        db.session.commit()
        return '', 204


@app.route('/api/lineitems', methods=['GET', 'POST'])
def line_item_list():
    if request.method == 'GET':
        all_line_items = LineItem.query.all()
        result = line_items_schema.dump(all_line_items)
        return jsonify(result)
    elif request.method == 'POST':
        req_data = json.loads(request.data)
        new_line_item = LineItem()
        new_line_item.name = req_data['name']
        new_line_item.cost = req_data['cost']
        new_line_item.percent_of_total = req_data['percent_of_total']
        new_line_item.budget_id = req_data['budget_id']
        db.session.add(new_line_item)
        db.session.commit()
        return line_item_schema.jsonify(new_line_item)



@app.route('/api/lineitems/<int:line_item_id>', methods=['GET', 'PUT', 'DELETE'])
def line_item_details(line_item_id):
    if request.method == 'GET':
        line_item = LineItem.query.get_or_404(line_item_id)
        line_item_json = line_item_schema.dump(line_item)
        print(line_item_json)
        return jsonify(line_item_json)

    elif request.method == 'PUT':
        line_item = LineItem.query.get_or_404(line_item_id)
        req_data = json.loads(request.data)

        if 'name' in req_data:
            line_item.name = req_data['name']
        if 'cost' in req_data:
            line_item.cost = req_data['cost']
        if 'percent_of_total' in req_data:
            line_item.percent_of_total = req_data['percent_of_total']
        if 'budget_id' in req_data:
            line_item.budget_id = req_data['budget_id']

        db.session.commit()
        return line_item_schema.jsonify(line_item)

    elif request.method == 'DELETE':
        line_item = LineItem.query.get_or_404(line_item_id)
        db.session.delete(line_item)
        db.session.commit()
        return '', 204



admin = Admin(app, name='Budget Items Admin', template_mode='bootstrap3')
admin.add_view(ModelView(BudgetItem, db.session))
admin.add_view(ModelView(LineItem, db.session))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
