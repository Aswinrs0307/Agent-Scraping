# filename: display_bank_of_cyprus_details.py

# Read and print the contents of the text file
with open('bank_of_cyprus_details.txt', 'r', encoding='utf-8') as file:
    details = file.read()

print(details)