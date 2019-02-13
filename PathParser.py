import json
import os
import ntpath
import re

CONFIGURATION_FILE = os.path.join(os.getcwd(), 'configuration.json')
REQUIRED_FIELDS    = ["category", "regex", "classify", "default", "data_type"]
"""
Class used to parse a path using the description provided by configuration.json
This will allow to break a path apart and create categories for searches.
"""
class PathParser:
    def __init__(self, path, study, configuration_file=CONFIGURATION_FILE):
        self.path      = path
        self.path_dict = {}

        with open(configuration_file) as stream:
            data = json.load(stream)

        data_pass, broken_path, needs_decomposition, study_data\
         = PathParser.qc_data(data, path, study)

        if data_pass and needs_decomposition:
            categories = [item["category"] for item in \
                            study_data["folder_structure"]]
            regex = [item["regex"] for item in\
                        study_data["folder_structure"]]
            classify = [item["classify"] for item in\
                            study_data["folder_structure"]]
            default = [item["default"] for item in\
                        study_data["folder_structure"]]
            data_type = [item["data_type"] for item in\
                        study_data["folder_structure"]]

            number_of_levels  = len(study_data["folder_structure"])
            root_index        = broken_path.index(study_data["root"])
            clean_broken_path = [broken_path[index] for index in \
                                    range(root_index + 1, len(broken_path))]

            if len(clean_broken_path) < len(categories):
                print("Structure after root folder is smaller than " + \
                        "defined in configuration.json file\n" + \
                        "Only classifying category up to: " + \
                        categories[len(clean_broken_path) - 1])

            for index, element in enumerate(clean_broken_path):

                try:
                    category_setting       = categories[index]
                    regex_setting          = regex[index]
                    classify_setting       = classify[index]
                    default_setting        = default[index]
                    data_type_setting      = data_type[index]

                    if classify_setting:
                        if regex_setting:
                            found_pattern = re.search(regex_setting, element)
                            if found_pattern:
                                element = found_pattern.group(0)
                            elif default != "same":
                                element = default

                        self.path_dict[category_setting] = {
                            "value": element,
                            "data_type": data_type_setting
                        }
                    else:
                        print("Classification skipped")
                except:
                    if index >= len(categories):
                        break
                    else:
                        print("Error found in  creation of path_dict with: " +\
                                element + " and index " + index)

    @classmethod
    def qc_data(cls, data, path, study):
        error       = False
        broken_path = []
        if data:
            if study in data:
                study_data      = data[study]
                structure_check = PathParser.check_study_structure(study_data)

                if structure_check:
                    broken_path = PathParser.split_path_into_components(path)
                    root        = study_data["root"]

                    if root in broken_path:
                        if not "needs_decomposition" in study_data:
                            error = True
                            print("needs_decomposition parameter not found")
                    else:
                        error = True
                        print('Root not in path for study ' + study + \
                                ' and path ' + path)
                else:
                    error = True
                    print("Check configuration structure for study: " + study)
            else:
                error = True
                print("Study: " + study + " not found in configuration file")
        else:
            error = True
            print("Issues loading configuration data")

        return (not error, broken_path, study_data["needs_decomposition"],\
            study_data)

    @classmethod
    def check_study_structure(cls, data_as_json):
        return "root" in data_as_json and "folder_structure" in data_as_json\
            and all((item in inner_dict for item in REQUIRED_FIELDS\
                    for inner_dict in data_as_json["folder_structure"]))

    @classmethod
    def split_path_into_components(cls, path):
        head, tail = ntpath.split(path)
        path_split = [tail]

        while head != "" and head != "/":
            head, tail = ntpath.split(head)
            path_split.append(tail)

        return path_split[::-1]
