# -*- coding: iso-8859-1 -*-

###############################################################
# Name:			 EditDistance.py
# Purpose:	 Minimum Edit Distance algorithm
# Code from: http://www.cs.colorado.edu/~martin/csci5832/edit-dist-blurb.html
# Created:	 2013-08-14
##############################################################


def substCost(x,y):
	if x == y: return 0
	else: return 1
	
def insertCost(x):
	return 1

def deleteCost(x):
	return 1

def  minEditDist(target, source):
	n = len(target)
	m = len(source)

	distance = [[0 for i in range(m+1)] for j in range(n+1)]

	for i in range(1,n+1):
		distance[i][0] = distance[i-1][0] + insertCost(target[i-1])

	for j in range(1,m+1):
		distance[0][j] = distance[0][j-1] + deleteCost(source[j-1])

	for i in range(1,n+1):
		for j in range(1,m+1):
		   distance[i][j] = min(
					distance[i-1][j]+1,
					distance[i][j-1]+1,
					distance[i-1][j-1]+substCost(source[j-1],target[i-1])
				)
	return distance[n][m]
