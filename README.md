# Quantitative Blackjack Simulator: Kelly Criterion & Risk of Ruin 🎲📈

A Python-based Object-Oriented numerical simulation of Blackjack designed to model card counting, dynamic bet sizing using the Kelly Criterion, and long-term bankroll trajectory. 

## Overview

While Blackjack is often viewed purely as a casino game, it serves as an excellent sandbox for quantitative analysis and stochastic processes. This project moves beyond simple Expected Value (EV) calculations to answer a fundamental question in quantitative finance: *How do you maximize compound growth while mathematically eliminating the risk of bankruptcy?*

By simulating a physical 6-deck shoe and tracking the Hi-Lo True Count, this simulator applies dynamic bet sizing using fractional Kelly mechanics to visualize the chaotic nature of variance and the necessity of strict risk management.

## Key Features

*   **Object-Oriented Architecture:** Uses a scalable `CasinoShoe` class to accurately model physical deck mechanics, including deck penetration and cut-cards, rather than relying on infinite-deck assumptions.
*   **Card Counting (Hi-Lo System):** Dynamically tracks the Running Count and calculates the True Count to identify exact moments of positive mathematical expectation (+EV).
*   **Dynamic Bet Sizing (Kelly Criterion):** Implements a proportional betting algorithm that calculates the optimal wager based on the player's real-time edge, adjusting dynamically as the shoe progresses.
*   **Bankroll Trajectory Visualization:** Utilizes `matplotlib` to plot actual account balance over thousands of hands, clearly illustrating drawdowns, volatility, and the "Risk of Ruin."
*   **Configurable Rule Sets:** Easily toggle between standard casino rules (e.g., Dealer Hits on Soft 17).

## The Mathematics

### 1. The Shifting Edge
The baseline house edge under H17 rules is approximately **-0.72%**. As cards are drawn, the remaining composition of the deck changes. For every $+1$ increase in the True Count, the player's mathematical expectation increases by roughly **+0.50%**.

### 2. The Kelly Criterion
To maximize the logarithm of wealth during +EV situations, the simulator calculates the optimal bet fraction $f^*$ using a simplified Kelly formula:

$$f^* = \text{Edge}$$

Because Full Kelly is aggressively volatile and practically guarantees massive drawdowns in noisy environments, the simulation uses a **Half-Kelly** strategy ($f^* / 2$) to smooth out variance and protect the bankroll from statistical anomalies.

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
git clone https://github.com/yourusername/blackjack-kelly-simulator.git
cd blackjack-kelly-simulator
\`\`\`

2. Run the simulation script:
\`\`\`bash
python simulator.py
\`\`\`

3. The script will output the final bankroll, total profit, and generate a line chart showing your bankroll's trajectory over the simulated hands.

## Customization

You can adjust the simulation parameters directly in the script to test different risk profiles:
*   `hands`: Change the total number of hands simulated (default is 50,000).
*   `initial_bankroll`: Set your starting capital.
*   `penetration`: Adjust the cut-card placement in the `CasinoShoe` (default is 0.75 or 75%).
*   `calculate_kelly_bet()`: Modify the Kelly fraction (e.g., change from Half-Kelly to Quarter-Kelly for lower variance).

## Author
**Abdellah Kahlaoui**

## License
This project is open-source and available under the MIT License.
