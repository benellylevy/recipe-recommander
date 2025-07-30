# 🍲 Recipe Recommender Web App

An intelligent recipe suggestion tool that matches your mood, your pantry and your diet.

-----

## What does this project do?

The Recipe Recommender is a user-friendly web application that helps users discover creative and personalized recipe suggestions based on:
	•	✅ Three fresh ingredients the user currently has
	•	✅ Dietary preferences (e.g. Vegan)
	•	✅ Preferred cuisine (e.g. Japanese, Italian, Indian)
	•	✅ Dietary intolerances (e.g. Gluten, Dairy, Peanut)

The app connects in real-time to a public recipe API (Spoonacular) and fetches 5–10 relevant recipe candidates. It then intelligently filters and ranks them according to how many of the recipe’s required ingredients the user already has at home.

Users receive a list of top 3 matching recipes — each with a preview image, link to instructions, and an ingredient breakdown:
✔️ What you already have, ❌ what you’re missing.

Users can save favorites to a persistent list and remove them later.

----

## 📥 What input does it expect?

The user provides:
	•	Three manually typed ingredients (e.g. "tomato", "pasta", "onion")
	•	Dietary preference (checkbox: Vegan / Not vegan)
	•	Preferred cuisine (dropdown: e.g. “Japanese”, “Mexican”)
	•	Dietary intolerances (checkbox list: e.g. gluten, dairy, soy)

All inputs are collected via an elegant and responsive web form.

----

## 📤 What output does it return?

After submitting the form, the user receives:
	•	A ranked list of 3 recipe suggestions
	•	✅ Title, image, external recipe link
	•	Option to add recipes to “Favorites”
	•	Option to remove recipes from “Favorites”
	•	Separate page to browse favorite recipes


## Technicalities: How to run it


## ⚙️ How to run the project locally

1. Clone the repository:

```bash
git clone https://github.com/yourusername/recipe-recommender.git
cd recipe-recommender
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Spoonacular API key:

```
SPOONACULAR_API_KEY=your_api_key_here
```

5. Run the app:

```bash
python app.py
```

Then go to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 🎓 Academic note

This project was developed as part of 
Instructor: Liron Shapira
