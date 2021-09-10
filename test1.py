#!/usr/bin/env python
# -*- coding: utf-8 -*-

def setZeroes(matrix):
    x = []
    y = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                if i not in x:
                    x.append(i)
                if j not in y:
                    y.append(j)
    return 1
    for i in x:
        for j in y:
            matrix[i][j] = 0

setZeroes([[1,1,1],[1,0,1],[1,1,1]])