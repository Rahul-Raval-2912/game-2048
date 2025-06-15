# 2048 Game

A web-based 2048 game built with **Flask**, **HTML**, **CSS**, and **JavaScript**. Slide tiles to merge numbers and reach 2048, with support for keyboard, mouse wheel, and touch swipe inputs.

> 🔗 **GitHub Repository:** [2048 Game](https://github.com/Rahul-Raval-2912/2048)

---

## Table of Contents

- Features
- Tech Stack
- Project Structure
- Prerequisites
- Installation
- Usage
- Contributing
- License

---

## Features

- **Interactive Gameplay:** Slide tiles using arrow keys, mouse wheel, or swipe gestures.
- **Animations:** Smooth tile movements with CSS transitions.
- **High Scores:** Saves and displays top 5 high scores.
- **Sound Effects:** Plays a sound on victory or game over (optional).
- **Responsive Design:** Works on both desktop and mobile browsers.

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Storage:** JSON for high scores

---

## Project Structure

```bash
2048_game/
├── app.py              # Flask backend
├── static/
│   ├── style.css       # CSS for styling
│   ├── game.js         # JavaScript for game logic
│   └── sound.mp3       # Optional sound effect
├── templates/
│   └── index.html      # HTML template
└── high_scores.json    # High scores storage
```

---

## Prerequisites

- **Python** (v3.6+), **pip**
- A modern web browser (e.g., Chrome, Firefox)

---

## Installation

- Clone the repo:
  ```bash
  git clone https://github.com/Rahul-Raval-2912/2048.git
  ```
- Navigate to the directory:
  ```bash
  cd 2048_game
  ```
- Install dependencies:
  ```bash
  pip install flask
  ```
- Run the game:
  ```bash
  python app.py
  ```

---

## Usage

- Open your browser and go to `http://127.0.0.1:5000`.
- Play using:
  - **Desktop:** Arrow keys or mouse wheel.
  - **Mobile:** Swipe gestures.
- Click "Reset Game" to start over.
- High scores are displayed below the board.

---

## Contributing

- Fork the repo.
- Create a branch (`git checkout -b feature/your-feature`).
- Commit changes (`git commit -m "Add feature"`).
- Push branch (`git push origin feature/your-feature`).
- Open a Pull Request.

---

## License

MIT License. See [LICENSE](LICENSE) file.