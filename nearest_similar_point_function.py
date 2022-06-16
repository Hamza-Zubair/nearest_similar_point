# mandatory import of libraries
import geopandas as gpd
import pandas as pd

# function similar to existing gpd.sjoin_nearest() but checks for the nearest similar function
def nearest_similar_point(target, base, unique_target_id, similar_field):
    """
    Calculates distance of nearest point with similar catgeory from target to base and returns a GeoDataFrame.
    
    Parameters:
    -----
    target: GeoDataFrame(point) with Projected-CRS for which the nearest neighbour's distance will be calculated
    base: GeoDataFrame(point) with Projected-CRS which is kept as source to calculate distance
    unique_target_id: a unique id field in str i.e.('unique_id') from target dataframe 
    similar_field: an identically common field in both dataframes in str i.e.('similar_field')
    
    Returns:
    -----
    df: GeoDataFrame(point) with distance field.
    
    Dependencies:
    -----
    geopandas and pandas libaries should be imported
    
    Notes
    -----
    Results will be innaccurate if geometries are in a geographic-CRS.
    Data loss in case of unique_target_id contain duplicate values.
    Inaccurate results if there is no common field in both GeoDataFrames
    Suitable only for small datasets & no error handling/exceptions taken into account
    """
    df = pd.merge(target, base, how = 'cross', suffixes = ['','_base'])  # m*n of datasets, 
    df['distance'] = df.geometry.distance(df.geometry_base)  # not memory efficient, only suitable with small datasets
    df = df[df[similar_field] == df[similar_field+'_base']]  # filter, keeping points with similar target and base category
    df.sort_values(by=[similar_field,similar_field+'_base','distance'], inplace = True) 
    df.drop_duplicates(subset=[unique_target_id, similar_field, similar_field+'_base'], keep='first', inplace=True) # keep shortest distance record
    df = df[df.columns.drop(list(df.filter(regex='_base')))]  # removing extra fields
    return df


# tested with 2 hunderd million records (m*n), with time of ~5.5 mins. so its not efficient with big datasets
# most time taking part of function is distance calculation, maybe it can be improved in future

# bench mark the time for running the whole program
import timeit
start = timeit.default_timer()

target = gpd.read_file(r'path\file.shp')
base = gpd.read_file(r'path\file.shp')
result = nearest_similar_point(target, base,'id', 'info')

end = timeit.default_timer()
total = end - start
print('Whole program takes', total, "seconds") 