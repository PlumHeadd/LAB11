from flask import Flask, request, render_template

app = Flask(__name__)

# In-memory tasks list
tasks = []

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

@app.route('/', methods=['GET'])
def home():
    # Render the page with form and current list of tasks
    return render_template('index2.html', tasks=get_tasks())

@app.route('/add-task', methods=['POST'])
def add_new_task():
    task_description = request.form.get('task')
    if task_description:
        add_task(task_description)
    return render_template('index2.html', tasks=get_tasks())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
