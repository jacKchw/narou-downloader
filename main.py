from narou_downloader import Novel

if __name__ == "__main__":
    n = Novel("n5194gp")
    print(n.title)
    n.save_all_novel("/home/jack/Downloads")
