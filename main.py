from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#Create flask instance
app = Flask(__name__)

#Configure the SQLAlchemy for the application
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:Flint346297@localhost/todo_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initialize SQLAlchemy object
db = SQLAlchemy(app)

#Todo model
class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default = False, nullable = False)

    #Method that will turn the Todo model into a dict so its easier to turn to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
            }


#default route
@app.route("/")
def home():
    return "Home Page"


#HTTP Method Routes
# GET POST PUT DELETE

#Create new to do list item
@app.route("/todos", methods=["POST"])
def create_todo():

    #get the user data
    data = request.get_json()

    #create new todo using the Todo model with the data from the user
    #.get function is a dictionary function that returns the value of a key if it exists
    new_todo = Todo(
        title = data["title"],
        description = data.get("description", ""),
        completed = data.get("completed", False)
    )
        
    #add the todo in the database then commit the changes
    db.session.add(new_todo)
    db.session.commit()

    #201 is the status code for successfully created
    return jsonify({"message": "Todo created successfully", "todo": new_todo.to_dict()}), 201


#Get all the todos
@app.route("/todos", methods=["GET"])
def get_todos():

    #Query all the todos 
    todos = Todo.query.all()

    #return each todo in the list
    #200 is the status code for successful retrieval "OK"
    return jsonify([todo.to_dict() for todo in todos]), 200


#Get a specific todo 
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):

    #Query to find the todo with the id
    todo = Todo.query.get(todo_id)

    #If the todo is found, return it
    #If not, return a corresponding message
    if todo:
        return jsonify(todo.to_dict()), 200
    else:
        #404 is the status code for not found
        return jsonify({"error": "Todo not found"}), 404


#Update a specific todo
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):

    #Collect data
    data = request.get_json()

    #Query to find the todo
    todo = Todo.query.get(todo_id)

    if todo:
        todo.title = data.get("title", todo.title)
        todo.description = data.get("description", todo.description)
        todo.completed = data.get("completed", todo.completed)

        db.session.commit()
        return jsonify({"message": "Todo updated successfully", "todo": todo.to_dict()}), 200

    return jsonify({"error": "Todo not found"}), 404


#Delete a specific todo
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    
    #Query to find the todo with the id
    todo = Todo.query.get(todo_id)

    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Todo deleted successfully"}), 200

    return jsonify({"error": "Todo not found"}), 404


#Runs only when the script is run directly
if __name__ == "__main__":
    app.run(debug=True)
  