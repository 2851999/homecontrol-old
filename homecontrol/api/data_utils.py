import os
from typing import Any, Callable, List, Optional


def read_last_lines(
    path: str,
    count: int,
    step: Optional[int],
    parse_func: Callable[[str], Any] = lambda line: line,
) -> List[Any]:
    """
    Reads last 'count' lines moving in steps of 'step'
    Returns list of data obtained by parsing each line of the file with
    'parse_func'
    """

    data_from_file = []
    with open(path, "rb") as file:
        # https://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-similar-to-tail
        total_lines_wanted = count * (1 if step is None else step)

        BLOCK_SIZE = 1024
        file.seek(0, 2)
        block_end_byte = file.tell()
        lines_to_go = total_lines_wanted
        block_number = -1
        blocks = []
        while lines_to_go > 0 and block_end_byte > 0:
            if block_end_byte - BLOCK_SIZE > 0:
                file.seek(block_number * BLOCK_SIZE, 2)
                blocks.append(file.read(BLOCK_SIZE))
            else:
                file.seek(0, 0)
                blocks.append(file.read(block_end_byte))
            lines_found = blocks[-1].count(b"\n")
            lines_to_go -= lines_found
            block_end_byte -= BLOCK_SIZE
            block_number -= 1
        all_read_text = b"".join(reversed(blocks))
        data_from_file = all_read_text.splitlines()[-total_lines_wanted::step]

    # Convert loaded data to required format
    # TODO: Try and do this above
    data = []
    for line in data_from_file:
        data.append(parse_func(line.decode()))
    return data


def read_all_lines(
    path: str, step: Optional[int], parse_func: Callable[[str], Any] = lambda line: line
) -> List[Any]:
    """
    Returns list of data obtained by parsing each line of a file with
    'parse_func'
    """

    data = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(parse_func(line))

            # Skip as required
            if step is not None:
                for _i in range(step - 1):
                    file.readline()
    return data
