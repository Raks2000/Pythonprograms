with open("stocks_sample.csv", "r") as file:
    dictionary = {}
    for line in file:
        data = line.strip().split(",")
        key = data[0]
        values = data[1:]
        dictionary[key] = values
    print(dictionary)
