import os

def last_lines(path, buffer_size=4096):
    with open(path, 'rb') as f:
        file_size = f.seek(0, os.SEEK_END)
        buffer = b""
        position = file_size
        # decoder = lambda b: b.decode('utf-8', errors='replace')  # fail-safe
        decoder = lambda b: b.decode('utf-8', errors='strict')  # fail-safe

        while position > 0:
            read_size = min(buffer_size, position)
            position -= read_size
            f.seek(position)
            chunk = f.read(read_size)
            buffer = chunk + buffer

            try:
                text = decoder(buffer)
            except UnicodeDecodeError:
                continue  # keep accumulating until decodable

            lines = text.splitlines(keepends=True)
            if position > 0 and not text.startswith(tuple('\r\n')):
                incomplete = lines.pop(0)
                buffer = incomplete.encode('utf-8')  # try again later
            else:
                buffer = b""

            for line in reversed(lines):
                yield line

        if buffer:
            try:
                yield decoder(buffer)
            except UnicodeDecodeError:
                raise ValueError("Unable to decode remaining buffer as UTF-8")
