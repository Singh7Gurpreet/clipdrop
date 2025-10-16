class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def write_to_file(self, content):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            print(f"Error writing to file: {e}")

    def read_from_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = file.read()
            print(f"Successfully read from {self.filename}")
            return data
        except FileNotFoundError:
            print(f"File not found: {self.filename}")
            return ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
