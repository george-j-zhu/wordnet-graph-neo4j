from xml.etree import ElementTree

class WordNetManger:
    def __init__(self, file_name):
        self.file_name = file_name

    def _parse(self):
        # XML ファイルから ElementTree オブジェクトを生成
        tree = ElementTree.parse(self.file_name)

        # 先頭要素を表す Element オブジェクトを取得
        root = tree.getroot()
        return root

    def create_csv_for_neo4j(self):
        # neo4jインポート用のcsvファイルを作成
        root = self._parse()
        for child in root:
            # loopは3回のみなので、以下ifを入れても性能は大丈夫
            if child.tag == "Lexicon":
                for resource in child:
                    if resource.tag == "LexicalEntry":
                        for entry in resource:
                            if entry.tag == "Lemma":
                                print(entry.tag, entry.attrib)
                            else:
                                print(entry.tag, entry.attrib)
                        break
                    elif resource.tag == "Synset":
                        for entry in resource:
                            print(entry.tag, entry.attrib)
                        break
                    else:
                        pass

if __name__ == "__main__":
    wordNetManger = WordNetManger("jpn_wn_lmf.xml")
    wordNetManger.create_csv_for_neo4j()