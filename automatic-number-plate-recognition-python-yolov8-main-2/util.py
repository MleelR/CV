import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                   'license_plate' in results[frame_nmr][car_id].keys() and \
                   'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['car']['bbox'][0],
                                                                results[frame_nmr][car_id]['car']['bbox'][1],
                                                                results[frame_nmr][car_id]['car']['bbox'][2],
                                                                results[frame_nmr][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()


def license_complies_format(text):
    parts = text.split(' ')
    if len(parts) != 2:
        return False
    
    letters, numbers = (parts[0], parts[1]) if parts[0].isalpha() else (parts[1], parts[0])
    
    if len(numbers) >= 1 and len(numbers) <= 4 and len(letters) == 3:
        return True
    else:
        return False




def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    mapping = {0: dict_char_to_int, 1: dict_char_to_int, 4: dict_int_to_char, 5: dict_int_to_char,
               2: dict_char_to_int, 3: dict_int_to_char}
    for j in [0, 1, 2, 3, 4, 5, 6]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_

def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)
    
    all_letters = []
    all_numbers = []
    best_score = 0

    for detection in detections:
        bbox, text, score = detection

        # Remove non-alphabetic/non-numeric characters and convert to uppercase
        cleaned_text = ''.join(c for c in text if c.isalnum()).upper()

        # Separate letters and numbers
        letters = ''.join(c for c in cleaned_text if c.isalpha())
        numbers = ''.join(c for c in cleaned_text if c.isdigit())

        if letters:
            all_letters.append(letters)
        if numbers:
            all_numbers.append(numbers)

        # Keep track of the highest confidence score
        best_score = max(best_score, score)

    # Combine letters and numbers
    formatted_text = f"{''.join(all_letters)} {''.join(all_numbers)}" if all_letters and all_numbers else None
    

    return (formatted_text, best_score) if formatted_text else (None, None)









def get_car(license_plate, vehicle_track_ids):
    """
    Retrieve the vehicle coordinates and ID based on the license plate coordinates.

    Args:
        license_plate (tuple): Tuple containing the coordinates of the license plate (x1, y1, x2, y2, score, class_id).
        vehicle_track_ids (list): List of vehicle track IDs and their corresponding coordinates.

    Returns:
        tuple: Tuple containing the vehicle coordinates (x1, y1, x2, y2) and ID.
    """
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1


def convert_bbox_to_xyxy(bbox):
    """
    Converts a bounding box of the format [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] 
    to (x1, y1, x2, y2).
    """
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]
    
    x1, x2 = min(x_coords), max(x_coords)
    y1, y2 = min(y_coords), max(y_coords)
    
    return (x1, y1, x2, y2)
