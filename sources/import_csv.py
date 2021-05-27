from os import path
from csv import DictReader
from sources.models.company_model import CompanyModel


class WantedCSVReader:
    def __init__(self) -> None:
        self.f = open(path.dirname(__file__) + "/wanted_temp_data.csv", "r")
        self.reader = DictReader(f=self.f)

    def __del__(self):
        self.f.close()

    def readline(self):
        for _ in self.reader:
            c_name_ko = _.get("company_ko")
            c_name_en = _.get("company_en")
            c_name_jp = _.get("company_ja")

            locale_name = {}
            search_name_list = []
            if c_name_ko:
                locale_name["ko"] = c_name_ko
                search_name_list.append(c_name_ko)
            if c_name_en:
                locale_name["en"] = c_name_en
                search_name_list.append(c_name_en)
            if c_name_jp:
                locale_name["jp"] = c_name_jp
                search_name_list.append(c_name_jp)

            search_name = ", ".join(search_name_list)
            tag_ids = _.get("tag_ko").strip().split("|")

            # print(search_name, locale_name, tag_ids)
            yield search_name, locale_name, tag_ids


if __name__ == "__main__":
    wcr = WantedCSVReader()
    for _ in wcr.readline():
        print(_[2])
