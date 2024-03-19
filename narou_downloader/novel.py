import os
from bs4 import BeautifulSoup
import urllib
import codecs
import time
import re
import requests
import datetime

base_url = "https://ncode.syosetu.com/"
output_path = "download"


class Novel:
    def __init__(self, novel_id):
        self.id = novel_id
        self.url = base_url + novel_id + "/"
        self.info = self.__search()
        self.title = re.sub(r'[<>:/"|?*\\]', "", str(self.info["Title"]))
        self.folderName = os.path.join(output_path, self.title)

        self.chapter_dig = len(str(self.info["Chapter Number"]))

    def __repr__(self):
        return "Novel" + str(self.info)

    def save_all_novel(self, sep=False, chapterRange=None):
        """
        Parameters
        ----------
        sep : boolen, optional
            If True, output txt files seperately. The default is False.
        chapterRange : range, optional
            Range of extracted chapters. Extract all if None. The default is None.

        Returns
        -------
        None.

        """
        self.__create_folder(sep)
        # all novel text
        if type(chapterRange) != range:
            chapterRange = range(1, self.info["Chapter Number"] + 1)
        for chapter in chapterRange:
            d = self.extract_content(chapter)
            self.__write_txt(d, sep)
            if chapter % 10 == 0:
                print("{} items are loaded".format(chapter))
            time.sleep(1)

    def get_all_novel(self):
        novel_list = []
        for chapter in range(1, self.info["Chapter Number"] + 1):
            novel_list.append(self.extract_content(chapter))
        return novel_list

    def get_novel_words(self, limit):
        novel_list = []
        words, chapter = 0, 0
        while True:
            chapter += 1
            try:
                d = self.extract_content(chapter)
                novel_list.append(d)
                words += len(d["text"])
                if words > limit:
                    break
            except:
                break

        return novel_list

    def __search(self):
        # use API to search for novel metadata
        payload = {
            "out": "json",
            "of": "t-w-nt-ga",
            "ncode": self.id,
        }

        response = requests.get(
            "https://api.syosetu.com/novelapi/api/",
            params=payload,
        )
        json_response = response.json()[1]
        info = {
            "Novel Code": self.id,
            "Title": json_response["title"],
            "Writer": json_response["writer"],
            "Chapter Number": json_response["general_all_no"],
            "Retrieval  Date": str(datetime.datetime.now()),
        }
        info["Serial"] = True if json_response["noveltype"] == 1 else False
        return info

    def __get_soup(self, page_url):
        req = urllib.request.Request(
            page_url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def extract_content(self, chapter):
        # get one chapter
        if self.info["Serial"]:
            soup = self.__get_soup(self.url + str(chapter) + "/")
            subtitle = soup.find("p", attrs={"class": "novel_subtitle"}).get_text()
        else:
            soup = self.__get_soup(self.url)
            subtitle = self.info["Title"]

        text = soup.find(id="novel_honbun").get_text()
        return {"chapter": chapter, "subtitle": subtitle, "text": text}

    def __create_folder(self, sep):
        try:
            os.mkdir(output_path)
        except:
            pass

        # create folder
        count = 0
        while True:
            try:
                if count != 0:
                    self.folderName = os.path.join(
                        output_path, self.title + "_" + str(count).zfill(2)
                    )
                os.mkdir(self.folderName)
                break
            except FileExistsError:
                count += 1

        # create info section
        txt = "\n".join(
            [str(key) + ": " + str(item) for key, item in self.info.items()]
        )
        txt += "\n\n\n"
        path = (
            os.path.join(self.folderName, "info.txt")
            if sep
            else os.path.join(self.folderName, self.title + ".txt")
        )
        with codecs.open(path, "w", encoding="utf8") as f:
            f.write(txt)

    def __write_txt(self, d, sep):
        # create txt file
        if sep:
            chapterNum = str(d["chapter"]).zfill(self.chapter_dig)
            subtitle = re.sub(r'[<>:/"|?*\\]', "", str(d["subtitle"]))
            fileName = chapterNum + "_" + subtitle
            with codecs.open(
                os.path.join(self.folderName, fileName + ".txt"), "w", encoding="utf8"
            ) as f:
                f.write(d["text"])
        else:
            with codecs.open(
                os.path.join(self.folderName, self.title + ".txt"), "a", encoding="utf8"
            ) as f:
                f.write(
                    str(d["chapter"])
                    + " "
                    + d["subtitle"]
                    + "\n\n"
                    + d["text"]
                    + "\n\n\n\n"
                )
