#!/usr/bin/env python
# -*- coding: utf-8 -*-


def isPalindrome(s: str) -> bool:
        if not s: return True
        s_low=s.lower()
        numbers = '1234567890'
        letters ='qwertyuiopasdfghjklzxcvbnm'
        L=len(s_low)
        point1,point2=0,L-1
        flag = False
        while point1<point2:
            if s_low[point1] not in numbers and s_low[point1] not in letters:
                point1+=1
                if point1 >= point2:
                    flag = True
                    break
            while s_low[point2] not in numbers and s_low[point2] not in letters:
                point2-=1
                if point1>=point2:
                    flag = True
                    break
            if flag == True: break
            if s_low[point1]!=s_low[point2]:
                return False
        return True

isPalindrome("A man, a plan, a canal: Panama")