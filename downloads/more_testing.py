import numpy as np
import pandas as pd

yo = pd.DataFrame([[1,1],[2,2]])
yo = 'gi'


if type(yo) == str:
    print('str')
elif type(yo) == pd.core.frame.DataFrame:
    print('df')
isinstance(yo, str)
