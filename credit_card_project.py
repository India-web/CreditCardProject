import random

# -----------------------------
# CARD DATA TABLE
# -----------------------------
CARD_TABLE = [
    # VISA
    ("Visa", ("4",), (13, 16, 19)),
    ("Visa Debit", ("4000", "4001", "4005"), (16,)),
    ("Visa Prepaid", ("4026", "4175", "4508", "4844", "4913", "4917"), (16,)),

    # MASTERCARD
    ("Mastercard", tuple(str(i) for i in range(51, 56)) +
                   tuple(str(i) for i in range(2221, 2721)), (16,)),
    ("Mastercard Debit", ("5200", "5204", "5218"), (16,)),
    ("Mastercard Prepaid", ("5105",), (16,)),

    # AMERICAN EXPRESS
    ("American Express", ("34", "37"), (15,)),

    # DISCOVER
    ("Discover", ("6011", "65") + tuple(str(i) for i in range(644, 650)), (16,)),
    ("Discover Debit", ("60119",), (16,)),

    # DINERS CLUB
    ("Diners Club", ("300", "301", "302", "303", "304", "305", "36", "38"), (14,)),

    # JCB
    ("JCB", tuple(str(i) for i in range(3528, 3590)), (16,)),

    # UNIONPAY
    ("UnionPay", ("62",), (16, 17, 18, 19)),
    ("UnionPay Debit", ("6200",), (16, 19)),

    # BCcard / DinaCard
    ("BCcard / DinaCard", ("6555",), (16,)),

    # CARTES BANCAIRES (co-branded)
    ("Cartes Bancaires / Visa", ("40000025",), (16,)),
    ("Cartes Bancaires / Mastercard", ("55555525",), (16,)),

    # EFTPOS (Australia)
    ("eftpos Australia / Visa", ("400005036",), (16,)),
    ("eftpos Australia / Mastercard", ("555505036",), (16,)),

    # CARNET (Mexico)
    ("Carnet", ("506221",), (16,))
]


# -----------------------------
# LUHN ALGORITHM
# -----------------------------
def luhn_checksum(number):
    digits = list(map(int, number[::-1]))
    total = 0

    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            total += d - 9 if d > 9 else d
        else:
            total += d

    return total % 10 == 0


# -----------------------------
# CARD IDENTIFICATION
# -----------------------------
def identify_card(number):
    for name, prefixes, lengths in CARD_TABLE:
        if len(number) in lengths:
            for p in prefixes:
                if number.startswith(p):
                    return name
    return None


# -----------------------------
# CARD CATEGORY (MII)
# -----------------------------
def card_category(number):
    categories = {
        '1': 'Airlines',
        '2': 'Airlines and future industry',
        '3': 'Travel and entertainment',
        '4': 'Banking and financial',
        '5': 'Banking and financial',
        '6': 'Merchandising and banking',
        '7': 'Petroleum industry',
        '8': 'Healthcare and telecom',
        '9': 'National assignment'
    }
    return categories.get(number[0], 'Unknown')


# -----------------------------
# VALIDATION
# -----------------------------
def validate_card(number):
    if not number.isdigit():
        return {
            "valid": False,
            "message": "Invalid input"
        }

    if not luhn_checksum(number):
        return {
            "valid": False,
            "message": "Invalid card"
        }

    issuer = identify_card(number)

    if not issuer:
        return {
            "valid": False,
            "message": "Invalid card"
        }

    return {
        "valid": True,
        "category": card_category(number),
        "issuer": issuer
    }


# -----------------------------
# CARD GENERATION
# -----------------------------
def generate_card(card_name):
    for name, prefixes, lengths in CARD_TABLE:
        if name.lower() == card_name.lower():
            prefix = random.choice(prefixes)
            length = random.choice(lengths)

            number = prefix
            while len(number) < length - 1:
                number += str(random.randint(0, 9))

            for i in range(10):
                candidate = number + str(i)
                if luhn_checksum(candidate):
                    return candidate
    return None


# -----------------------------
# MAIN MENU
# -----------------------------
def main():
    while True:
        print("\n--- CREDIT CARD PROJECT ---")
        print("1. Validate credit card")
        print("2. Generate credit card")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            cc = input("Enter card number: ")
            print(validate_card(cc))

        elif choice == '2':
            print("\nAvailable card types:")
            for name, _, _ in CARD_TABLE:
                print("-", name)

            card_name = input("\nEnter card name exactly as shown: ")
            card = generate_card(card_name)

            if card:
                print("Generated card:", card)
            else:
                print("Invalid card type")

        elif choice == '3':
            print("Exiting program")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
