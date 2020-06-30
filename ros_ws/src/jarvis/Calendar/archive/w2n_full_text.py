
# a mapping of digits to their names when they appear in the
# relative "ones" place (this list includes the 'teens' because
# they are an odd case where numbers that might otherwise be called
# 'ten one', 'ten two', etc. actually have their own names as single
# digits do)
class my_w2n:
    __ones__ = { 'one':   1, 'eleven':     11,
                    'two':   2, 'twelve':     12,
                    'three': 3, 'thirteen':   13,
                    'four':  4, 'fourteen':   14,
                    'five':  5, 'fifteen':    15,
                    'six':   6, 'sixteen':    16,
                    'seven': 7, 'seventeen':  17,
                    'eight': 8, 'eighteen':   18,
                    'nine':  9,
                    'ten':10 ,  'nineteen':   19,
                    'half':0.5 }

    # a mapping of digits to their names when they appear in the 'tens'
    # place within a number group
    __tens__ = {    'nhalf': 30,
                    'twenty':  20,
                    'thirty':  30,
                    'forty':   40,
                    'fifty':   50,
                    'sixty':   60,
                    'seventy': 70,
                    'eighty':  80,
                    'ninety':  90 }

    # an ordered list of the names assigned to number groups
    __groups__ = {  'hundred':100,
                    'thousand':  1000,
                    'million':   1000000,
                    'billion':   1000000000,
                    'trillion':  1000000000000 }

                

    def __init__(self):
        self.info = "This will convert words to numbers"
    
    # find
    def find_grands(self,s):

        if type(s) is str:
            words = s.split() 
        elif type(s) is list:
            words=s
        words.append('d')
        new_value=0
        count=0   # count to know starta and end of numbers
        old_value=0  
        start = None
        got_and = False
        try:
            while(count<len(words)):
                not_one = True
                not_ten = True
                not_grand = True
                if words[count] in self.__ones__.keys():
                    if start is None: start = count
                    not_one=False
                    new_value = self.__ones__.get(words[count])
                    count+=1
                    if count==len(words):
                        if old_value>new_value:
                            old_value = old_value+new_value
                        # else:
                        #     non_currency = True
                        #     #old_value = old_value*100 + new_value
                        #     old_value = str(old_value)+' h '+str(new_value)+' m '
                        #     end = count
                        #     break
                    if words[count] in self.__groups__.keys():
                        if start is None: start = count
                        not_grand = False
                        new_value *= self.__groups__.get(words[count])
                        count+=1
                        old_value=old_value+new_value

                elif words[count] in self.__groups__.keys():
                    if start is None: start = count
                    not_grand = False
                    start = count
                    new_value =self.__groups__.get(words[count])
                    count+=1
                    old_value=old_value+new_value

                if words[count] in self.__tens__.keys():
                    if start is None: start = count
                    not_ten = False
                    if new_value>99:
                        old_value = old_value + self.__tens__.get(words[count])
                        count+=1
                    else:
                        non_currency = True
                        #old_value = old_value+new_value*100 + self.__tens__.get(words[count])
                        old_value = str(new_value)+' h '+str(self.__tens__.get(words[count]))+' m '
                        count+=1

                if not_grand and not_ten and not not_one:
                    if got_and:
                        old_value = old_value+new_value
                        got_and = False
                    else:
                        old_value = new_value
                        not_one = True

                # if not_grand and not_ten and not not_one:
                #     old_value = old_value+new_value
                
                if not_grand and not_ten and not_one:
                    
                    if start is not None and words[count]!='and':
                        end = count
                        words = words[:start] + [str(old_value)] + words[end:]
                        new_value = 0
                        start = None
                        old_value=0
                    elif words[count]=='and':
                        got_and=True 
                        count+=1
                    else: count+=1
            if start is not None:
                end = count
                words = words[:start] + [str(old_value)] + words[end:]     
            return words[:-1]
        except IndexError:
            end = count
            words = words[:start] + [str(old_value)] + words[end:]   
            return words[:-1]

    def find_time(self,s):
        short =  False
        '''
        Three hour twenty minutes - 3h20m
        three and half hour- 3h30m
        three hours - 3h
        an hour - 1h
        half an hour - 30m 
        '''   
        if type(s) is list:
            n = ' '
            s = n.join(s)
        if 'half an hour' in s:
            s = s.replace('half an hour','0 h 30 m')
            short = True
        if 'in an hour' in s:
            s =  s.replace('an hour','1 h')
            short = True
        if 'and half' in s:
            s = s.replace('and half', 'nhalf')
            short=True
        if ' hours' in s or 'minutes' in s:
            short = True 
        # if 'half hour' in s or 'half hours' in s:
        #     s = s.replace('half hour','halfhour')
        new_value = self.find_grands(s)
        found=True
        if new_value is None: found = False
        return new_value,found,short

# a = my_w2n()
# s = "let check if this works for remind me in ten to pay three hundred"
# new_value=a.find_time(s)
# new_value = a.find_grands(new_value)

# if new_value is not None:
#     print(new_value)
# else: print("No numbers found")
# print(" ")
# print(s)
# print(" ")





    