# Decision Efficiency Index (DEI) Project

This project demonstrates a simple system to calculate and visualize the Decision Efficiency Index (DEI). It consists of a FastAPI backend for calculations and data storage, and a Nuxt 4 frontend for user interaction and analytics.

![Quick Demo](https://iili.io/fKg8sTJ.md.png "DEI Demo")

## How it works

1.  **Home Page**: You enter three parameters:
    *   **Decision Time**: How long it took to make a decision.
    *   **Error Rate**: The probability of error (0 to 1).
    *   **Robustness Score**: A score representing the resilience of the decision.
    
    When you click "Run DEI Test", the backend calculates the score using the formula:
    `DEI = (1 / decision_time) * (1 - error_rate) * robustness_score`

2.  **Analytics Page**: This page visualizes the history of your tests.
    *   **Line Chart**: Shows how your DEI score changes over time.
    *   **Bar Chart**: Compares the Robustness Score and Error Rate for each test.

## Tech Stack

*   **Backend**: Python, FastAPI
*   **Frontend**: Vue.js, Nuxt 4, TailwindCSS v4, Chart.js

## Running the Project

1.  **Backend**:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```

2.  **Frontend**:
    ```bash
    cd frontend
    pnpm install
    pnpm dev
    ```

Open your browser at `http://localhost:3000` to use the app.
