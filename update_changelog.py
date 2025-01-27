import datetime
import json
from collections import defaultdict
from file_selector import get_and_select_files
import secrets

json_data_file = "changelog.json"
changelog_file = "CHANGELOG.md"


def print_json_data(obj: dict, indent=2):
    print(json.dumps(obj, indent=indent))


def generate_operation_id():
    return secrets.token_hex(16)


OPERATIONS = [
    "ADD",
    "REMOVE",
    "UPDATE",
    "FIX",
    "REFRACTOR",
    "STYLE",
    "TEST",
    "DOCS",
]


class Node:
    def __init__(self, path, description, node_type):
        self.path = path
        self.description = description
        self.type = node_type
        self.parent: Node = None
        self.children: dict = {}
        self.is_file = False
        self.name = path.split("/")[-1]
        self.is_root = False
        self.root = self.get_root()

    def get_root(self):
        if self.is_root or not self.parent:
            return self
        return self.parent.get_root()


class Directory(Node):
    def __init__(self, path, description=None):
        super().__init__(path, description, "directory")
        self.is_root = path == "."
        if self.is_root:
            self.parent = None
        parents = path.split("/")
        self.name = parents[-1]
        parents.pop()
        if not parents:
            self.parent = Directory(".")

        self.parent = Directory("/".join(parents))

    def add_file(self, file):
        self.children[file.name] = file
        file.parent = self


class File(Node):
    def __init__(self, path, description=None):
        super().__init__(path, description, "file")
        self.parent = Directory("/".join(path.split("/")[:-1]))


class Operation:
    def __init__(self, operation: str, modified_zone: str, explanation: str):
        self.operation = operation
        self.modified_zone = modified_zone
        self.explanation = explanation
        self.modified_files_map = {}

    def add_modified_file(self, file_path, explanation):
        self.modified_files_map[file_path] = explanation


def input_operation_dict():
    operation_type = (
        input(f"Enter the type of operation ({', '.join(OPERATIONS)}): ")
        .upper()
        .strip()
    )
    if operation_type not in OPERATIONS:
        print("Invalid operation type")
        return
    modified_zone = input("Enter the modified zone: ").strip()
    explanation = input("Enter the explanation of the operation: ").strip()
    return {
        "operation": operation_type,
        "modified_zone": modified_zone,
        "explanation": explanation,
        "operation_id": generate_operation_id(),
    }


def update_changelog(recompile=False, update_commit_msg=True):
    # open or create the json file
    try:
        json_file = open(json_data_file, "r")
        data = json.load(json_file)
        data = defaultdict(list, data)
    except FileNotFoundError:
        data = defaultdict(list)
    last_operation = None

    last_date_str = list(data.keys())[0] if data else None
    if not recompile :
        last_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        last_operation = input_operation_dict()
        modified_files = get_and_select_files()
        last_operation["modified_files"] = {
            file_path: {"description": ""} for file_path in modified_files
        }
        for modified_file in modified_files:
            explanation = input(
                f"Enter the explanation for the modification of {modified_file}: "
            )

            last_operation["modified_files"][modified_file]["description"] = explanation
        data[last_date_str].append(last_operation)
    if update_commit_msg and last_date_str:

        last_operation = last_operation or data[last_date_str][-1]
        with open(".git/COMMIT_MSG", "w") as commit_msg:
            commit_msg.write(
                f"{last_operation['operation']}({last_operation['modified_zone']}): {last_operation['explanation']}"
            )
    # sort the data by date
    data_to_save = dict(data)
    data_to_save = dict(sorted(data_to_save.items(), reverse=True))
    with open(changelog_file, "w") as changelog:
        # Begin to write the new changelog
        changelog.write(f"# CHANGELOG\n\n")
        for date, operations in data_to_save.items():
            changelog.write(f"## {date}\n")
            for operation in operations:
                if "operation_id" not in operation:
                    operation["operation_id"] = generate_operation_id()
                operation_obj = operation
                operation_name = operation_obj["operation"]
                modified_zone = operation_obj["modified_zone"]
                modification = operation_obj["explanation"]
                changelog.write(
                    f"- **{operation_name}**(`{modified_zone}`): {modification}\n"
                )
                modified_files = operation_obj.get("modified_files", {})
                distincts_directories_to_files = {}
                directory = ""
                for file_path in modified_files:
                    directory = "/".join(file_path.split("/")[:-1])
                    distincts_directories_to_files[directory] = (
                        distincts_directories_to_files.get(directory, [])
                    )
                    distincts_directories_to_files[directory].append(file_path)

                # print_json_data(distincts_directories_to_files)

                for directory, files in distincts_directories_to_files.items():
                    dir_path = directory
                    if directory.startswith("./"):
                        dir_path = directory[2:]

                    changelog.write(f"  - **[{dir_path}](./{dir_path})**\n")
                    for file_path in files:
                        file_name = file_path.split("/")[-1]
                        semicolon = (
                            ":" if modified_files[file_path].get("description") else ""
                        )
                        changelog.write(
                            f"    - [{file_name}](./{file_path}){semicolon}"
                        )

                        if modified_files[file_path].get("description"):
                            changelog.write(
                                f" {modified_files[file_path]['description']}\n"
                            )
                        else:
                            changelog.write("\n")
            changelog.write("\n")
    # reverse the data to make the latest date at the top
    with open(json_data_file, "w") as json_file:
        json.dump(data_to_save, json_file, indent=2)


if __name__ == "__main__":
    import sys

    recompile = len(sys.argv) > 1 and sys.argv[1] == "recompile"
    update_changelog(recompile=recompile)
