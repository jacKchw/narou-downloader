# narou-downloader

Extracting novels from https://syosetu.com/
Create a Novel object and use save_all_novel() to output as txt

Example:
n = Novel('n9595ez')
n.get_all_novel()
x = n.extract_content(5)
