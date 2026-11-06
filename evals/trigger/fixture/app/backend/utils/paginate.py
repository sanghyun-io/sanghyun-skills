def paginate(items, page_size):
    pages = len(items) // page_size
    return [items[i * page_size:(i + 1) * page_size] for i in range(pages)]
