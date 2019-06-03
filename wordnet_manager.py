#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree
import csv

class WordNetManger:
    def __init__(self, file_name):

        self.csv_path = "./"

        self.file_name = file_name

        # word nodes (property: lemma,pos)
        # csv title: lexiconId:ID,lemma,pos,:LABEL
        self.words = []
        # synsets nodes (property: id,def)
        # csv title: synsetId:ID,def,:LABEL
        self.synsets = []
        # relationships between words and synsets (property: pos)
        # csv title: :START_ID,pos,:END_ID,:TYPE
        self.rel_sence = []
        # relationships between synsets (property: relType)
        # csv title: :START_ID,relType,:END_ID,:TYPE
        self.rel_sementic = []

    def _parse(self):
        # XML ファイルから ElementTree オブジェクトを生成
        tree = ElementTree.parse(self.file_name)

        # 先頭要素を表す Element オブジェクトを取得
        root = tree.getroot()
        return root

    def create_csv_for_neo4j(self):

        print("Expending Wordnet...")
        self._expend_wordnet_in_memory()
        print("Done.")
        print("Generating csv files for neo4j importing...")
        self._create_nodes()
        self._create_relationships()
        print("Done.")


    def _expend_wordnet_in_memory(self):
        # neo4jインポート用のcsvファイルを作成
        root = self._parse()
        for child in root:
            # loopは3回のみなので、以下ifを入れても性能は大丈夫
            if child.tag == "Lexicon":
                for resource in child:
                    if resource.tag == "LexicalEntry":
                        lexicon_id = resource.attrib["id"]
                        for entry in resource:
                            if entry.tag == "Lemma":
                                word_lemma = entry.attrib["writtenForm"]
                                word_pos = entry.attrib["partOfSpeech"]

                                pos_label = ""
                                if word_pos == "n":
                                    pos_label = "Noun"
                                elif word_pos == "v":
                                    pos_label = "Verb"
                                elif word_pos == "a":
                                    pos_label = "Adjective"
                                elif word_pos == "r":
                                    pos_label = "Adverb"
                                else:
                                    pass
                                #print("Lemma:", word_lemma, word_pos)
                                self.words.append([lexicon_id, word_lemma, word_pos, "Word"])
                                #if pos_label == "":
                                #    self.words.append([lexicon_id, word_lemma, word_pos, "Word"])
                                #else:
                                #    self.words.append([lexicon_id, word_lemma, word_pos, "Word|"+pos_label])
                            elif entry.tag == "Sense":
                                synset_id = entry.attrib["synset"]
                                synset_pos = synset_id.split("-")[-1]
                                #print("  Sense synset id", synset_id)
                                self.rel_sence.append([lexicon_id, synset_pos, synset_id, "REL_SENCE"])
                            else:
                                pass
                    elif resource.tag == "Synset":
                        synset_id = resource.attrib["id"]
                        synset_pos = synset_id.split("-")[-1]
                        #print("Synset id", synset_id)

                        if resource[0].tag == "Definition":
                            definition = resource[0].attrib["gloss"]
                            #print("  Definition:", definition)
                            self.synsets.append([synset_id, definition, "Synset"])
                        else:
                            # Definitionがない場合はプロパティの値を空とする
                            #print("  Definition:", definition)
                            self.synsets.append([synset_id, "", "Synset"])

                        for entry in resource:
                            if entry.tag == "SynsetRelations":
                                for relation in entry:
                                    rel_target_id = relation.attrib["targets"]
                                    rel_target_type = relation.attrib["relType"]
                                    #print("    related synset:", rel_target_id, rel_target_type)
                                    self.rel_sementic.append([synset_id, rel_target_type, rel_target_id, "REL_SEMANTIC_LINK"])
                            else:
                                pass
                    else:
                        pass
            else:
                pass

    def _create_nodes(self):

        with open(self.csv_path + 'words.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["lexiconId:ID","lemma","pos",":LABEL"])
            writer.writerows(self.words)

        with open(self.csv_path + 'synsets.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["synsetId:ID","def",":LABEL"])
            writer.writerows(self.synsets)

    def _create_relationships(self):
        with open(self.csv_path + 'word_synset_relation.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([":START_ID","pos",":END_ID",":TYPE"])
            writer.writerows(self.rel_sence)

        with open(self.csv_path + 'synset_synset_relation.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([":START_ID","relType",":END_ID",":TYPE"])
            writer.writerows(self.rel_sementic)

if __name__ == "__main__":
    wordNetManger = WordNetManger("jpn_wn_lmf.xml")
    wordNetManger.create_csv_for_neo4j()