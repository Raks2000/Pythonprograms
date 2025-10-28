def calculate_notes(amount):
    notes = [2000, 500, 100]
    note_count = {}
    
    for note in notes:
        if amount >= note:
            note_count[note] = amount // note
            amount = amount % note
        else:
            note_count[note] = 0
    
    return note_count

# Get input from user
withdrawal_amount = int(input("Enter withdrawal amount: "))

# Calculate notes
result = calculate_notes(withdrawal_amount)

# Print results
print("\nNotes to be dispensed:")
print(f"₹2000 notes: {result[2000]}")
print(f"₹500 notes: {result[500]}")
print(f"₹100 notes: {result[100]}")