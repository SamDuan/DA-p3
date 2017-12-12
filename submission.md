# OpenStreetMap Data Case Study

### Map Area
Raleigh, NC, United States

- [https://mapzen.com/data/metro-extracts/metro/raleigh_north-carolina/](https://mapzen.com/data/metro-extracts/metro/raleigh_north-carolina/)
- [https://www.openstreetmap.org/relation/179052](https://www.openstreetmap.org/relation/179052)

This map is of a city that I used to live, so I’m quite interested to see what database querying reveals.

## Problems Encountered in the Map
The full size map was run against audit.py, data.py and db.py sequentially, and few problems with the data are found as shown below:

- Missing spaces upon entering *("LaurelcherryStreet")* 
- Extra information included the street names *("Westgate Park Dr #100", "Barrett Dr Suite 206", "Fayetteville St #1100")*
- Inconsistent postal codes *("277030", "27713-2229", "28616")*
- Typos in the city names *(Morrisville is mis-spelled as Morisville)*

# Data Overview and Additional Ideas
This section contains basic statistics about the dataset, and sql queries used to gather them are listed as well.

### File sizes
```
raleigh_north-carolina.osm .... 482 MB
mydb.db ....................... 266 MB
nodes.csv ..................... 190 MB
nodes_tags.csv ................ 2.1 MB
ways.csv ...................... 13 MB
ways_nodes.cv ................. 63 MB
ways_tags.csv ................. 30 MB
```  

### Number of nodes
```sql
sqlite> SELECT COUNT(*) FROM nodes;
```
```sql
2374920
```

### Number of ways
```sql
sqlite> SELECT COUNT(*) FROM ways;
```
```sql
243842
```

### Number of unique users
```sql
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
```sql
1019
```

### Top 10 contributing users
```sql
sqlite> SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
```
```sql
jumbanho        1552751
JMDeMai         219489
bdiscoe         129500
woodpeck_fixbot 112193
bigal945        103601
yotann          66555
runbananas      41249
BjornRasmussen  37676
sandhill        33495
MikeInRaleigh   30578
```

### Number of users appearing only once (having 1 post)
```sql
sqlite> SELECT COUNT(*)
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1)  u;
```

```sql
199
```

### Sort cities by count, descending
```sql
sqlite> SELECT tags.value, COUNT(*) as count
FROM (SELECT * FROM nodes_tags UNION ALL
      SELECT * FROM ways_tags) tags
WHERE tags.key == 'city'
GROUP BY tags.value
ORDER BY count DESC;
```
And the results are shown below:

```sql
Raleigh      6830
Cary         3119
Morrisville  1732
Durham       1674
Chapel Hill  625
Carrboro     503
Research Triangle Park 6
Hillsborough 5
RTP          4
raleigh      4
chapel Hill  3
Chapel Hill, NC 2
Wake Forest  2
cary         2
durham       2
 Raleigh     1
Apex         1
Morisville   1
Ralegh       1
Ralegih      1
chapel hill  1
```

Firstly, the major cities in the triangle are (Raleigh-Durham-Chapel Hills) are included in this data set. Thus, it contains not only the city of Raleigh but also the nearby cities. Secondly, it is visible that there are several variations of names of the same city (e.g. "Chapel Hill", "chapel Hill", Chapel Hill, NC", "chapel hill").

### Top 10 amenities

```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```

```sql
bicycle_parking  1146
restaurant       924
place_of_worship 742
fast_food        366
bench            264
waste_basket     250
cafe             194
atm              156
school           152
parking          144
```
It is surprising to find out that there are many bicycle parking lots in this area. It is possible these parkings are around the campuses for the students, who ride bikes in their campuses.

### Top 10 shops

```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='shop'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```

```sql
clothes|198
supermarket|186
hairdresser|118
vacant|88
beauty|74
car_repair|60
jewelry|58
department_store|54
gift|48
art|42
```

# Additional Ideas

## Contributor statistics
Based on the result from the top 10 contriting users, it is easy to note that the user "jumbanho" has a very high contribution, which is larger than 65%. In other words, the contribution from this user is more than the totality of all other users. It is possible the data entry could be skewed due to dominance of data source. How to reduce the risk of having biased data entry is a question that worth considering

# Conclusion
This review renders a general overlook of the geography information in Raleigh area, and certain entry errors have been be identified as well. In addition, the data in this map is largely supplied by a single user, which could possibly lead to bias information.
