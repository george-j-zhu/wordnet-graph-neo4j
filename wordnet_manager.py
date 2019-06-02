#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree

class WordNetManger:
    def __init__(self, file_name):
        self.file_name = file_name

        # word nodes (property: lemma,pos)
        self.words = {}
        # synsets nodes (property: id,def)
        self.synsets = {}
        # relationships between words and synsets (property: pos)
        self.rel_sence = {}
        # relationships between synsets (property: relType)
        self.rel_sementic = {}

    def _parse(self):
        # XML ファイルから ElementTree オブジェクトを生成
        tree = ElementTree.parse(self.file_name)

        # 先頭要素を表す Element オブジェクトを取得
        root = tree.getroot()
        return root

    def create_csv_for_neo4j(self):
        self._expend_xml_on_memory()

    def _expend_xml_on_memory(self):
        # neo4jインポート用のcsvファイルを作成
        root = self._parse()
        for child in root:
            # loopは3回のみなので、以下ifを入れても性能は大丈夫
            if child.tag == "Lexicon":
                for resource in child:
                    if resource.tag == "LexicalEntry":
                        word_id = resource.attrib["id"]
                        for entry in resource:
                            if entry.tag == "Lemma":
                                word_lemma = entry.attrib["writtenForm"]
                                word_pos = entry.attrib["partOfSpeech"]
                                print("Lemma:", word_lemma, word_pos)
                            elif entry.tag == "Sense":
                                synset_id = entry.attrib["synset"]
                                print("  Sense synset id", synset_id)
                            else:
                                pass
                    elif resource.tag == "Synset":
                        synset_id = resource.attrib["id"]
                        synset_pos = synset_id.split("-")[-1]
                        print("Synset id", synset_id)
                        for entry in resource:
                            if entry.tag == "Definition":
                                definition = entry.attrib["gloss"]
                                print("  Definition:", definition)
                            elif entry.tag == "SynsetRelations":
                                for relation in entry:
                                    rel_target_id = relation.attrib["targets"]
                                    rel_target_type = relation.attrib["relType"]
                                    print("    related synset:", rel_target_id, rel_target_type)
                            else:
                                pass
                    else:
                        pass
            else:
                pass

    def _create_node(self):
        pass

    def _create_relationship(self):
        pass

if __name__ == "__main__":
    wordNetManger = WordNetManger("jpn_wn_lmf.xml")
    wordNetManger.create_csv_for_neo4j()