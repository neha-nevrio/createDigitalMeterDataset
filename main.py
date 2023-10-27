import os
import cv2
import xml.etree.ElementTree as ET

# Set the input and output directories
input_folder = r"C:\Users\nehab\PycharmProjects\createDigitalMeterDataset\Counter-in-digital-meter\test"
output_folder = r"C:\Users\nehab\PycharmProjects\createDigitalMeterDataset\New-Counter-Digital\test"

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through files in input folder
for xml_file in os.listdir(input_folder):
    if xml_file.endswith('.xml'):
        xml_path = os.path.join(input_folder, xml_file)
        image_filename = os.path.splitext(xml_file)[0] + ".jpg"
        print(image_filename)
        image_path = os.path.join(input_folder, image_filename)

        # Load the XML data
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find the specific object element that contains the coordinate
        xmin = int(root.find(".//xmin").text)
        ymin = int(root.find(".//ymin").text)
        xmax = int(root.find(".//xmax").text)
        ymax = int(root.find(".//ymax").text)

        # Read image
        image = cv2.imread(image_path)

        # Crop image according to coordinates
        try:
            cropped_image = image[ymin:ymax, xmin:xmax]
        except Exception as e:
            print('cropped_image err', e)

        # Calculate new values
        xmax = xmax - xmin
        width = xmax
        ymax = ymax - ymin
        height = ymax

        # Update the XML data
        root.find(".//xmin").text = "0"
        root.find(".//ymin").text = "0"
        root.find(".//xmax").text = str(xmax)
        root.find(".//ymax").text = str(ymax)
        root.find(".//width").text = str(width)
        root.find(".//height").text = str(height)

        # Save the cropped image to the output folder
        output_image_path = os.path.join(output_folder, image_filename)
        cv2.imwrite(output_image_path, cropped_image)

        # Save the XML file to the output folder
        output_xml_path = os.path.join(output_folder, xml_file)
        tree.write(output_xml_path)

    print("Cropping and saving complete.")
