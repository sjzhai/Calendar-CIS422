import functions



def get_weekday_test():
    #basic functionality
    assert functions.get_weekday('2018','4','23') == ['2018-04-22', '2018-04-23', '2018-04-24', '2018-04-25', '2018-04-26', '2018-04-27', '2018-04-28']
    assert functions.get_weekday('3000','4','23') == ['3000-04-20', '3000-04-21', '3000-04-22', '3000-04-23', '3000-04-24', '3000-04-25', '3000-04-26']
    assert functions.get_weekday('1900','4','23') == ['1900-04-22', '1900-04-23', '1900-04-24', '1900-04-25', '1900-04-26', '1900-04-27', '1900-04-28']
    
    #assert functions.get_weekday('1','4','23') == ['1-04-17', '1-04-18', '1-04-19', '1-04-20', '1-04-21', '1-04-22', '1-04-23']
    #For some reason it doesn't get the right weekdays for early dates. 1900 works, 1500 doesn't.
    #Should either auto-fail early dates or actually make it return the right dates.

    #invalid dates
    assert functions.get_weekday('2018','99','23') == False
    assert functions.get_weekday('999999','4','23') == False
    assert functions.get_weekday('2018','4','999999') == False
    assert functions.get_weekday('0','4','23') == False
    assert functions.get_weekday('2018','0','23') == False
    assert functions.get_weekday('2018','4','0') == False

    #leap years
    assert functions.get_weekday('2016','2','29') != False
    assert functions.get_weekday('2018','2','29') == False

    #misc
    assert functions.get_weekday('-2018','-4','-23') == False
    assert functions.get_weekday('hi','hi','hi') == False
    assert functions.get_weekday('1900','4','23') == functions.get_weekday(1900,4,23)

def prev_next_test():
    assert functions.prev(functions.get_weekday('2018','4','23')) == functions.get_weekday('2018','4','16')
    assert functions.next(functions.get_weekday('2018','4','23')) == functions.get_weekday('2018','4','30')
    assert functions.next(functions.get_weekday('1900','4','23')) == functions.get_weekday('1900','4','30')
    assert functions.prev(functions.get_weekday('1900','4','23')) == functions.get_weekday('1900','4','20')    
    assert functions.prev(functions.get_weekday('3000','4','23')) == functions.get_weekday('3000','4','19')
    assert functions.next(functions.get_weekday('3000','4','23')) == functions.get_weekday('3000','4','30')

    assert functions.next(['2018-04-22']) == functions.get_weekday('2018','4','30')
    assert functions.prev(['2018-04-22']) == functions.get_weekday('2018','4','16')
    
    #print(functions.prev(functions.get_weekday('2018','99','23')))
    #Seems like it doesn't check to make sure the week is actually valid and tosses an error if it isn't.
    #If the function is only being called by the prev and next buttons it might not be an issue.
    #Might want to also limit this to whatever get_weekday is limited to, to avoid the same problem.

def check_data_test():
    #basic functionality
    assert functions.check_data("test","t","2018","4","23","12","30","2","30") == True

    #empty fields
    assert functions.check_data("","t","2018","4","23","12","30","2","30") == False
    assert functions.check_data("test","","2018","4","23","12","30","2","30") == False
    assert functions.check_data("test","t","","4","23","12","30","2","30") == False
    assert functions.check_data("test","t","2018","","23","12","30","2","30") == False
    assert functions.check_data("test","t","2018","4","","12","30","2","30") == False
    assert functions.check_data("test","t","2018","4","23","","30","2","30") == False
    assert functions.check_data("test","t","2018","4","23","12","","2","30") == False
    assert functions.check_data("test","t","2018","4","23","12","30","","30") == False
    assert functions.check_data("test","t","2018","4","23","12","30","2","") == False

    #zeroes
    assert functions.check_data("test","t","0","4","23","12","30","2","30") == False
    assert functions.check_data("test","t","2018","0","23","12","30","2","30") == False
    assert functions.check_data("test","t","2018","4","0","12","30","2","30") == False
    assert functions.check_data("test","t","2018","4","23","0","30","2","30") == True
    assert functions.check_data("test","t","2018","13","23","0","30","2","30") == False
    assert functions.check_data("test","t","2018","4","23","12","0","2","30") == True
    assert functions.check_data("test","t","2018","4","23","12","30","0","30") == True
    assert functions.check_data("test","t","2018","4","23","12","30","2","0") == True
    #assert functions.check_data("test","t","2018","4","23","12","30","0","0") == False
    #need to fix this one.

    #other boundary cases
    assert functions.check_data("test","t","2018","4","35","12","30","2","30") == False
    assert functions.check_data("test","t","2018","4","23","24","30","2","30") == False
    assert functions.check_data("test","t","2018","4","23","12","60","2","30") == False
    
    #assert functions.check_data("test","t","2018","4","23","23","30","2","30") == False
    #assert functions.check_data("test","t","2018","4","23","23","45","0","30") == False
    #I forgot if we are allowing events to carry over to the next day or not. Currently, it passes if they carry over.

    
    #assert functions.check_data("test","t","2018","4","23","12","30","2","60") == False
    #need to fix this one as well.

    #negatives
    #also need to fix these    
    #assert functions.check_data("test","t","2018","4","23","12","30","2","-30") == False
    #assert functions.check_data("test","t","2018","4","23","12","30","-2","30") == False
    assert functions.check_data("test","t","2018","4","23","12","-30","2","30") == False
    assert functions.check_data("test","t","2018","4","23","-12","30","2","30") == False
    assert functions.check_data("test","t","2018","4","-23","12","30","2","30") == False
    assert functions.check_data("test","t","2018","-4","23","12","30","2","30") == False
    assert functions.check_data("test","t","-2018","4","23","12","30","2","30") == False

    #misc
    #same problem as with negatives for the hours/minutes on duration.
    #assert functions.check_data("test","t","2018","4","23","12","30","2","a") == False
    #assert functions.check_data("test","t","2018","4","23","12","30","a","30") == False
    assert functions.check_data("test","t","2018","4","23","12","a","2","30") == False
    assert functions.check_data("test","t","2018","4","23","a","30","2","30") == False
    assert functions.check_data("test","t","2018","4","a","12","30","2","30") == False
    assert functions.check_data("test","t","2018","a","23","12","30","2","30") == False
    assert functions.check_data("test","t","a","4","23","12","30","2","30") == False
    

if __name__ == "__main__":
    get_weekday_test()
    prev_next_test()
    check_data_test()
