## nearest_similar_point

#####  Works similarly like gpd.sjoin_nearest() but it calculates distance to nearest point with same category in source and target data

The simple spatial join nearest function only calculate the nearest feature without considering if they have any common type or category this function calculates the nearest similar object.

See the explained.png to understand better for example: target feature with id:1 and type: sign_pole is spatially closest to base feature of type: traffic light but its ignored because the type/category doesnt match and hence it gives distance of nearest point where type matches (connected with line for illustration)


##### work in progress, right now only considered for point data frames, no error handling, slow coz of geoseries distance calculation method
