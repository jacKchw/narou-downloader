import sys

sys.path.append(".")

from novel import Novel

if __name__ == "__main__":
    n = Novel("n1166fi")
    n.save_all_novel()
