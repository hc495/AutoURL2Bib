def is_utf8(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read()
        return True
    except UnicodeDecodeError:
        return False


class non_standard_entrance_replacement():
    def __init__(self):
        self.replacements = []
        self.original = []
        self.bad_entrances = ['@software']

    def encode(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                for bad_entrance in self.bad_entrances:
                    if line.startswith(bad_entrance):
                        self.original.append(bad_entrance)
                        line = line.replace(bad_entrance, '@article', 1)
                        self.replacements.append(line.strip())
                        # print(f"Replaced {bad_entrance} with @article.")
                file.write(line)

    def decode(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if line.startswith('@article') and line.strip() in self.replacements:
                    line = line.replace('@article', self.original[self.replacements.index(line.strip())], 1)
                file.write(line)