import random

CARD_TABLE = [
    ("Visa Debit", ("4000", "4001", "4005"), (16,)),
    ("Visa Prepaid", ("4026", "4175", "4508", "4844", "4913", "4917"), (16,)),
    ("Visa", ("4",), (13, 16, 19)),

    (
        "Mastercard",
        tuple(map(str, range(51, 56))) + tuple(map(str, range(2221, 2721))),
        (16,)
    ),
    ("Mastercard Debit", ("5200", "5204", "5218"), (16,)),
    ("Mastercard Prepaid", ("5105",), (16,)),

    ("American Express", ("34", "37"), (15,)),

    (
        "Discover",
        ("6011", "65") + tuple(map(str, range(644, 650))),
        (16,)
    ),
    ("Discover Debit", ("60119",), (16,)),

    ("Diners Club", ("300", "301", "302", "303", "304", "305", "36", "38"), (14,)),
    ("JCB", tuple(map(str, range(3528, 3590))), (16,)),

    ("UnionPay Debit", ("6200",), (16, 19)),
    ("UnionPay", ("62",), (16, 17, 18, 19)),

    ("BCcard / DinaCard", ("6555",), (16,)),
    ("Carnet", ("506221",), (16,))
]

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

def identify_card(number):
    for name, prefixes, lengths in CARD_TABLE:
        if len(number) in lengths:
            for p in prefixes:
                if number.startswith(p):
                    return name
    return None

def card_category(number):
    return {
        '1': 'Airlines',
        '2': 'Airlines & future industry',
        '3': 'Travel & entertainment',
        '4': 'Banking & financial',
        '5': 'Banking & financial',
        '6': 'Merchandising & banking',
        '7': 'Petroleum industry',
        '8': 'Healthcare & telecom',
        '9': 'National assignment'
    }.get(number[0], 'Unknown')

def validate_card(number):
    if not number or not number.isdigit():
        return {"status": "error", "message": "Invalid input"}

    if not luhn_checksum(number):
        return {"status": "invalid", "message": "Luhn check failed"}

    issuer = identify_card(number)
    if not issuer:
        return {"status": "invalid", "message": "Unknown issuer"}

    return {
        "status": "valid",
        "issuer": issuer,
        "category": card_category(number),
        "length": len(number)
    }

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
