//all degree avg
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
RETURN avg(degree) AS mean

// in degree avg
MATCH (n)
WITH n, size([(n)-->() | 1]) AS degree
RETURN avg(degree) AS mean

//median all degrees
MATCH (n)
WITH n, size ([(n)--() | 1]) AS degree
ORDER BY degree
WITH collect(degree) AS values
RETURN values[toInteger(size(values)/2)] AS median


//median in degree
MATCH (n)
WITH n, size ([(n) -->() | 1]) AS degree
ORDER BY degree
WITH collect(degree) AS values
RETURN values[toInteger(size(values)/2)] AS median


//median out degree
MATCH (n)
WITH n, size ([(n)<--() | 1]) AS degree
ORDER BY degree
WITH collect(degree) AS values
RETURN values[toInteger(size(values)/2)] AS median


//mode all degrees
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
RETURN degree AS mode, count(*) AS frequency
ORDER BY frequency DESC
LIMIT 1


//mode in degree
MATCH (n)
WITH n, size([(n)-->() | 1]) AS degree
RETURN degree AS mode, count(*) AS frequency
ORDER BY frequency DESC
LIMIT 1


//mode out degree
MATCH (n)
WITH n, size([(n)<--() | 1]) AS degree
RETURN degree AS mode, count(*) AS frequency
ORDER BY frequency DESC
LIMIT 1


//out degree avg
MATCH (n)
WITH n, size([(n)<--() | 1]) AS degree
RETURN avg(degree) AS mean

// st dev all degrees
MATCH (n)
WITH avg(size([(n)--() | 1])) AS mean

MATCH (n)
WITH mean, (size([(n)--() | 1]) - mean) * (size([(n)--() | 1]) - mean) AS sqDiff

RETURN sqrt(avg(sqDiff)) AS stDev


// st dev in degree
MATCH (n)
WITH avg(size([(n)-->() | 1])) AS mean

MATCH (n)
WITH mean, (size([(n)-->() | 1]) - mean) * (size([(n)-->() | 1]) - mean) AS sqDiff

RETURN sqrt(avg(sqDiff)) AS stDev


// st dev out degree
MATCH (n)
WITH avg(size([(n)<--() | 1])) AS mean

MATCH (n)
WITH mean, (size([(n)<--() | 1]) - mean) * (size([(n)<--() | 1]) - mean) AS sqDiff

RETURN sqrt(avg(sqDiff)) AS stDev