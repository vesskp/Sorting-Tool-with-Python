import sys
from collections import Counter

def log_message(message, file_name=""):
    if file_name:
        with open(file_name, "a") as f:
            f.write(message + "\n")
    else:
        print(message)


def read_lines(file_name=""):
    lines = ""
    if file_name:
        with open(file_name, "r") as f:
            lines = f.read()
    else:
        while True:
            try:
                data = input()
                if data:
                    lines += data + "\n"
            except EOFError:
                break
    return lines


def parse_input(data_type, file_name=""):
    input_data = read_lines(file_name)

    if data_type == 'long':
        data = []
        for item in list(map(str, input_data.split())):
            if item.replace("-", "").isdigit():
                data.append(int(item))
            else:
                print(f'"{item}" is not a long. It will be skipped.')
        return data
    elif data_type == 'line':
        return input_data.splitlines()
    elif data_type == 'word':
        return input_data.split()
    else:
        raise ValueError("Invalid data type. Expected 'long', 'line', or 'word'.")


def calculate_and_print_results(data, data_type, sort_type, file_name=""):
    total_count = len(data)
    counter = Counter(data)

    if data_type == 'long':
        greatest = max(data)
        occurrence = counter[greatest]
    else:
        greatest = max(data, key=lambda x: (len(x), x))
        occurrence = counter[greatest]

    percentage = (occurrence * 100) // total_count

    log_message(f"Total {data_type}s: {total_count}.", file_name)

    if sort_type == 'natural':
        if data_type == 'long' or data_type == 'word':
            d = list(map(str, (sorted(data))))
            log_message(f"Sorted data: {" ".join(d)}", file_name)
        elif data_type == 'line':
            d = sorted(data)
            log_message("Sorted data:", file_name)
            for line in d:
                log_message(line, file_name)
    elif sort_type == 'byCount':
        count_dict = {item: data.count(item) for item in set(data)}
        percentage_list = {}
        for value, key in count_dict.items():
            if key not in percentage_list:
                percentage_list[key] = []
            percentage_list[key].append(value)
        keys = sorted(percentage_list.keys(), reverse=False)
        for key in keys:
            value = percentage_list[key]
            if data_type == 'long':
                value = sorted(list(map(int, value)))
            elif data_type == 'word' or data_type == 'line':
                value = sorted(list(map(str, value)))

            value = list(map(str, value))
            for v in value:
                log_message(f"{v}: {key} time(s), {key * 100 // total_count}%", file_name)

    else:
        if data_type == 'line':
            msg = f"The longest line:\n{greatest}\n"
        else:
            msg = f"The greatest {data_type}: {greatest}"

        msg += f" ({occurrence} time(s), {percentage}%)."
        log_message(msg, file_name)


def main():
    args = sys.argv[1:]
    data_type = 'word'  # Default data type
    sort_type = 'natural'  # Default sorting type
    input_file = ""
    output_file = ""

    for arg in args:
        if arg.startswith('-') and arg not in ['-sortingType', '-dataType', '-inputFile', '-outputFile']:
            print(f'"{arg}" is not a valid parameter. It will be skipped.')
    if '-sortingType' in args:
        try:
            sort_type = args[args.index('-sortingType') + 1]
            if sort_type not in ['natural', 'byCount']:
                print("No sorting type defined!")
                return
        except IndexError:
            print("No sorting type defined!")
            return
    if '-dataType' in args:
        try:
            data_type = args[args.index('-dataType') + 1]
            if data_type not in ['long', 'line', 'word']:
                print("No data type defined!")
                return
        except IndexError:
            print("No data type defined!")
            return
    if '-inputFile' in args:
        try:
            input_file = args[args.index('-inputFile') + 1]
        except IndexError:
            print("No data type defined!")
            return
    if '-outputFile' in args:
        try:
            output_file = args[args.index('-outputFile') + 1]
        except IndexError:
            print("No data type defined!")
            return

    if output_file:
        with open(output_file, "w") as f:
            f.write("")

    try:
        data = parse_input(data_type, input_file)
        calculate_and_print_results(data, data_type, sort_type, output_file)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
