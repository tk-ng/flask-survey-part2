from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def show_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)


@app.route("/questions/<int:num>")
def show_question(num):
    if num > len(satisfaction_survey.questions):
        flash("The Question ID does not exist in this questionnaire.")
        return redirect(f"/questions/{len(responses)}")
    if num < len(satisfaction_survey.questions) and num > len(responses):
        flash("You have not yet answered some of the previous questions.")
        return redirect(f"/questions/{len(responses)}")
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")
    elif num < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[num].question
        choices = satisfaction_survey.questions[num].choices
        return render_template("question.html", question=question, choices=choices)


@app.route("/answer", methods=["POST"])
def save_answer():
    answer = request.form['answer']
    responses.append(answer)
    return redirect(f"/questions/{len(responses)}")


@app.route("/thankyou")
def show_complete():
    return render_template("thankyou.html")
