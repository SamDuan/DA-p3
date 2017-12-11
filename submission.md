# OpenStreetMap Data Case Study

### Map Area
Raleigh, NC, United States

- [https://mapzen.com/data/metro-extracts/metro/raleigh_north-carolina/](https://mapzen.com/data/metro-extracts/metro/raleigh_north-carolina/)
- [https://www.openstreetmap.org/relation/179052](https://www.openstreetmap.org/relation/179052)

This map is of the city I used to live, so I’m quite interested to see what database querying reveals.

## Problems Encountered in the Map
The full size map was run against audit.py, data.py and db.py sequentially, and few problems with the data are found as shown below:

- Missing spaces upon entering *("LaurelcherryStreet")* 
- Extra information included the street names *("Westgate Park Dr #100", "Barrett Dr Suite 206", "Fayetteville St #1100")*
- Inconsistent postal codes *("277030", "27713-2229", "28616")*
- Typos in the city names *(Morrisville is mis-spelled as Morisville)*

# Sort cities by count, descending

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
2374920

### Number of ways
```sql
sqlite> SELECT COUNT(*) FROM ways;
```
243842

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
199

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

# Additional Ideas (to-do)

## Contributor statistics and gamification suggestion (to-do)
The contributions of users seems incredibly skewed, possibly due to automated versus manual map editing (the word “bot” appears in some usernames). Here are some user percentage statistics:

- Top user contribution percentage (“jumbanho”) 52.92%
- Combined top 2 users' contribution (“jumbanho” and “woodpeck_fixbot”) 83.87%
- Combined Top 10 users contribution
94.3%
- Combined number of users making up only 1% of posts 287 (about 85% of all users)

Thinking about these user percentages, I’m reminded of “gamification” as a motivating force for contribution. In the context of the OpenStreetMap, if user data were more prominently displayed, perhaps others would take an initiative in submitting more edits to the map. And, if everyone sees that only a handful of power users are creating more than 90% a of given map, that might spur the creation of more efficient bots, especially if certain gamification elements were present, such as rewards, badges, or a leaderboard.

# Conclusion (to-do)
 After this review of the data it’s obvious that the Charlotte area is incomplete, though I believe it has been well cleaned for the purposes of this exercise. It interests me to notice a fair amount of GPS data makes it into OpenStreetMap.org on account of users’ efforts, whether by scripting a map editing bot or otherwise. With a rough GPS data processor in place and working together with a more robust data processor similar to data.pyI think it would be possible to input a great amount of cleaned data to OpenStreetMap.org.
