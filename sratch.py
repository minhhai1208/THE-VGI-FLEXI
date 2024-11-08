import numpy as np

arr_2d = np.array([ [[10, 3, 5], 
                    [7, 6, 1]] ,
                    [[1,2,3],
                     [4,5,6]]
                    ])
print(arr_2d.shape)
index_of_min_along_axis_0 = np.argmin(arr_2d, axis=1) 

print(index_of_min_along_axis_0)