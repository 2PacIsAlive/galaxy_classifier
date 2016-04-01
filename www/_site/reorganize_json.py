import json
with open("runtime_analysis.json", "r") as file_:
    old = json.load(file_)

insertion_sort = []
quicksort      = []
mergesort      = []

for key in old.keys():
    insertion_sort.append( {"n": int(key), "avg": old[key]["Insertion Sort"]["avg"], "max": old[key]["Insertion Sort"]["max"]} )
    mergesort.append(      {"n": int(key), "avg": old[key]["Mergesort"]["avg"],      "max": old[key]["Mergesort"]["max"]} )
    quicksort.append(      {"n": int(key), "avg": old[key]["Quicksort"]["avg"],      "max": old[key]["Quicksort"]["max"]} )

json_entry = {"Insertion Sort": insertion_sort,
              "Mergesort":      mergesort,
              "Quicksort":      quicksort}

with open("runtime_analysis_v5.json", "w") as out:
    json.dump(json_entry, out)
