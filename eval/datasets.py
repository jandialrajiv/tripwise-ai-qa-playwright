POLICY_QA = [
    {"id": "pci_001", "q": "What is PCI compliance in travel payments?", "gold": "PCI DSS is a security standard designed to protect payment card data.", "must_contain": ["payment", "security"]},
    {"id": "bag_001", "q": "What is the baggage policy for domestic flights?", "gold": "Standard carry-on is 1 carry-on plus 1 personal item.", "must_contain": ["carry-on", "personal"]},
    {"id": "cancel_001", "q": "What are cancellation rules for non-refundable fares?", "gold": "Non-refundable fares typically are not eligible for cash refunds; a credit may be offered depending on fare rules.", "must_contain": ["non-refundable", "credit"]},
]
