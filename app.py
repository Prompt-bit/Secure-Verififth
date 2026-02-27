from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

cats = [
    "https://cataas.com/cat?1",
    "https://cataas.com/cat?2",
    "https://cataas.com/cat?3",
    "https://cataas.com/cat?4"
]

not_cats = [
    "https://picsum.photos/id/1015/300/300",
    "https://picsum.photos/id/1025/300/300",
    "https://picsum.photos/id/1035/300/300",
    "https://picsum.photos/id/1045/300/300",
    "https://picsum.photos/id/1055/300/300",
    "https://picsum.photos/id/1065/300/300"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    chosen_cats = random.sample(cats, 3)
    chosen_others = random.sample(not_cats, 6)

    all_images = chosen_cats + chosen_others
    random.shuffle(all_images)

    correct_indexes = [
        i for i, img in enumerate(all_images)
        if img in chosen_cats
    ]

    session["correct"] = correct_indexes

    return jsonify({
        "images": all_images
    })

@app.route("/verify", methods=["POST"])
def verify():
    user_selected = request.json.get("selected", [])
    correct = session.get("correct", [])

    if sorted(user_selected) == sorted(correct):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True)