
from ast import Or
import mdp.crawler as crawler, mdp.analyzer as analyzer

class Decomposer:

    def __init__(self) -> None:
        pass

    def info(self) -> None:
        print("This is Bintang Decomposer class")

    def canMerge(self, root1, root2, threshold):
        can_merge = 0
        same_elements = list(set(root1).intersection(root2))
        if set(same_elements) == set(root1) or set(same_elements) == set(root2):
            can_merge = 1
        if len(set(same_elements)) >= threshold:
            can_merge = 1
        return can_merge

    def decompose(self, filepath, threshold):
        filepath_list = crawler.dfsfilepath(filepath)

        try:
            # create php class list
            php_class_list = {}
            for fp in filepath_list:
                php_class = analyzer.extractClassFromFile(fp)
                if len(php_class.fullname) < 0:
                    raise Exception("PHP class name not valid.", fp, php_class.fullname)
                php_class_list[php_class.fullname] = php_class
        except Exception as e:
            raise Exception(e, fp, php_class.fullname)

            
        # remove framework or utility class reference
        new_class_list = {}
        for cname in php_class_list:
            cl = php_class_list[cname]
            refined_cl = {}
            for r in cl.reference_occurrences:
                if r in php_class_list:
                    refined_cl[r] = cl.reference_occurrences[r]
            new_class_list[cname] = refined_cl
        
        # remove cyclic dependency
        for cname in new_class_list:
            for refname in new_class_list[cname]:
                if refname in new_class_list:
                    if cname in new_class_list[refname]:
                        new_class_list[refname].pop(cname)

        # revert class list from
        # a = {b,c,d} where a uses b, c, and d to
        # a = {b,c,d} where a is used by b, c, and d
        reverted_class_list = {}
        for cname in new_class_list:
            if cname not in reverted_class_list:
                reverted_class_list[cname] = {}
            for rname in new_class_list[cname]:
                if rname not in reverted_class_list:
                    reverted_class_list[rname] = {}
                reverted_class_list[rname][cname] = new_class_list[cname][rname]

        # find root / kelas yang tidak direferensikan kelas lain
        root = {}
        for cname in reverted_class_list:
            if len(reverted_class_list[cname]) < 1:
                root[cname] = []
        
        # traversed root (mentraverse elemen-elemen yang digunakan oleh root)
        for ro in root:
            to_be_traversed = [ro]
            has_been_traversed = []
            while(len(to_be_traversed) > 0):
                processed = to_be_traversed.pop(0)
                for re in new_class_list[processed]:
                    root[ro].append(re)
                    if re not in has_been_traversed:
                        to_be_traversed.append(re)
                has_been_traversed.append(processed)
        
        # menghapus root yang tidak menggunakan elemen apapun
        to_be_deleted = []
        for ro in root:
            if len(root[ro]) < 1:
                to_be_deleted.append(ro)
        for e in to_be_deleted:
            del root[e]
        
        # mencopy root            
        new_root = root.copy()

        # menmerge root-root yang ada sampai tidak ada yang bisa dimerge
        mapper = {}
        for root in new_root:
            mapper[root] = str(len(mapper))
        modified_root = {}
        for root in new_root:
            modified_root[mapper[root]] = new_root[root]
        backup_root = new_root.copy()
        new_root = modified_root.copy()

        while(True):
            to_be_removed = []
            merged_root = None
            root_name = None
            merging = 0
            for el in new_root:
                if(len(new_root[el]) < 1):
                    continue
                for eli in new_root:
                    if el == eli:
                        continue
                    if(len(new_root[eli]) < 1):
                        continue
                    if(self.canMerge(new_root[el], new_root[eli], threshold)):
                        to_be_removed.append(el)
                        to_be_removed.append(eli)
                        root1 = new_root[el].copy()
                        root2 = new_root[eli].copy()
                        root1.extend(root2)
                        merged_root = list(set(root1))
                        root_name = el
                        for i in mapper:
                            if mapper[i] == eli:
                                mapper[i] = el
                        merging = 1
                        break
                if merging == 1:
                    break
            if (merging == 1):
                for e in to_be_removed:
                    new_root.pop(e)
                new_root = new_root.copy()
                new_root[root_name] = merged_root
            else:
                break

        # hasil akhir clustering (mengelompokkan berdasarkan root)
        final_dict = {}
        for root in new_root:
            for el in new_root[root]:
                if el not in final_dict:
                    final_dict[el] = []
                final_dict[el].append(root)

        for root in backup_root:
            if root not in final_dict:
                final_dict[root] = []
            final_dict[root] = [mapper[root]]


        gol_terbuang = {}
        for root in to_be_deleted:
            if root not in final_dict:
                final_dict[root] = ["-1"]

        # Biar rapi
        final_dict = self.arrangeClusterIndex(final_dict)

        # for e in final_dict:
        #     if "0" in final_dict[e] or "1" in final_dict[e]:
        #         print(e, final_dict[e])

        return final_dict


    def findNameSpace(self, class_full_name:str):
        sep_val = class_full_name.count('#')
        if sep_val == 0:
            return None
        else:
            words = class_full_name.split("#")
            words = words[:-1]
            namespace = "#".join(words)
            return namespace
            
    def arrangeClusterIndex(self, final_dict:dict)->dict:
        new_index = {"-1":"-1"}
        new_dict = {}
        for el in final_dict:
            clusters = final_dict[el]
            new_clusters = []
            for cluster in clusters:
                if str(cluster) not in new_index:
                    new_index[str(cluster)] = str(len(new_index) - 1)
                new_clusters.append(new_index[str(cluster)])
            new_dict[el] = new_clusters
        return new_dict


