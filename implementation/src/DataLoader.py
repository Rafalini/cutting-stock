import json

def loadData(inputFile: str):
    jsonData = json.load(open(inputFile))
    assert jsonData["factory_rod_size"] > 0, "Rod size cannot be smaller than 1"

    for i in jsonData["order"]:
        assert i["rod_size"] <= jsonData["factory_rod_size"], "Required rod size cannot exceed lenght of rod produced by factory"
        assert i["rods_number"] > 0, "Number of rods cannot be smaller than 1"
        assert i["relaxation_number"] >= 0, "Number of rods cannot be smaller than 0"
        assert i["relaxation_length"] >= 0, "Relaxation amount cannot be smaller than 0"
        assert i["relaxation_length"] < i["rod_size"], "Length to relax cannot exceed rod length"
        assert i["relaxation_number"] <= i["rods_number"], "Number of rods cannot be smaller than number of rods that can be relaxed!"
    return jsonData