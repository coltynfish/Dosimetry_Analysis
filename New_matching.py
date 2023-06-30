import pandas as pd
import numpy as np

# Take user input for array name
arrnm = input("Name of Array (case sensitive): ")
arrname = arrnm + ".txt"

# Open txt file and read the content in a list
with open(arrname, 'r') as f:
    arrbar = f.read().split()
    arrbar = [barcode.replace('\n', '').replace('\\', '') for barcode in arrbar]
print("The barcodes are:", arrbar)

# You will need to change the path to the file
file_path = input("Enter the file path for the Excel file: ")
df = pd.read_excel(file_path)

# Delete all columns except for the ones we want
# This leaves only the serial number, the read date, and the Deep Dose values
df = df[['Serial Number', 'Read Date/Time', 'Deep Dose']]

# Print the head of the dataframe
print(df.head(5))

# This collects the date and time you want to match
# Get user date and time input
date = input("Enter the date (MM/DD/YYYY): ")
time = input("Enter the starting time (HH:MM:SS): ")

# This converts the input into a pandas date and time
indate = pd.to_datetime(date + ' ' + time)

# This filters the dataframe by the date and time
# Check if data is after the input time
df = df[df["Read Date/Time"] >= indate]

avg_pos = []

# For loop for matching the barcodes
# This loop will match the barcodes in the Excel file to the barcodes in the text file
# It will then calculate the average Deep Dose for each barcode
for i in range(len(arrbar)):
    t2 = df["Serial Number"].str.strip() == arrbar[i]
    df2 = df[t2]
    print("The dataframe for %s is: " % arrbar[i])
    print(df2)
    avg = df2["Deep Dose"].astype("int").mean()
    avg_pos.append(avg)
    print("The average is:", avg)
    print("\n")

# Create a 10x11 array from the output_array
output_array_2d = np.array(avg_pos).reshape((10, 11))

# Replace NaN values with 0s
output_array_2d = np.nan_to_num(output_array_2d)

print("Output 2D array:")
print(output_array_2d)

avgfile = arrnm + "avg.txt"
with open(avgfile, 'w') as f:
    for row in output_array_2d:
        for item in row:
            f.write("%s " % item)
        f.write("\n")

# Ask user if they want to run the root file
# plot = input("Do you want to run the root file? (y/n): ")
# if plot == 'y':
#     # Run root file
#     os.system("root -l testrootanalysis_3.C")
# else:
#     print("Ok, bye!")
