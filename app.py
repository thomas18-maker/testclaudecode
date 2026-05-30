from flask import Flask, render_template, request, redirect, url_for
import tasks

app = Flask(__name__)


@app.route("/")
def index():
    all_tasks = tasks.load_tasks()
    return render_template("index.html", tasks=all_tasks, priorities=tasks.PRIORITIES)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "medium")
    if title:
        tasks.add_task(title, priority)
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    tasks.complete_task(task_id)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    tasks.delete_task(task_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
