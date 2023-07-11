import csv
from datetime import datetime

# Open the CSV file for reading
with open(r"C:\Users\Logan\Desktop\School Files\Senior Project\Shared_Dat\PhaseII_ET_WithNextWater.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)

    # Read the header row
    header = next(reader)

    # Change the first column label to 'Date'
    header[0] = 'Date'

    # Create a new CSV file for writing
    with open('output.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write the modified header row to the new file
        writer.writerow(header)

        # Process the remaining rows
        for row in reader:
            # Convert the first column to datetime object
            date_str = row[0]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')

            # Format the first column as '%m/%d/%y' with quotation marks
            row[0] = str(date_obj.strftime('%m/%d/%y'))

            # Write the modified row to the new file
            writer.writerow(row)