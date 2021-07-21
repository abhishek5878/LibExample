def reject_outliers(data, m = 2.):
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d/mdev if mdev else 0.
        return (s < m)

def mean_dup(x_):
        global reject_outliers
        if 1==len(np.unique(x_.values)):
            return x_.values[0]
        else:
            x = x_.values[reject_outliers(x_.values.copy())]
            x_mean = x.mean()
            mask = (x_mean*0.975 <= x) & (x <= x_mean*1.025)
            return x[mask].mean()

def remove_duplicate(df):
    '''
        Removes duplicates in dataframe and element samples whose composition is not 100%

        input format  ->  df  = dataframe
    '''
    features = df.columns.values.tolist()
    features.remove(df.columns[-1])
    property_name = df.columns[-1]

    df = df[df[features].sum(axis=1).between(99,101)]
    df = df.groupby(features,as_index=False).agg(mean_dup)
    df = df.dropna()
    df = df.loc[(df[property_name])> 0]
    return df
