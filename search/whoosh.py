from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

import inspect
import os


def createSearchableData():
    root = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\txt"
    print(root)
    schema = Schema(title=TEXT(stored=True, phrase=False), path=ID(stored=True), textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    # Creating a index writer to add document as per schema
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    filepaths = [os.path.join(root, i) for i in os.listdir(root)]
    for path in filepaths:
        fp = open(path, 'r')
        # , encoding='UTF-8'
        text = fp.read()
        writer.add_document(title=path.split("\\")[7], path=path, textdata=text)
        fp.close()
    writer.commit()


def findQuery(query_str, topN):
    ix = open_dir("indexdir")
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        query = QueryParser("textdata", ix.schema, group=OrGroup).parse(query_str)
        results = searcher.search(query, limit=topN)

        r = []
        for hit in results:
            r.append(str(hit["title"]))
    return r

