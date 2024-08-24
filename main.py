from flask import Flask, request, jsonify

app = Flask(__name__)

#In memory list to store todo items
todos = []

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

    todo_id = len(todos) + 1

    #create new todo with the data from the user
    #.get function is a dictionary function that returns the value of a key if it exists
    #if the key doesn't exist then it returns the second thing you put in
    #the title of a todo is mandatory, so it will always exist so you don't need the .get function
    new_todo = {
        "id": todo_id,
        "title": data["title"],
        "description": data.get("description", " "),
        "completed": data.get("completed", False)
    }

    #append the todo onto the list
    todos.append(new_todo)

    #201 is the status code for successfully created
    return jsonify({"message": "Todo created successfully", "todo": new_todo}), 201


#Get all the todos
@app.route("/todos", methods=["GET"])
def get_todos():

    #200 is the status code for successful retrieval "OK"
    return jsonify(todos), 200


#Get a specific todo 
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):

    todo = None

    #Iterate through the todo list to find the matching todo
    for item in todos:
        if item["id"] == todo_id:
            todo = item
            break
    
    #If the todo is found, return it
    #If not, return a corresponding message
    if todo:
        return jsonify(todo), 200
    else:
        #404 is the status code for not found
        return jsonify({"error": "Todo not found"}), 404


#Update a specific todo
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):

    todo = None

    #Iterate through the list to find the todo needed to be updated
    for item in todos:
        if item["id"] == todo_id:
            todo = item
            break
    
    if todo:

        #Collect the data from the user
        data = request.get_json()

        #Update the todo, if the key wasn't updated, keep the value the same
        todo["title"] = data.get("title", todo["title"])
        todo["description"] = data.get("description", todo["description"])
        todo["completed"] = data.get("completed", todo["completed"])

        return jsonify({"message": "Todo updated successfully", "todo": todo}), 200
    else:
        return jsonify({"error": "Todo not found"}), 404



#Delete a specific todo
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    
    #Declare the todos variable global so it is accessible within the function
    global todos

    #create a new todos list, that will hold all the todos except the one to be deleted
    new_todos = []

    #Iterate through the current todos, add all the ones except the deleted one to the new_todos
    for todo in todos:
        if todo["id"] != todo_id:
            new_todos.append(todo)
    
    #Update the current list
    todos = new_todos

    #return the appropriate message
    return jsonify({"message": "Todo deleted successfully"}), 200


#Runs only when the script is run directly
if __name__ == "__main__":
    app.run(debug=True)
  