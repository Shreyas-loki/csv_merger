import glob
import shutil
import os
from datetime import datetime


def get_concatenated_csv(all_csv_files):
    
    current_date_time = datetime.now()
    result_csv_name = str(current_date_time.year) + str(current_date_time.month).zfill(2) + str(current_date_time.day).zfill(2) + '_' + \
                    str(current_date_time.hour).zfill(2) + str(current_date_time.minute).zfill(2) + str(current_date_time.second).zfill(2)
                # zfill(2) does 2 zeros padding to the left of the string, based on the size of the string

    with open('./csv_results/' + result_csv_name + '.csv', 'w') as outFile:    # All the .csv result files will be in "csv_results" directory
        for index, fname in enumerate(all_csv_files):
            with open(fname, 'r') as inFile:
                if index != 0:          # Throw away header on all but first file
                    inFile.readline()       
                
                # Block copy rest of file from input to output without parsing
                shutil.copyfileobj(inFile, outFile)
                print(fname + " has been copied.")
                outFile.write('\n')


def remove_all_input_csv(path):
    file_names_list = os.listdir(path)

    for item in file_names_list:
        if item.endswith(".csv"):
            os.remove(os.path.join(path, item))



# main code
path = r'C://Users/shreyas.r/OneDrive - HCL Technologies Ltd/Documents/MW1_Team_JSON/'      # provide the path indside single quotes, where all csv files are located
all_csv_files = glob.glob(path + "*.csv")
all_csv_files.sort()

get_concatenated_csv(all_csv_files)
remove_all_input_csv(path)
