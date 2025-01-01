import os
import csv
import pandas as pd
import argparse
from datetime import datetime
def is_positive_integer(value):
    return value.isdigit() and int(value) > 0
def is_natural_integer(value):
    return value.isdigit() and int(value) >= 0
def is_decimal(value):
    try:
        float_value = float(value)
        return '.' in value and float_value == float(value)
    except ValueError:
        return False
def is_date(value):
    if value == '':
        return True
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False
def is_timestamp(value):
    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return True
    except ValueError:
        return False
def validate_csv(file_path):
    errors = []
    data_type_checks = {
        'subject': is_positive_integer,
        '类型': lambda x: x in {'1', '2', '3', '4', '6'},
        'VIB评分': is_decimal,
        'VIB标准差': is_decimal,
        'VIB评分数': is_positive_integer,
        '1.1': is_natural_integer,
        '2.1': is_natural_integer,
        '3.1': is_natural_integer,
        '4.1': is_natural_integer,
        '5.1': is_natural_integer,
        '6.1': is_natural_integer,
        '7.1': is_natural_integer,
        '8.1': is_natural_integer,
        '9.1': is_natural_integer,
        '10.1': is_natural_integer,
        '表面排名': is_natural_integer,
        '表面评分数': is_positive_integer,
        '表面评分': is_decimal,
        '1.2': is_natural_integer,
        '2.2': is_natural_integer,
        '3.2': is_natural_integer,
        '4.2': is_natural_integer,
        '5.2': is_natural_integer,
        '6.2': is_natural_integer,
        '7.2': is_natural_integer,
        '8.2': is_natural_integer,
        '9.2': is_natural_integer,
        '10.2': is_natural_integer,
        '是否被锁定': lambda x: x in {'True', 'False'},
        '发布发售放送时间': is_date,
        'NSFW': lambda x: x in {'True', 'False'},
        '搁置': is_natural_integer,
        '抛弃': is_natural_integer,
        '想': is_natural_integer,
        '已': is_natural_integer,
        '在': is_natural_integer,
        'is1': is_natural_integer,
        'is2': is_natural_integer,
        'is3': is_natural_integer,
        'is4': is_natural_integer,
        'is5': is_natural_integer,
        'is6': is_natural_integer,
        'is7': is_natural_integer,
        'is8': is_natural_integer,
        'is9': is_natural_integer,
        'is10': is_natural_integer,
        'is11': is_natural_integer,
        'is12': is_natural_integer,
        'is13': is_natural_integer,
        'is14': is_natural_integer,
        'is15': is_natural_integer,
        'is16': is_natural_integer,
        'is17': is_natural_integer,
        'is18': is_natural_integer,
        'is19': is_natural_integer,
        'is20': is_natural_integer,
        'is21': is_natural_integer,
        'is22': is_natural_integer,
        'is23': is_natural_integer,
        'is24': is_natural_integer,
        'is25': is_natural_integer,
        'is26': is_natural_integer,
        'is27': is_natural_integer,
        'is28': is_natural_integer,
        'is29': is_natural_integer,
        'is30': is_natural_integer,
        'is31': is_natural_integer,
        'is32': is_natural_integer,
        'is33': is_natural_integer,
        'is34': is_natural_integer,
        'is35': is_natural_integer,
        'is36': is_natural_integer,
        'is37': is_natural_integer,
        'is38': is_natural_integer,
        'is39': is_natural_integer,
        'is40': is_natural_integer,
        'is41': is_natural_integer,
        'is42': is_natural_integer,
        'is43': is_natural_integer,
        'is44': is_natural_integer,
        'is45': is_natural_integer,
        'is46': is_natural_integer,
        'is47': is_natural_integer,
        'is48': is_natural_integer,
        'is49': is_natural_integer,
        'is50': is_natural_integer,
        'ad1': is_natural_integer,
        'ad2': is_natural_integer,
        'ad3': is_natural_integer,
        'ad4': is_natural_integer,
        'ad5': is_natural_integer,
        'ad6': is_natural_integer,
        'ad7': is_natural_integer,
        'ad8': is_natural_integer,
        'ad9': is_natural_integer,
        'ad10': is_natural_integer,
        'ad11': is_natural_integer,
        'ad12': is_natural_integer,
        'ad13': is_natural_integer,
        'ad14': is_natural_integer,
        'ad15': is_natural_integer,
        'ad16': is_natural_integer,
        'ad17': is_natural_integer,
        'ad18': is_natural_integer,
        'ad19': is_natural_integer,
        'ad20': is_natural_integer,
        'ad21': is_natural_integer,
        'ad22': is_natural_integer,
        'ad23': is_natural_integer,
        'ad24': is_natural_integer,
        'ad25': is_natural_integer,
        'ad26': is_natural_integer,
        'ad27': is_natural_integer,
        'ad28': is_natural_integer,
        'ad29': is_natural_integer,
        'ad30': is_natural_integer,
        'tc1': is_natural_integer,
        'tc2': is_natural_integer,
        'tc3': is_natural_integer,
        'tc4': is_natural_integer,
        'tc5': is_natural_integer,
        'tc6': is_natural_integer,
        'tc7': is_natural_integer,
        'tc8': is_natural_integer,
        'tc9': is_natural_integer,
        'tc10': is_natural_integer,
        'tc11': is_natural_integer,
        'tc12': is_natural_integer,
        'tc13': is_natural_integer,
        'tc14': is_natural_integer,
        'tc15': is_natural_integer,
        'tc16': is_natural_integer,
        'tc17': is_natural_integer,
        'tc18': is_natural_integer,
        'tc19': is_natural_integer,
        'tc20': is_natural_integer,
        'tc21': is_natural_integer,
        'tc22': is_natural_integer,
        'tc23': is_natural_integer,
        'tc24': is_natural_integer,
        'tc25': is_natural_integer,
        'tc26': is_natural_integer,
        'tc27': is_natural_integer,
        'tc28': is_natural_integer,
        'tc29': is_natural_integer,
        'tc30': is_natural_integer,
        'tc31': is_natural_integer,
        'tc32': is_natural_integer,
        'tc33': is_natural_integer,
        'tc34': is_natural_integer,
        'tc35': is_natural_integer,
        'tc36': is_natural_integer,
        'tc37': is_natural_integer,
        'tc38': is_natural_integer,
        'tc39': is_natural_integer,
        'tc40': is_natural_integer,
        'tc41': is_natural_integer,
        'tc42': is_natural_integer,
        'tc43': is_natural_integer,
        'tc44': is_natural_integer,
        'tc45': is_natural_integer,
        'tc46': is_natural_integer,
        'tc47': is_natural_integer,
        'tc48': is_natural_integer,
        'tc49': is_natural_integer,
        'tc50': is_natural_integer,
        'tc51': is_natural_integer,
        'tc52': is_natural_integer,
        'tc53': is_natural_integer,
        'tc54': is_natural_integer,
        'tc55': is_natural_integer,
        'tc56': is_natural_integer,
        'tc57': is_natural_integer,
        'tc58': is_natural_integer,
        'tc59': is_natural_integer,
        'tc60': is_natural_integer,
        'tc61': is_natural_integer,
        'tc62': is_natural_integer,
        'tc63': is_natural_integer,
        'tc64': is_natural_integer,
        'tc65': is_natural_integer,
        'tc66': is_natural_integer,
        'tc67': is_natural_integer,
        'tc68': is_natural_integer,
        'tc69': is_natural_integer,
        'tc70': is_natural_integer,
        'tc71': is_natural_integer,
        'tc72': is_natural_integer,
        'tc73': is_natural_integer,
        'tc74': is_natural_integer,
        'tc75': is_natural_integer,
        'tc76': is_natural_integer,
        'tc77': is_natural_integer,
        'tc78': is_natural_integer,
        'tc79': is_natural_integer,
        'tc80': is_natural_integer,
        'rd1': is_natural_integer,
        'rd2': is_natural_integer,
        'rd3': is_natural_integer,
        'rd4': is_natural_integer,
        'rd5': is_natural_integer,
        'rd6': is_natural_integer,
        'rd7': is_natural_integer,
        'rd8': is_natural_integer,
        'rd9': is_natural_integer,
        'rd10': is_natural_integer,
        'rd11': is_natural_integer,
        'rd12': is_natural_integer,
        'rd13': is_natural_integer,
        'rd14': is_natural_integer,
        'rd15': is_natural_integer,
        'rd16': is_natural_integer,
        'rd17': is_natural_integer,
        'rd18': is_natural_integer,
        'rd19': is_natural_integer,
        'rd20': is_natural_integer,
        'rd21': is_natural_integer,
        'rd22': is_natural_integer,
        'rd23': is_natural_integer,
        'rd24': is_natural_integer,
        'rd25': is_natural_integer,
        'rd26': is_natural_integer,
        'rd27': is_natural_integer,
        'rd28': is_natural_integer,
        'rd29': is_natural_integer,
        'rd30': is_natural_integer,
        'rd31': is_natural_integer,
        'rd32': is_natural_integer,
        'rd33': is_natural_integer,
        'rd34': is_natural_integer,
        'rd35': is_natural_integer,
        'rd36': is_natural_integer,
        'rd37': is_natural_integer,
        'rd38': is_natural_integer,
        'rd39': is_natural_integer,
        'rd40': is_natural_integer,
        'rd41': is_natural_integer,
        'rd42': is_natural_integer,
        'rd43': is_natural_integer,
        'rd44': is_natural_integer,
        'rd45': is_natural_integer,
        'rd46': is_natural_integer,
        'rd47': is_natural_integer,
        'rd48': is_natural_integer,
        'rd49': is_natural_integer,
        'rd50': is_natural_integer,
        'rd51': is_natural_integer,
        'rd52': is_natural_integer,
        'rd53': is_natural_integer,
        'rd54': is_natural_integer,
        'rd55': is_natural_integer,
        'rd56': is_natural_integer,
        'rd57': is_natural_integer,
        'rd58': is_natural_integer,
        'rd59': is_natural_integer,
        'rd60': is_natural_integer,
        'rd61': is_natural_integer,
        'rd62': is_natural_integer,
        'rd63': is_natural_integer,
        'rd64': is_natural_integer,
        'rd65': is_natural_integer,
        'rd66': is_natural_integer,
        'rd67': is_natural_integer,
        'rd68': is_natural_integer,
        'rd69': is_natural_integer,
        'rd70': is_natural_integer,
        'qd1': is_natural_integer,
        'qd2': is_natural_integer,
        'qd3': is_natural_integer,
        'qd4': is_natural_integer,
        'qd5': is_natural_integer,
        'qd6': is_natural_integer,
        'qd7': is_natural_integer,
        'qd8': is_natural_integer,
        'qd9': is_natural_integer,
        'qd10': is_natural_integer,
        'qd11': is_natural_integer,
        'qd12': is_natural_integer,
        'qd13': is_natural_integer,
        'qd14': is_natural_integer,
        'qd15': is_natural_integer,
        'qd16': is_natural_integer,
        'qd17': is_natural_integer,
        'qd18': is_natural_integer,
        'qd19': is_natural_integer,
        'qd20': is_natural_integer,
        'qd21': is_natural_integer,
        'qd22': is_natural_integer,
        'qd23': is_natural_integer,
        'qd24': is_natural_integer,
        'qd25': is_natural_integer,
        'qd26': is_natural_integer,
        'qd27': is_natural_integer,
        'qd28': is_natural_integer,
        'qd29': is_natural_integer,
        'qd30': is_natural_integer,
        'qd31': is_natural_integer,
        'qd32': is_natural_integer,
        'qd33': is_natural_integer,
        'qd34': is_natural_integer,
        'qd35': is_natural_integer,
        'qd36': is_natural_integer,
        'qd37': is_natural_integer,
        'qd38': is_natural_integer,
        'qd39': is_natural_integer,
        'qd40': is_natural_integer,
        'qd41': is_natural_integer,
        'qd42': is_natural_integer,
        'qd43': is_natural_integer,
        'qd44': is_natural_integer,
        'qd45': is_natural_integer,
        'qd46': is_natural_integer,
        'qd47': is_natural_integer,
        'qd48': is_natural_integer,
        'qd49': is_natural_integer,
        'qd50': is_natural_integer,
        'qd51': is_natural_integer,
        'qd52': is_natural_integer,
        'qd53': is_natural_integer,
        'qd54': is_natural_integer,
        'qd55': is_natural_integer,
        'qd56': is_natural_integer,
        'qd57': is_natural_integer,
        'qd58': is_natural_integer,
        'qd59': is_natural_integer,
        'qd60': is_natural_integer,
        'qd61': is_natural_integer,
        'qd62': is_natural_integer,
        'qd63': is_natural_integer,
        'qd64': is_natural_integer,
        'qd65': is_natural_integer,
        'qd66': is_natural_integer,
        'qd67': is_natural_integer,
        'qd68': is_natural_integer,
        'qd69': is_natural_integer,
        'qd70': is_natural_integer,
        '更新时间': is_timestamp,
        '表面标准差': is_decimal,
        'VIB朴素排名': is_natural_integer,
        '类型内VIB总平均分': is_decimal,
        '类型内前250的最小VIB评分数': is_natural_integer,
        '类型内加权VIB平均分': is_decimal,
        'VIB加权排名': is_natural_integer
    }
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            lines = list(csvreader)
            if len(lines) == 0:
                errors.append("file is empty")
                return errors
    except Exception as e:
        errors.append(f"cannot be opened by csv module: {e}")
        return errors
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        errors.append(f"cannot be opened by pandas module: {e}")
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if line.strip() == '':
                errors.append(f"line {i+1} is empty")
    with open(file_path, 'rb') as f:
        for i, line in enumerate(f):
            if not line.endswith(b'\r\n'):
                errors.append(f"line {i+1} does not end with CRLF")
    column_count = len(lines[0]) if lines else 0
    for i, row in enumerate(lines):
        if len(row) != column_count:
            errors.append(f"line {i+1} has {len(row)} columns, expected {column_count}")
    if not errors:
        header = lines[0]
        for i, row in enumerate(lines[1:], start=2):
            for col_name, check_func in data_type_checks.items():
                if col_name in header:
                    index = header.index(col_name)
                    if not check_func(row[index]):
                        errors.append(f"line {i} column '{col_name}' has invalid data: {row[index]}")
    return errors
def main(directory):
    all_valid = True
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            errors = validate_csv(file_path)
            if errors:
                all_valid = False
                print(f"{filename}:")
                for error in errors:
                    print(f"  - {error}")
            else:
                print(f"{filename} is valid.")
    if all_valid:
        print("All CSVs are valid.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate CSV files in a directory.')
    parser.add_argument('directory', type=str, help='The directory containing CSV files to validate.')
    args = parser.parse_args()
    main(args.directory)
