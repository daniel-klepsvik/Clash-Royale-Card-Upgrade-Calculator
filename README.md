# 👑 Clash Royale Card Upgrade Calculator

A Python tool that connects to the official **Clash Royale API** to calculate exactly how many levels you can upgrade a card based on your current inventory and the **Total Gold Cost** required.

## ✨ Features
- **2026 Economy Ready:** Updated with Level 16 costs and post-Elite Wild Card logic.
- **Smart Level Normalization:** Converts internal API levels to the standard in-game display (1–16).
- **Progress Tracking:** Shows your current card count vs. the total goal for the next level.
- **Secure:** Uses environment variables (`.env`) to keep your API keys private.

## 📁 Project Structure
```text
.
├── main.py              # Core logic & API interaction
├── .env                 # (Private) API Key & Player Tag
├── .env.example         # Template for setting up keys
├── .gitignore           # Prevents sensitive files from being uploaded
├── requirements.txt     # List of required Python libraries
└── README.md            # Project documentation