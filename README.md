# Quantitative Blackjack Simulator: Kelly Criterion & Risk Management (Wonging) 🎲📈

A Python-based, object-oriented Blackjack simulation for exploring card counting, edge-based bet sizing, bankroll trajectories, and risk-management strategies under configurable assumptions.

## Overview

Blackjack is a useful sandbox for quantitative analysis and stochastic processes. This project explores the trade-off between expected growth and bankroll risk through Monte Carlo simulation; it does not imply that any betting strategy can guarantee profits or eliminate the risk of bankruptcy.

By simulating a physical 6-deck shoe and tracking the Hi-Lo True Count, this simulator applies fractional Kelly mechanics and table-selection strategies ("Wonging") to visualize the chaotic nature of variance and the necessity of strict risk management.

## Key Features

*   **Object-Oriented Architecture:** Uses a scalable `CasinoShoe` class to accurately model physical deck mechanics, including deck penetration and cut-cards, rather than relying on infinite-deck assumptions.
*   **Card Counting (Hi-Lo System):** Dynamically tracks the Running Count and calculates the True Count to identify exact moments of positive mathematical expectation (+EV).
*   **Dynamic Bet Sizing (Kelly Criterion):** Implements a proportional betting algorithm that calculates the optimal wager based on the player's real-time edge, adjusting dynamically as the shoe progresses.
*   **Strategic Risk Management ("Wonging"):** The simulator intelligently back-counts (watches without betting) when the True Count drops below a profitable threshold, preventing the slow drain of forced minimum bets during negative-EV states.
*   **Bankroll Trajectory Visualization:** Utilizes `matplotlib` to plot actual account balance over thousands of hands, clearly illustrating drawdowns, volatility, and compound growth.

## The Mathematics & Strategy

### 1. The Shifting Edge
The baseline house edge under H17 rules is approximately **-0.72%**. As cards are drawn, the remaining composition of the deck changes. For every $+1$ increase in the True Count, the player's mathematical expectation increases by roughly **+0.50%**.

### 2. Bet Sizing via the Kelly Criterion

The implementation uses a simplified edge-based sizing rule:
$f^* = \\text{Edge}$
This is a modeling simplification, not a universal exact Kelly formula for Blackjack. A rigorous Kelly calculation depends on the payout structure and defensible estimates of player advantage and outcome variance. The simulator uses a **Half-Kelly** fraction to illustrate more conservative sizing; it still cannot prevent losses or drawdowns.

### 3. Risk of Ruin and Wonging
The simulator implements **Wonging** by pausing play when the True Count falls below the configured threshold (`-1.0`). This can reduce exposure to modeled negative-expectation situations, but it does **not** eliminate risk of ruin or guarantee positive returns. Outcomes depend on the rules, edge estimates, bankroll, betting constraints, shoe penetration, variance, and randomness. Treat charts as simulation results under the selected assumptions, not as real-world guarantees.

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
git clone https://github.com/AbdellahKah/BlackJack_MonteCarlo.git
cd BlackJack_MonteCarlo
\`\`\`

2. Run the simulation script:
\`\`\`bash
python simulator.py
\`\`\`

3. The script will output the final bankroll, total profit, the number of hands actually played versus watched, and generate a line chart showing your bankroll's trajectory.

## Customization

You can adjust the simulation parameters directly in the script to test different risk profiles:
*   `total_rounds`: Change the total number of casino rounds simulated.
*   `initial_bankroll`: Set your starting capital.
*   `penetration`: Adjust the cut-card placement in the `CasinoShoe` (default is 0.75 or 75%).
*   `true_count < -1.0`: Modify the Wonging threshold to test different entry/exit strategies.

## Author
**Abdellah Kahlaoui**

## License
This project is open-source and available under the MIT License.
