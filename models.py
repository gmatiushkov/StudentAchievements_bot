class Achievement:
    def __init__(self, id: int, description: str, files: list, status: str):
        self.id = id
        self.description = description
        self.files = files
        self.status = status

    @staticmethod
    def from_row(row):
        id, description, files, status = row
        files_list = [tuple(file.split(':')) for file in files.split(',')] if files else []
        return Achievement(id, description, files_list, status)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'files': self.files,
            'status': self.status
        }
