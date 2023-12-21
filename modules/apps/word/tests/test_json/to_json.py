import json


x = {'position': 0, 'id': 'template_settings', 'font_size': 10, 'font_name': 'Arial', 'orientation': 'landscape', 'full_page_title': 'imas', 'pdf_orientation': 'portrait', 'title': 'Мой Шаблон', 'format': 'word_kaz', 'user_id': '2114', 'an_id': '10808', 'location': '2', 's_date': '2023-08-06', 'f_date': '2023-08-06', 's_time': '00:00', 'f_time': '23:59', 'full_text': '0', 'sCountry_id': '0', 'iCategory_id': 'all', 'sResource_id': 'all', 'metrics': '0', 'order': '', 'sSentiment': '', 'sLanguage_id': 'all', 'message_type': 'all', 'place': '0', 'place_id': '0', 'token': 'XllWCJMBjQpi'}

with open('static_rest_data.JSON', 'w') as file:
    file.write(json.dumps(x))