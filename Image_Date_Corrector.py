import os
import re
from datetime import datetime
from win32_setctime import setctime as set_win32_creation_time

class ImageDateModifier:
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.error_files = []

    def extract_date_time(self, filename):
        pattern = r'(\d{4})[\-_]?(0[1-9]|1[0-2])[\-_]?(0[1-9]|[12][0-9]|3[01])[_-]?([0-1]?[0-9]|2[0-3])([0-5][0-9])?([0-5][0-9])?'
        match = re.search(pattern, filename)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            hour = int(match.group(4)) if match.group(4) else 0
            minute = int(match.group(5)) if match.group(5) else 0
            second = int(match.group(6)) if match.group(6) else 0
            return datetime(year, month, day, hour, minute, second)
        else:
            return None

    def extract_date(self, filename):
        pattern = r'(\d{4})[\-_]?(0[1-9]|1[0-2])[\-_]?(0[1-9]|[12][0-9]|3[01])'
        match = re.search(pattern, filename)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return datetime(year, month, day)
        else:
            return None

    def set_creation_date(self, file_path, date_time):
        os.utime(file_path, (date_time.timestamp(), date_time.timestamp()))
        set_win32_creation_time(file_path, date_time.timestamp())
        self.success_count += 1

    def get_current_time(self):
        return datetime.now()

    def process_files(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    date_time = self.extract_date_time(filename)
                    if date_time:
                        self.set_creation_date(file_path, date_time)
                    else:
                        date = self.extract_date(filename)
                        if date:
                            current_time = self.get_current_time()
                            new_date_time = datetime(date.year, date.month, date.day, current_time.hour, current_time.minute, current_time.second)
                            self.set_creation_date(file_path, new_date_time)
                except Exception as e:
                    self.error_count += 1
                    self.error_files.append(filename)
                    print(f"Error processing file: {filename} - {e}")

        print("Creation dates of images in folder updated successfully!")
        print("Number of files whose creation date changed:", self.success_count)
        print("Number of files that caused errors:", self.error_count)

        if self.error_files:
            print("\nFiles that caused errors:")
            for file in self.error_files:
                print(file)



# Example usage
folder_path = "Path to Image"
file_modifier = ImageDateModifier()
file_modifier.process_files(folder_path)
