class Achievement:
    def __init__(self, id: int, description: str, files: list, status: str, student_group: str, student_name: str):
        self.id = id
        self.description = description
        self.files = files
        self.status = status
        self.student_group = student_group
        self.student_name = student_name

    @staticmethod
    def from_row(row):
        id, description, files, status, student_group, student_name = row
        files_list = [tuple(file.split(':')) for file in files.split(',')] if files else []
        return Achievement(id, description, files_list, status, student_group, student_name)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'files': self.files,
            'status': self.status,
            'student_group': self.student_group,
            'student_name': self.student_name
        }


class User:
    def __init__(self, id: int, full_name: str, group_number: str, password: str):
        self.id = id
        self.full_name = full_name
        self.group_number = group_number
        self.password = password

    @staticmethod
    def from_row(row):
        id, full_name, group_number, password = row
        return User(id, full_name, group_number, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'group_number': self.group_number,
            'password': self.password
        }

