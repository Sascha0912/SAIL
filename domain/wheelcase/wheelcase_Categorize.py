import pandas as pd

def wheelcase_Categorize(samples, d):
    # to which bin does a cube belong? depends on the selected features
    # print("samples")
    # print(samples)
    index = [i for i in range(0,len(samples))]
    categories = pd.DataFrame(columns=[0,1],index=index)
    for i in range(len(samples)):
        second = samples.iloc[i,2]
        third = samples.iloc[i,3]
        fourth = samples.iloc[i,4]
        fifth = samples.iloc[i,5]

        if (second>0 and third>0): # deformation to inside
            completeWidth = 0
        elif (second>0 and third<0):
            width1 = abs(third)
            # width2 = abs(third)
            completeWidth = width1*2
        elif (second<0 and third>0):
            width1 = abs(second)
            completeWidth = width1*2
        else:
            width1 = abs(second)
            width2 = abs(third)
            completeWidth = max(width1,width2)*2

        if (fifth<0):
            maxHeight = 0
        else:
            maxHeight = fifth
        # height1 = abs(samples.iloc[i,4])
        # height2 = abs(samples.iloc[i,5])
        # maxHeight = max(height1,height2)

        categories.loc[i] = [completeWidth, maxHeight]

    categories.reset_index(drop=True,inplace=True)
    # print("categories")
    # print(categories)
    return categories
