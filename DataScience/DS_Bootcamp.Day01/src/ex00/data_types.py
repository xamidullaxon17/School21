def data_types():
    number = 23
    name = "Xamidullaxon"
    floats = 12.3
    boolean = True
    lists = ["python", "java","htlm","css","c++"]
    dictionary = {"Apple":"olma","tree":"daraxt"}
    tuples = ("rabbit", "cat", "dog", "mouse")
    sets = {1,2,3,4,5}
    print([type(number).__name__,type(name).__name__,
           type(floats).__name__,type(boolean).__name__,type(lists).__name__,
           type(dictionary).__name__,type(tuples).__name__,type(sets).__name__,])
    
if __name__ == "__main__":
    data_types()
