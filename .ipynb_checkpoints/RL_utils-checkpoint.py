import numpy as np

def rldecode(data):
    datalen = len(data)
    bytes_buffer = []
    
    cursor = 0;
    zero_ba = [False]
    one_ba = [True]
    for i, (loc, run) in enumerate(data):
        bytes_buffer += zero_ba * (loc - cursor) + one_ba * run
        cursor = loc + run
        
        if i%100 == 0:
            print(f"{i}/{datalen}")
    print("Constructing Array")
    array = np.asarray(bytes_buffer, dtype=np.bool)
    print("Array Finished")
    
    return array




if __name__ == "__main__":
    import random
    zero_sizes = [random.randint(0, 100) for x in range(50)]
    one_sizes = [random.randint(0, 100) for x in range(50)]
    
    cursor = 0
    test_rle = []
    for z, o in zip(zero_sizes, one_sizes):
        cursor = cursor + z
        test_rle += [(cursor, o)]
        cursor += o
    # print(test_rle)
    
    npa = rldecode(test_rle)
    
    
    print(npa)
        
    
    