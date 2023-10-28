import os
import cv2
import xml.etree.ElementTree as ET


def create_output_folder(output_folder):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def update_dataset(input_folder,output_folder,additional_height):
    # Loop through the XML files in the input folder
    for xml_file in os.listdir(input_folder):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(input_folder, xml_file)
            image_filename = os.path.splitext(xml_file)[0] + ".jpg"
            image_path = os.path.join(input_folder, image_filename)

            # Check if the image file exists
            if not os.path.exists(image_path):
                print(f"Image file not found: {image_path}")
                continue

            # Load the XML data
            tree = ET.parse(xml_path)
            root = tree.getroot()

            height, width, xmax, xmin, ymax, ymin = extract_xml_info(root)

            # Read image
            image = cv2.imread(image_path)
            image = check_and_rotate_image(image, xmax, xmin, ymax, ymin)

            ymax, ymin = create_lower_and_upper_bound(additional_height, height, ymax, ymin)

            # Read and crop the image
            cropped_image = image[ymin:ymax, 0:width]

            # Calculate new values
            height = ymax - ymin

            update_xml(height, root, ymax, ymin)

            save_result(cropped_image, image_filename, output_folder, tree, xml_file)
    print("Cropping and saving complete with additional 5 pixels of height at the top and bottom.")


def save_result(cropped_image, image_filename, output_folder, tree, xml_file):
    # Save the cropped image and the updated XML file to the output folder
    output_image_path = os.path.join(output_folder, image_filename)
    output_xml_path = os.path.join(output_folder, xml_file)
    cv2.imwrite(output_image_path, cropped_image)
    tree.write(output_xml_path)


def update_xml(height, root, ymax, ymin):
    # Update the XML data
    root.find(".//ymin").text = str(ymin)  # Adjusted ymin
    root.find(".//ymax").text = str(ymax)  # Adjusted ymax
    root.find(".//height").text = str(height)  # Adjusted ymax


def create_lower_and_upper_bound(additional_height, height, ymax, ymin):
    if ymin - additional_height < 0:
        ymin = ymin
    else:
        ymin = ymin - additional_height
    if ymax + additional_height > height:
        ymax = ymax

    else:
        ymax = ymax + additional_height
    return ymax, ymin


def check_and_rotate_image(image, xmax, xmin, ymax, ymin):
    if (ymax - ymin) > (xmax - xmin):
        # by 90 degrees clockwise
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return image


def extract_xml_info(root):
    height = int(root.find(".//height").text)
    width = int(root.find(".//width").text)
    xmin = int(root.find(".//xmin").text)
    ymin = int(root.find(".//ymin").text)
    xmax = int(root.find(".//xmax").text)
    ymax = int(root.find(".//ymax").text)
    return height, width, xmax, xmin, ymax, ymin


def main():
    # Define the additional height to be cropped at the top and bottom
    additional_height = 50
    # Set the input and output directories
    input_folder = r"C:\Users\nehab\PycharmProjects\createDigitalMeterDataset\Counter-in-digital-meter\valid"
    output_folder = r"C:\Users\nehab\PycharmProjects\createDigitalMeterDataset\Counter-in-digital-meter-Output\valid"

    create_output_folder(output_folder)
    update_dataset(input_folder, output_folder, additional_height)

if __name__ == "__main__":
    main()