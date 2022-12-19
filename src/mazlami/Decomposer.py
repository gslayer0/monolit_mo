import mazlami.crawler as crawler, mazlami.preprocessing as preprocessing
import sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mazlami.kruskal as kruskal


class Decomposer:

    def DFS(self, nd, new_nodes, component, visited):
        for e in new_nodes[nd]:
            if e not in visited:
                visited.append(e)
                component.append(e)
                self.DFS(e, new_nodes, component, visited)

    def computeComponents(self,resultMST):
        new_nodes = {}
        visited = []
        components = []
        for i in resultMST:
            node1 = i[0]
            node2 = i[1]
            if node1 not in new_nodes:
                new_nodes[node1] = []
            if node2 not in new_nodes:
                new_nodes[node2] = []
            if i[2] != "dihapus":
                new_nodes[node1].append(node2)
                new_nodes[node2].append(node1)
        
        for nd in new_nodes:
            if nd not in visited:
                component = []
                visited.append(nd)
                component.append(nd)
                self.DFS(nd, new_nodes, component, visited)
                components.append(component)

        return components

    def decompose(self, filepath, threshold):
        filepath_list = crawler.dfsfilepath(filepath)
        php_class_list = {}
        for fp in filepath_list:
            raw = preprocessing.extract(fp)
            php_class_list[raw[0]] = raw[1]
            if len(raw[0]) < 2:
                print(fp, raw[0])

        vectorizer = TfidfVectorizer()
        src_bucket = []
        for i in php_class_list:
            src_bucket.append(php_class_list[i])
        vectors = vectorizer.fit_transform(src_bucket)
        cosine_sim = cosine_similarity(vectors, vectors)

        headers = []
        for i in php_class_list:
            headers.append(i)

        nodes = {}
        idx = -1
        for node in php_class_list:
            idx += 1
            nodes[node] = {}
            el = cosine_sim[idx]
            sec_idx = 0
            for i in php_class_list:
                dividen = round(el[sec_idx],14)
                if dividen == 0:
                    dividen = 0.0000000000001
                nodes[node][i] = 1 / dividen
                sec_idx += 1
        
        mapper = {}
        counter = 0
        for header in headers:
            mapper[header] = counter
            counter += 1

        g = kruskal.Graph(len(mapper))

        done_imported = []
        for node in nodes:
            for ng in nodes[node]:
                if node == ng:
                    continue
                if ng not in done_imported:
                    g.addEdge(mapper[node], mapper[ng], nodes[node][ng])
            done_imported.append(node)

        resultMST = g.KruskalMST()

        reversed_result = []
        result2MST = resultMST.copy()
        while(len(result2MST) > 0):
            reversed_result.append(result2MST.pop())

        new_nodes = {}

        for i in resultMST:
            node1 = i[0]
            node2 = i[1]
            if node1 not in new_nodes:
                new_nodes[node1] = []
            if node2 not in new_nodes:
                new_nodes[node2] = []
            if i[2] != "dihapus":
                if node2 not in new_nodes[node1]:
                    new_nodes[node1].append(node2)
                if node1 not in new_nodes[node2]:
                    new_nodes[node2].append(node1)


        n_max = threshold
        n_number = 1
        components = []

        reversed_result2 = reversed_result.copy()
        components_final = self.computeComponents(reversed_result2)
        while n_number < n_max:
            el  = reversed_result2.pop(0)
            if el[2] == "dihapus":
                break
            el[2] = "dihapus"
            reversed_result2.append(el)
            components_final = self.computeComponents(reversed_result2)
            n_number = len(components_final)

        formatted_com_fin = []
        for c in components_final:
            new_c = []
            for e in c:
                for el in mapper:
                    if mapper[el] == e:
                        new_c.append(el)
            formatted_com_fin.append(new_c)

        final_dict = {}
        coutn = 0
        for el in formatted_com_fin:
            for ele in el:
                final_dict[ele] = [str(coutn)]
            coutn +=1

        return final_dict    