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

def run_simulation(hands=20000, initial_bankroll=10000):
    bankroll = initial_bankroll
    min_bet = 10 # Let's say a 10 MAD minimum table
    
    history = [bankroll]
    shoe = CasinoShoe(num_decks=6, penetration=0.75)
    
    for _ in range(hands):
        if bankroll < min_bet:
            print("Bankrupt! Risk of ruin achieved.")
            break
            
        if shoe.needs_shuffle():
            shoe.shuffle()
            
        # 1. Calculate Bet Size based on True Count
        true_count = shoe.get_true_count()
        current_bet = calculate_kelly_bet(bankroll, true_count, min_bet)
        
        # Ensure we don't bet more than we have
        current_bet = min(current_bet, bankroll)
        
        # 2. Deal Initial Cards
        player_hand = [shoe.draw(), shoe.draw()]
        dealer_hand = [shoe.draw(), shoe.draw()]
        dealer_upcard = dealer_hand[0]
        
        player_bj = calculate_total(player_hand) == 21
        dealer_bj = calculate_total(dealer_hand) == 21
        
        # 3. Resolve Blackjacks
        if player_bj and not dealer_bj:
            bankroll += current_bet * 1.5
        elif dealer_bj and not player_bj:
            bankroll -= current_bet
        elif player_bj and dealer_bj:
            pass # Push
        else:
            # 4. Play out the hand
            player_total = play_player(player_hand, dealer_upcard, shoe)
            
            if player_total > 21:
                bankroll -= current_bet # Bust
            else:
                dealer_total = play_dealer(dealer_hand, shoe)
                
                if dealer_total > 21:
                    bankroll += current_bet
                elif player_total > dealer_total:
                    bankroll += current_bet
                elif player_total < dealer_total:
                    bankroll -= current_bet
                    
        history.append(bankroll)

    # Calculate overall ROI
    profit = bankroll - initial_bankroll
    print(f"Hands Played: {len(history)-1}")
    print(f"Final Bankroll: {bankroll:.2f}")
    print(f"Total Profit: {profit:.2f}")
    
    return history

# --- Run and Visualize ---
print("Running Kelly Bet Simulation...")
bankroll_history = run_simulation(hands=50000, initial_bankroll=10000)

plt.figure(figsize=(10, 6))
plt.plot(bankroll_history, color='blue', linewidth=1)
plt.axhline(y=10000, color='red', linestyle='--', label='Starting Bankroll')
plt.title("Card Counting & Half-Kelly Bet Sizing: Bankroll Trajectory")
plt.xlabel("Hands Played")
plt.ylabel("Bankroll")
plt.legend()
plt.grid(True, alpha=0.3)

# Use a logarithmic scale if the growth gets massive, otherwise linear is fine
if max(bankroll_history) > 50000:
    plt.yscale('log')
    plt.ylabel("Bankroll (Log Scale)")

plt.show()
