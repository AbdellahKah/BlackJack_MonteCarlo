# Blackjack Monte Carlo Simulator 🎲📉

A Python-based numerical simulation of Blackjack designed to visualize the Law of Large Numbers, calculate Expected Value (EV), and analyze the statistical impact of casino rule variations.

## Overview

While Blackjack is often viewed purely as a game of chance, it is fundamentally a sequential decision-making problem under uncertainty. This project uses Monte Carlo methods to simulate millions of hands, demonstrating how short-term variance eventually converges to the theoretical mathematical expectation (the "house edge"). 

Developed as an applied mathematics exploration into stochastic processes and probability distributions, this simulator allows users to test how specific rule changes—such as the dealer hitting on a Soft 17—shift the statistical baseline.

## Features

*   **High-Volume Simulation:** Capable of running 1,000,000+ iterations efficiently to demonstrate mathematical convergence.
*   **Basic Strategy Heuristics:** Implements an optimized decision matrix for player actions (Hit, Stand) based on the dealer's upcard.
*   **Configurable Rule Sets:** Easily toggle between standard casino rules (e.g., S17 - Dealer Stands on all 17s vs. H17 - Dealer Hits on Soft 17).
*   **Data Visualization:** Utilizes `matplotlib` to plot the running Expected Value, clearly illustrating the transition from high initial variance to long-term mathematical certainty.

## The Mathematics

The simulator models a discrete-time random walk where the player's bankroll fluctuates based on hand outcomes. By employing an infinite shoe model (drawing with replacement) and basic strategy, the simulation proves that the Expected Value $E[X]$ converges to approximately **-0.50%** under standard rules, and drops to **-0.72%** when the H17 rule is introduced.

## Requirements

*   Python 3.x
*   `matplotlib`

To install the required dependencies, run:
\`\`\`bash
pip install matplotlib
\`\`\`

## Usage

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/blackjack-monte-carlo.git
cd blackjack-monte-carlo
\`\`\`

2. Run the simulation script:
\`\`\`bash
python simulator.py
\`\`\`

3. The script will output the final Expected Value percentage in the console and generate a line chart showing the EV convergence over the simulated hands.

## Customization

You can adjust the simulation parameters directly in the script:
*   `iterations`: Change the total number of hands simulated (default is 1,000,000).
*   `play_dealer()`: Modify the dealer logic to test different casino conditions (e.g., modifying the Soft 17 check).

## Author
**Abdellah Kahlaoui**

## License
This project is open-source and available under the MIT License.
