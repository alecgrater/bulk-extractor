import os
import zipfile
import time
from tqdm import tqdm

def main(num_of_extracts=None):
    # Create 'iso' directory if it doesn't exist
    iso_dir = os.path.join(os.getcwd(), 'iso')
    os.makedirs(iso_dir, exist_ok=True)

    # Initialize the list of failed games
    failed_files = []

    # Get the list of zip files in the current directory
    zip_files = [file_name for file_name in os.listdir() if file_name.endswith('.zip')]

    # Limit the number of extracts if num_of_extracts is specified
    if num_of_extracts is not None:
        zip_files = zip_files[:num_of_extracts]

    # Iterate through the zip files
    for i, file_name in enumerate(zip_files, start=1):
        # Extract the zip file
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            iso_files = [name for name in zip_ref.namelist() if name.endswith('.iso')]
            if len(iso_files) == 1:
                # Extract the .iso file
                iso_file = iso_files[0]
                print(f"Starting extract for {i}. {file_name}: {iso_file}")
                with tqdm(total=100, ncols=80) as pbar:
                    zip_ref.extract(iso_file, iso_dir)
                    # Close the zip file before attempting to delete it
                    zip_ref.close()
                    time.sleep(1)  # Wait for a second
                    # Delete the zip file
                    os.remove(file_name)
                    # Update the progress bar to 100
                    pbar.update(99)

            elif len(iso_files) == 0:
                zip_ref.close()
                # Add the zip file to the list of failed games
                failed_files.append(file_name)
                # Delete the zip file
                os.remove(file_name)
                print (f"Failed to xtract for {i}. {file_name}, no .iso file found")


    # Create a text file to store the failed games
    with open('failed_files.txt', 'w') as file:
        file.write('\n'.join(failed_files))

# Call the main function
main()
