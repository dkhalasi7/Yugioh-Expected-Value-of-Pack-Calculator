import csv
from collections import defaultdict

def read_yugioh_file(filename):
    """Read the Yugioh data from a text file."""
    with open(filename, 'r') as f:
        return f.readlines()

def write_to_csv(data, output_filename):
    """Write extracted data to a CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Rarity', 'Set and Card Number', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # write header

        for entry in data:
            writer.writerow(entry)

def extract_data(lines):
    """Extract data from the lines."""
    extracted_data = []
    for i in range(0, len(lines), 6):  # Step of 6 since there are 6 lines per record
        name = lines[i].strip().strip('"')
        rarity = lines[i + 1].strip()
        set_and_card_number = lines[i + 2].strip()
        price = lines[i + 3].strip().strip('$')  # Removing dollar sign for cleaner data

        extracted_data.append({
            'Name': name,
            'Rarity': rarity,
            'Set and Card Number': set_and_card_number,
            'Price': price
        })
    return extracted_data

def count_rarities(data):
    """Count the number of cards for each rarity."""
    rarity_count = defaultdict(int)
    for entry in data:
        rarity = entry['Rarity']
        rarity_count[rarity] += 1
    return rarity_count

def average_value_for_rarity(data, rarity):
    """Calculate the average value of a card for a given rarity."""
    total_value = 0.0
    count = 0

    for entry in data:
        if entry['Rarity'] == rarity:
            total_value += float(entry['Price'])
            count += 1

    if count == 0:  # to avoid division by zero
        return 0
    else:
        return total_value / count

def compute_expected_value_qcr_set(data):
    """Compute the expected value of a pack based on the pull rates and average card values."""
    C = average_value_for_rarity(data, "Common")
    S = average_value_for_rarity(data, "Super Rare")
    U = average_value_for_rarity(data, "Ultra Rare")
    Se = average_value_for_rarity(data, "Secret Rare")
    Q = average_value_for_rarity(data, "Quarter Century Secret Rare")
    # Given Probabilities
    P_U = 1/4
    P_Se = 1/12
    P_Q = 1/(24*4)

    # Calculating P(S) as remaining probability after other rarer cards
    P_S = 1 - P_U - P_Se - P_Q

    # Expected Value formula
    EV = 8*C + P_S*S + P_U*U + P_Se*Se + P_Q*Q

    return EV

def compute_expected_value_regular_set(data):
    """Compute the expected value of a pack based on the pull rates and average card values."""
    C = average_value_for_rarity(data, "Common")
    S = average_value_for_rarity(data, "Super Rare")
    U = average_value_for_rarity(data, "Ultra Rare")
    Se = average_value_for_rarity(data, "Secret Rare")
    St = average_value_for_rarity(data, "Starlight Rare")
    # Given Probabilities
    P_U = 1/4
    P_Se = 1/12
    P_St = 1/(24*12)

    # Calculating P(S) as remaining probability after other rarer cards
    P_S = 1 - P_U - P_Se - P_St

    # Expected Value formula
    EV = 8*C + P_S*S + P_U*U + P_Se*Se + P_St*St

    return EV

def compute_expected_value_collectors_set(data):
    """Compute the expected value of a pack based on the pull rates and average card values."""
    R = average_value_for_rarity(data, "Rare")
    S = average_value_for_rarity(data, "Super Rare")
    U = average_value_for_rarity(data, "Ultra Rare")
    Cr = average_value_for_rarity(data, "Collector's Rare")
    # Given Probabilities
    P_U = 1/8
    P_Cr = 1/(24*4)

    # Calculating P(S) as remaining probability after other rarer cards
    P_S = 1 - P_U  - P_Cr

    # Expected Value formula
    EV = 8*R + P_S*S + P_U*U + P_Cr*Cr

    return EV
def rarity_exists_in_set(data, target_rarity):
    """Check if a specific rarity exists in the dataset."""
    for entry in data:
        if entry['Rarity'] == target_rarity:
            return True
    return False

def main():
    input_filename = 'amde_prices.txt'
    output_filename = 'amde.csv'

    lines = read_yugioh_file(input_filename)
    data = extract_data(lines)
    write_to_csv(data, output_filename)

    print(f"Data extraction complete! Saved to {output_filename}")
    
    # Count rarities and output the counts
    rarity_counts = count_rarities(data)
    for rarity, count in rarity_counts.items():
        print(f"{rarity}: {count} cards")

    print(f"Data extraction complete! Saved to {output_filename}")
    
    # Compute and print the expected value of a pack
    if rarity_exists_in_set(data, "Quarter Century Secret Rare"):
        EV = compute_expected_value_qcr_set(data)
        print(f"Expected value of a pack: ${EV:.2f}")
        print(f"Expected Value of 24 Packs: ${EV*24:.2f}")
    elif rarity_exists_in_set(data, "Starlight Rare"):
        EV = compute_expected_value_regular_set(data)
        print(f"Expected value of a pack: ${EV:.2f}")
        print(f"Expected Value of 24 Packs: ${EV*24:.2f}")
    elif rarity_exists_in_set(data, "Collector's Rare"):  
        EV = compute_expected_value_collectors_set(data)
        print(f"Expected value of a pack: ${EV:.2f}")
        print(f"Expected Value of 24 Packs: ${EV*24:.2f}")        
if __name__ == "__main__":
    main()