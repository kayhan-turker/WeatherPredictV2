import json
from scripts.utils import *


class LogManager:
    def __init__(self, log_file, log_fields, default_value, field_default_override, empty_id_value):
        self.log_file = log_file
        self.log_fields = log_fields
        self.default_value = default_value
        self.field_default_override = field_default_override
        self.empty_id_value = empty_id_value

    def get_default_field_value(self, field):
        return self.default_value if field not in self.field_default_override else self.field_default_override[field]

    def return_empty_field_dict(self):
        return {field: self.get_default_field_value(field) for field in self.log_fields}

    def return_empty_log_dict(self):
        return {self.empty_id_value: self.return_empty_field_dict()}

    def read_request_log(self):
        try:
            with open(self.log_file, 'r') as f:
                content = f.read().strip()
                request_log = json.loads(content) if content else self.return_empty_log_dict()
        except (FileNotFoundError, json.JSONDecodeError):
            print_log("WARNING", "File not found, empty, or invalid. Creating empty JSON log.")
            request_log = self.return_empty_log_dict()

        for source_id, field_dict in request_log.items():
            # If source id has no fields listed
            if field_dict is None or not isinstance(field_dict, dict):
                print_log("WARNING", f"Source {source_id} missing field dictionary! Field dictionary added.")
                field_dict = self.return_empty_field_dict()

            for field in self.log_fields:
                default_value = self.get_default_field_value(field)
                default_type = type(default_value)

                # If a field is missing
                if field not in field_dict:
                    print_log("WARNING", f"Source {source_id} missing field! Added field {field}.")
                    value = default_value
                else:
                    value = field_dict[field]
                    value_type = type(value)

                    # Check empty value for field
                    if value is None or value == "" or value == "null":
                        value = default_value
                    else:
                        # Otherwise is there a type mismatch?
                        if default_type is float or default_type is int:
                            value = re.sub(r'[^0-9.]]', '', value) if value_type is str else value
                            value = int(round(float(value))) if default_type is int else float(value)
                        elif default_type is str:
                            value = str(value)

                field_dict[field] = value
            request_log[source_id] = field_dict

        return request_log

    def write_request_log(self, json_data):
        with open(self.log_file, 'w') as f:
            f.write('{\n' + ',\n'.join(
                f'    "{key}": {json.dumps(value, separators=(",", ":"))}'
                for key, value in json_data.items()
            ) + '\n}')