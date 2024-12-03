# filename: locate_search_fields.py
from bs4 import BeautifulSoup

# Step 1: Load the saved HTML content
with open('drcor_search_form.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Step 2: Analyze the DOM
soup = BeautifulSoup(html_content, 'html.parser')

# Identify search input fields
search_input_fields = soup.find_all('input', {'type': 'text'})
search_field_attributes = [{ 'id': field.get('id'), 'name': field.get('name'), 'class': field.get('class'), 'placeholder': field.get('placeholder') } for field in search_input_fields]

# Identify search trigger elements (buttons)
search_buttons = soup.find_all(['button', 'input'], {'type': 'submit'})
search_button_attributes = [{ 'id': button.get('id'), 'class': button.get('class'), 'text': button.text.strip() } for button in search_buttons]

# Save identified fields and buttons to a file
with open('search_fields_output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write("Search Input Fields:\n")
    for attr in search_field_attributes:
        output_file.write(f"{attr}\n")
    
    output_file.write("\nSearch Buttons:\n")
    for attr in search_button_attributes:
        output_file.write(f"{attr}\n")

print("Search fields and buttons saved to 'search_fields_output.txt'.")