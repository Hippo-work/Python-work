
#Generates each chunk only when needed — perfect for large datasets.
def read_in_chunks(file_obj, chunk_size=1024):
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data

for chunk in read_in_chunks(f):
    process = (chunk)
#Benefit: Avoids loading the entire file into memory





