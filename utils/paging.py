# utils/paging.py
def page_count(total_items, page_size):
    return (total_items + page_size - 1) // page_size

def get_page_items(items, page, page_size):
    start = page * page_size
    return items[start:start+page_size]
