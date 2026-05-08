import random
import matplotlib.pyplot as plt

class CasinoShoe:
    def __init__(self, num_decks=6, penetration=0.75):
        self.num_decks = num_decks
        self.penetration = penetration
        self.cards = []
        self.running_count = 0
        self.shuffle()
        
    def shuffle(self):
        # 4 suits of 2-10, plus 3 face cards (10), plus Aces (11)
        self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * self.num_decks
        random.shuffle(self.cards)
        self.running_count = 0
        
    def draw(self):
        card = self.cards.pop()
        # Update Hi-Lo Running Count
        if card in [2, 3, 4, 5, 6]:
            self.running_count += 1
        elif card in [10, 11]:
            self.running_count -= 1
        return card
        
    def get_true_count(self):
        # Prevent division by zero near the very end of a shoe
        remaining_decks = max(0.5, len(self.cards) / 52)
        return self.running_count / remaining_decks
        
    def needs_shuffle(self):
        # Shuffle when we hit the cut card
        cut_card_threshold = 52 * self.num_decks * (1 - self.penetration)
        return len(self.cards) < cut_card_threshold


def calculate_total(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def play_dealer(dealer_hand, shoe):
    while True:
        total = calculate_total(dealer_hand)
        # H17 Rule: Dealer hits on Soft 17
        is_soft_17 = (total == 17 and sum(dealer_hand) == 17 and 11 in dealer_hand)
        
        if total < 17 or is_soft_17:
            dealer_hand.append(shoe.draw())
        else:
            break
    return calculate_total(dealer_hand)

def play_player(player_hand, dealer_upcard, shoe):
    while True:
        total = calculate_total(player_hand)
        if total >= 21:
            break
            
        # Simplified Basic Strategy
        if total <= 11:
            player_hand.append(shoe.draw())
        elif total >= 17:
            break
        else:
            if dealer_upcard in [2, 3, 4, 5, 6]:
                break # Stand against weak dealer cards
            else:
                player_hand.append(shoe.draw())
                
    return calculate_total(player_hand)

def calculate_kelly_bet(bankroll, true_count, min_bet):
    # Baseline edge for H17 is approx -0.72%
    # Each +1 True Count adds roughly +0.50% to the player's edge
    player_edge = -0.0072 + (true_count * 0.005)
    
    if player_edge > 0:
        # Calculate Half-Kelly fraction to manage variance
        kelly_fraction = player_edge / 2
        optimal_bet = bankroll * kelly_fraction
        # Bet the optimal amount, but don't bet less than table minimum
        return max(min_bet, optimal_bet)
    else:
        # If no mathematical edge, bet the absolute table minimum
        return min_bet

def run_simulation(total_rounds=50000, initial_bankroll=10000, verbose=True):
    bankroll = initial_bankroll
    min_bet = 10 
    
    shoe = CasinoShoe(num_decks=6, penetration=0.75)
    
    hands_played = 0
    hands_watched = 0
    
    for _ in range(total_rounds):
        if bankroll < min_bet:
            if verbose: print("Bankrupt! Risk of ruin achieved.")
            break
            
        if shoe.needs_shuffle():
            shoe.shuffle()
            
        true_count = shoe.get_true_count()
        
        # Wonging Strategy
        if true_count < -1.0:
            hands_watched += 1
            for _ in range(6):
                if not shoe.needs_shuffle(): shoe.draw()
            continue 
        
        hands_played += 1
        
        current_bet = calculate_kelly_bet(bankroll, true_count, min_bet)
        current_bet = min(current_bet, bankroll)
        
        player_hand = [shoe.draw(), shoe.draw()]
        dealer_hand = [shoe.draw(), shoe.draw()]
        dealer_upcard = dealer_hand[0]
        
        player_bj = calculate_total(player_hand) == 21
        dealer_bj = calculate_total(dealer_hand) == 21
        
        if player_bj and not dealer_bj:
            bankroll += current_bet * 1.5
        elif dealer_bj and not player_bj:
            bankroll -= current_bet
        elif player_bj and dealer_bj:
            pass 
        else:
            player_total = play_player(player_hand, dealer_upcard, shoe)
            if player_total > 21:
                bankroll -= current_bet 
            else:
                dealer_total = play_dealer(dealer_hand, shoe)
                if dealer_total > 21:
                    bankroll += current_bet
                elif player_total > dealer_total:
                    bankroll += current_bet
                elif player_total < dealer_total:
                    bankroll -= current_bet

    profit = bankroll - initial_bankroll
    
    if verbose:
        print(f"Total Casino Rounds: {total_rounds}")
        print(f"Hands Actually Played: {hands_played}")
        print(f"Hands Watched (Wonged Out): {hands_watched}")
        print(f"Final Bankroll: {bankroll:.2f} MAD")
        print(f"Total Profit: {profit:.2f} MAD")
    
    return bankroll, profit, hands_played

def run_monte_carlo_batch(simulations=100, rounds_per_sim=20000, initial_bankroll=10000):
    print(f"Running {simulations} independent careers of {rounds_per_sim} rounds each...")
    
    final_bankrolls = []
    profitable_runs = 0
    ruined_runs = 0
    
    for i in range(simulations):
        # Print progress so you know it's not frozen
        if (i + 1) % 10 == 0:
            print(f"Completed {i + 1}/{simulations} simulations...")
            
        final_bankroll, profit, _ = run_simulation(
            total_rounds=rounds_per_sim, 
            initial_bankroll=initial_bankroll, 
            verbose=False # Turn off the individual prints
        )
        
        final_bankrolls.append(final_bankroll)
        
        if final_bankroll > initial_bankroll:
            profitable_runs += 1
        if final_bankroll < 10: # Hit minimum bet threshold
            ruined_runs += 1

    # Calculate Statistics
    win_rate = (profitable_runs / simulations) * 100
    ruin_rate = (ruined_runs / simulations) * 100
    avg_bankroll = sum(final_bankrolls) / simulations
    
    print("\n--- MACRO MONTE CARLO RESULTS ---")
    print(f"Total Simulations Run: {simulations}")
    print(f"Win Rate (Profitable Runs): {win_rate:.2f}%")
    print(f"Risk of Ruin (Bankruptcies): {ruin_rate:.2f}%")
    print(f"Average Final Bankroll: {avg_bankroll:.2f} MAD")
    
    # Plotting the Distribution (Histogram)
    plt.figure(figsize=(10, 6))
    plt.hist(final_bankrolls, bins=20, color='skyblue', edgecolor='black')
    plt.axvline(initial_bankroll, color='red', linestyle='dashed', linewidth=2, label='Starting Bankroll')
    plt.axvline(avg_bankroll, color='green', linestyle='dashed', linewidth=2, label='Average Final Bankroll')
    
    plt.title(f"Distribution of Final Bankrolls over {simulations} Simulations")
    plt.xlabel("Final Bankroll (MAD)")
    plt.ylabel("Frequency (Number of Runs)")
    plt.legend()
    plt.grid(axis='y', alpha=0.75)
    plt.show()

# Execute the Batch
# Note: 100 simulations of 20,000 rounds might take 10-20 seconds to compute.
run_monte_carlo_batch(simulations=1000, rounds_per_sim=500, initial_bankroll=100)
