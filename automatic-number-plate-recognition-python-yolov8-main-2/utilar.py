import string
import easyocr

# Initialize the OCR reader with Arabic and English
reader = easyocr.Reader(['ar', 'en'], gpu=False)

# Mapping dictionaries for character conversion (Arabic-style misrecognitions)
dict_char_to_int = {
    'O': '0',
    'I': '1',
    'J': '3',
    'A': '4',
    'G': '6',
    'S': '5'
}

dict_int_to_char = {
    '0': 'O',
    '1': 'I',
    '3': 'J',
    '4': 'A',
    '6': 'G',
    '5': 'S'
}

# Arabic license plate corrections (if OCR misreads letters)
arabic_corrections = {
    "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4", 
    "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9",
    "أ": "A", "ب": "B", "ج": "J", "د": "D", "ر": "R", "ص": "S",
    "ط": "T", "ع": "E", "ق": "Q", "ك": "K", "ل": "L", "م": "M", 
    "ن": "N", "ه": "H", "و": "W", "ي": "Y"
}

def write_csv(results, output_path):
    """Write the OCR results to a CSV file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                if 'car' in results[frame_nmr][car_id] and 'license_plate' in results[frame_nmr][car_id] and 'text' in results[frame_nmr][car_id]['license_plate']:
                    f.write('{},{},{},{},{},{},{}\n'.format(
                        frame_nmr,
                        car_id,
                        '[{} {} {} {}]'.format(*results[frame_nmr][car_id]['car']['bbox']),
                        '[{} {} {} {}]'.format(*results[frame_nmr][car_id]['license_plate']['bbox']),
                        results[frame_nmr][car_id]['license_plate']['bbox_score'],
                        results[frame_nmr][car_id]['license_plate']['text'],
                        results[frame_nmr][car_id]['license_plate']['text_score'])
                    )

def license_complies_format(text):
    """Check if the extracted text follows Arabic license plate format."""
    parts = text.split(' ')
    if len(parts) != 2:
        return False
    
    letters, numbers = (parts[0], parts[1]) if parts[0].isalpha() else (parts[1], parts[0])
    
    if len(numbers) >= 1 and len(numbers) <= 4 and len(letters) == 3:
        return True
    return False

def format_license(text):
    """Format the license plate text to match expected format."""
    license_plate_ = ''
    mapping = {0: dict_char_to_int, 1: dict_char_to_int, 4: dict_int_to_char, 5: dict_int_to_char,
               2: dict_char_to_int, 3: dict_int_to_char}
    
    for j in range(min(len(text), 7)):  # Prevent out-of-range errors
        if text[j] in mapping.get(j, {}):
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]
    
    return license_plate_

def correct_arabic_text(text):
    """Correct OCR misread Arabic characters and numbers."""
    return ''.join(arabic_corrections.get(char, char) for char in text)

def read_license_plate(license_plate_crop):
    """Read and format the Arabic license plate text from an image crop."""
    detections = reader.readtext(license_plate_crop)
    print(detections)

    for detection in detections:
        bbox, text, score = detection

        # Convert Arabic misread characters
        cleaned_text = correct_arabic_text(text)

        # Remove non-alphabetic or non-numeric characters
        cleaned_text = ''.join(c for c in cleaned_text if c.isalpha() or c.isdigit()).upper()

        i = 0
        while i < len(cleaned_text) and cleaned_text[i].isdigit():
            i += 1

        numbers = cleaned_text[:i]
        letters = cleaned_text[i:]

        formatted_text = f"{letters} {numbers}"

        if license_complies_format(formatted_text):
            return formatted_text, score
    
    return None, None

def get_car(license_plate, vehicle_track_ids):
    """Retrieve vehicle details based on license plate coordinates."""
    x1, y1, x2, y2, score, class_id = license_plate

    for j, (xcar1, ycar1, xcar2, ycar2, car_id) in enumerate(vehicle_track_ids):
        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            return vehicle_track_ids[j]
    
    return -1, -1, -1, -1, -1

def convert_bbox_to_xyxy(bbox):
    """Convert bounding box format from list to (x1, y1, x2, y2)."""
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]
    
    return min(x_coords), min(y_coords), max(x_coords), max(y_coords)
