import csv
from tabulate import tabulate
import networkx as nx
import math
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score, average_precision_score, recall_score, accuracy_score
from sklearn.metrics import classification_report

class Evaluator:

    def __init__(self) -> None:
        self.gt = None
        self.statistic_result = None
        self.final_table = None
        self.statistic_table = None
        self.cluster_indexes = None
        self.possible_domains = None
        self.purity_table_by_number = None
        self.purity_table_by_percentage = None
        self.purity_mean_by_number = None
        
        self.stats = {
            "Excellent Cluster":0, "Bad Cluster":0, "Semi-good Cluster":0, "Total Cluster":0
        }

    def getNumberofCluster(self):
        counter = 0
        for cl in self.cluster_indexes:
            if str(cl) != "-1":
                counter +=1

        return counter

    def readGroundTruth(self, filename) -> bool : 
        gt = {}
        with open(filename, "r") as f:
            csvReader = csv.reader(f, delimiter=";")
            for row in csvReader:
                gt[row[0]] = row[1]
        self.gt = gt
        return True
    
    def getNumberOfDomains(self):
        domains = []
        gt = self.gt
        for g in gt:
            if gt[g] not in domains:
                domains.append(gt[g])
        return len(domains)

    def assertResult(self,result:dict) -> bool:
        gt = self.gt    
        possible_domains = {}
        for el in gt:
            domain = gt[el]
            if domain not in possible_domains:
                possible_domains[domain] = 1
            else:
                possible_domains[domain] += 1
    
        
        cluster_indexes = []
        for el in result:
            if el not in gt:
                raise Exception(el, " is not in ground truth")
                continue
            if len(result[el]) > 0:
                for i in result[el]:
                    if len(i) < 1:
                        raise Exception("Sorry, cluster named with zero length is not prohibited!")
                    if i not in cluster_indexes:
                        cluster_indexes.append(i)
            else:
                raise Exception("Sorry, class with no cluster detected! -> " + el )

        final_table = {}
        for ci in cluster_indexes:
            final_table[ci] = {}
            for domain in possible_domains:
                final_table[ci][domain] = 0
        
        for cname in result:
            clusters = result[cname]
            for cluster in clusters:
                if cname in gt:
                    domain = gt[cname]
                    final_table[cluster][domain] += 1

        statistic_result = {}
        for cluster in final_table:
            if cluster not in statistic_result:
                statistic_result[cluster] = {}
            for domain in final_table[cluster]:
                if domain not in statistic_result[cluster]:
                    statistic_result[cluster][domain] = 0.0
                if possible_domains[domain] == 0:
                    statistic_result[cluster][domain] = 0.0
                else:
                    statistic_result[cluster][domain] = float(final_table[cluster][domain]) / float(possible_domains[domain]) * 100.0

            
        # return final_table
        headers = ["cluster"]
        headers.extend(possible_domains)

        statistic_table = [headers]
        for cluster in statistic_result:
            row = [cluster]
            for domain in statistic_result[cluster]:
                row.append(str(round(statistic_result[cluster][domain], 3)) + "%")
            statistic_table.append(row)
        
        self.final_table = final_table
        self.statistic_result = statistic_result    
        self.statistic_table = statistic_table
        self.possible_domains = possible_domains
        self.cluster_indexes = cluster_indexes

        self.getPurityByNumber()

        headers = ["cluster"]
        headers.extend(self.possible_domains)
        self.printable_final_table = [headers]
        for cluster in final_table:
            row = [cluster]
            for domain in final_table[cluster]:
                row.append(str(final_table[cluster][domain]))
            self.printable_final_table.append(row)
        
        return True

    def assignClusterToDomain(self):
        self.cltodomain = {}
        for cl in self.final_table:
            max = 0
            major_domain = "None"
            for domain in self.final_table[cl]:
                if self.final_table[cl][domain] > max:
                    max = self.final_table[cl][domain]
                    major_domain = domain
            self.cltodomain[cl] = major_domain


    def printGtDict(self, filename):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            for el in self.gt_dict:
                elnew = el
                if "#" in el:
                    elnew = el.split("#")[-1]
                writer.writerow([elnew, self.gt_dict[el]["actual"], self.gt_dict[el]["predicted"]])

    def evaluateResult(self, result):
        predicted = []
        groundt = []
        gt_dict = {}
        for r in result:
            if type(result[r]) == list:
                cl = result[r][0]
            else:
                cl = result[r]
            domain = self.cltodomain[cl]
            domain_in_gt = self.gt[r]
            predicted.append(domain)
            groundt.append(domain_in_gt)
            gt_dict[r] = {"actual":domain_in_gt, "predicted":domain}

        self.gt_dict = gt_dict
        report = classification_report(groundt, predicted)
        print(report)
        return accuracy_score(groundt, predicted)
        

        



    def printStatisticTable(self)->None:
        print(tabulate(self.statistic_table, headers="firstrow"))

    def getPurityByNumber(self):
        purity_mean = 0
        cluster_number = 0
        purity_max = -9999999
        purity_min = 9999999

        purity_table_by_number = {}
        for cl in self.cluster_indexes:
            if cl == -1 or cl == "-1" :
                continue
            elif cl not in purity_table_by_number:
                purity_table_by_number[cl] = None


        for cl in self.final_table:
            max = -9999999
            dominant_domain = None
            dividen = 0
            if cl == "-1" or cl == -1:
                continue
            cluster_data = self.final_table[cl]
            for domain in cluster_data:
                if domain == "not_in_ground_truth":
                    continue
                if cluster_data[domain] > max:
                    max = cluster_data[domain]
                    dominant_domain = domain
                if domain != "not_in_ground_truth":
                    dividen += cluster_data[domain]
            for domain in cluster_data:
                if domain == dominant_domain:
                    continue
                elif domain == "not_in_ground_truth":
                    continue
                else:
                    max -= cluster_data[domain]
            if dividen == 0:
                purity = 0
            else:
                purity = max/dividen
                if(purity > 1):
                    print(max, cl)
                    raise Exception("Sorry, purity over 1")
            purity_table_by_number[cl] = purity

            purity_mean += purity
            cluster_number +=1
            if(purity > purity_max):
                purity_max = purity
            if(purity_min > purity):
                purity_min = purity
        
        self.purity_table_by_number = purity_table_by_number

        purity_mean = purity_mean/cluster_number
        self.purity_mean_by_number = purity_mean
        self.purity_min_by_number = purity_min
        self.purity_max_by_number = purity_max

    def calcDomainSpread(self):
        self.domain_spread_table = None

        domain_spread = {}
        for cl in self.statistic_result:
            for domain in self.statistic_result[cl]:
                if domain == "not_in_ground_truth":
                    continue
                if domain not in domain_spread:
                    domain_spread[domain] = []
                if self.statistic_result[cl][domain] > 0:
                    domain_spread[domain].append(self.statistic_result[cl][domain])
        
        mean = 0
        min = 999999999
        max = -999999999
        domain_spread_table = {}
        for domain in domain_spread:
            row = domain_spread[domain]
            val = 0
            for e in row:
                val += e
            val = val / len(row)
            domain_spread_table[domain] = val
            mean += val
            if val > max:
                max = val
            if val < min:
                min = val

        mean = mean / len(domain_spread)
        self.domain_spread_table = domain_spread_table
        self.domain_spread_mean = mean
        self.domain_spread_min = min
        self.domain_spread_max = max

    
    def printDomainSpread(self):
        print("Table of Domain Spread")
        headers = ["domain", "mean of spread"]
        otw_print = [headers]
        for domain in self.domain_spread_table:
            row = [domain]
            row.append(str(round(self.domain_spread_table[domain], 4)) + "%")
            otw_print.append(row)

        otw_print.append(["MEAN", str(round(self.domain_spread_mean,4))])
        otw_print.append(["MIN", str(round(self.domain_spread_min,4))])
        otw_print.append(["MAX", str(round(self.domain_spread_max,4))])
        print(tabulate(otw_print, headers="firstrow"))

    def debug(self):
        for x in self.final_table:
            print(x,self.final_table[x])

        for x in self.possible_domains:
            print(x, self.possible_domains[x])

    def printAll(self):
        self.printPurityTableByNumber()
        self.printStatisticTable()
        print(tabulate(self.printable_final_table, headers="firstrow"))


    def printPurityTableByNumber(self):
        print("Table of Cluster Quality")
        headers = ["cluster", "Q(c)"]
        otw_print = [headers]
        for cluster in self.purity_table_by_number:
            row = [cluster]
            row.append(str(round(self.purity_table_by_number[cluster], 4)))
            otw_print.append(row)

        otw_print.append(["MEAN", str(round(self.purity_mean_by_number,4))])
        otw_print.append(["MIN", str(round(self.purity_min_by_number,4))])
        otw_print.append(["MAX", str(round(self.purity_max_by_number,4))])

        print(tabulate(otw_print, headers="firstrow"))

    def drawGraph(self, result, threshold):
        gt = self.gt
        possible_domains = {}
        for el in gt:
            domain = gt[el]
            if domain not in possible_domains:
                possible_domains[domain] = 1
            else:
                possible_domains[domain] += 1

        
        nodes = []
        centroids = []
        for el in result:
            if el in gt:
                domain = gt[el]
            else:
                continue
            clusters = result[el]
            node_counter = 0
            for cl in clusters:
                if cl not in centroids:
                    centroids.append(cl)
                nodes.append([el+str(node_counter), cl, domain])
                node_counter+= 1

        G = nx.Graph()

        max_pos =  math.ceil(math.sqrt(len(centroids)))

        x_cor = 0
        X_counter = 0
        y_cor = 0
        distance_per_centroid = 15
        fixed_positions = {}
        node_sizes = []
        node_colors = []
        centroid_labels = {}


        color_list = [
            "#F5DF4D", "#939597", "#0F4C81", "#FF6F61", "#5F4B8B", "#88B04B", "#F7CACA", "#93A9D1", 
            "#964F4C", "#AD5E99", "#009473","#DD4124", "#D94F70", "#45B5AA", "#F0C05A", "#5A5B9F", "#9B1B30"
        ]  

        color_mapper = {}
        counter_color = 0
        for domain in possible_domains:
            color_mapper[domain] = color_list[counter_color]
            counter_color +=1

        for c in centroids:
            G.add_node(c)
            centroid_labels[c] = c
            fixed_positions[c] = (x_cor,y_cor)
            X_counter +=1
            if(X_counter%max_pos == 0):
                y_cor += distance_per_centroid
                x_cor = 0
            else:
                x_cor = x_cor + distance_per_centroid
            node_sizes.append(70)
            node_colors.append("blue")
            
        for node in nodes:
            if node[0] not in list(G.nodes):
                G.add_node(node[0])
                node_colors.append(color_mapper[node[2]])
            G.add_edge(node[1], node[0])

        number_of_nodes = G.number_of_nodes() - len(centroids)

        for i in range(number_of_nodes):
            node_sizes.append(10)

        plt.figure()
        plt.title(threshold)
        pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_positions.keys())
        nx.draw(G, pos, node_size=node_sizes, width=0.09, node_color=node_colors)
        nx.draw_networkx_labels(G, pos, centroid_labels)        




