
# my chosen structure of website was a list of points (and subpoints) related to each concept
# this complicated getting the data as well as using them
# 
# I am afraid that this is not the most optimal way of getting there, but it is the best I can do so far ;)



# Following procedures take a string as an input and output a list with the following data structure:
# [lesson name,[concepts]]
# where concepts are structured in the following way:
# [[name of concept 1,[point 1 of concept 1, point 2, [optional-sublist related to point 2], point 3, ...]]
# [name of concept 2, [list of points and subpoints related to concept 2]]]

def get_data(text):     # create data structure out of a string
  data = []
  lesson_name = [text[:text.find('\n\n')]]
  data += lesson_name
  concepts = []
  text = text[len(lesson_name[0]):]

  while text.find('\n\n') == 0:
    concept, text = get_concept(text)
    concepts += [concept]

  data += [concepts]
  return data

def get_concept(text):
  concept = [text[2:text.find('\n  ')]]
  text = text[len(concept[0])+2:]
  points, text = get_points(text)
  concept += [points]
  return concept, text

def get_points(text):
  point_start = '\n  '
  add_point_start = '\n    '
  points = []
  while text.find(point_start) == 0:
    add_points = []
    while text.find(add_point_start) == 0:
      end = text.find('\n', 1)
      add_points += [text[5:end]]
      text = text[end:]

    if add_points:
      points += [add_points]
    else:
      end = text.find('\n', 1)
      if len(text[3:end]):
        points += [text[3:end]]
      text = text[end:]

  return points, text



# helping procedures:

def reorder_list(alist):        # reorder list to position sublists before the parent points in a list
  if is_list(alist) == False:
    return alist
  for item in alist:
    item = reorder_list(item)
    if is_list(item):
      i = alist.index(item)
      alist[i-1:i+1] = reversed(alist[i-1:i+1])
  return alist

def tab(n):         # create string of n tabs (each tab == 2 spaces)
  return '  '*n

def is_list(item):                # check whether item is a list
  return isinstance(item, list)



# following are main procedures that take string as an input,
# use other procedures to create a data structure from which html lesson content is created

def create_lesson(text):
  title, concepts = get_data(text)[0], get_data(text)[1]      # create data structure
  l_open = '<div class="lesson">\n'
  l_head = tab(1) + '<h3>%s</h3>\n\n' % (title)
  l_body = ''
  for con in concepts:
    l_body += create_concept(con[0], con[1])
  l_close = '</div>\n'
  return l_open + l_head + l_body + l_close


def create_concept(title, descr):
  descr = reorder_list(descr)
  con_open = tab(1) + '<div class="concept">\n'
  con_head = tab(2) + '<h4>%s</h4>\n\n' %(title)
  ul = create_ul(descr)
  con_close = '\n' + tab(1) + '</div>\n'
  return con_open + con_head + ul + con_close





def create_ul(descr, level = 0):
  if is_list(descr) == False:        # if descr is just one str, put into list
    descr = [descr]
  
  depth = ''              # decide class attribute based on level
  if level != 0:
    depth = ' add'

  ul_open = tab(2 + level) + '<ul class="points%s">' % (depth)      # indentation depends on level
  ul = ''
  ul_close = '\n' + tab(2 + level) + '</ul>'
  subs = []

  for item in descr:
    if is_list(item):      # if item is a list (means it contains additional points related to the next item)
      subs += item                  # add the item (list) to subs for later use and continue to next item in descr
      continue

    ul += '\n' + tab(3+level) + '<li>' + '\n' + tab(4 + level) + (item)

    if subs:                                              # if there is a list of additional subpoints stored
      ul += '\n' + (create_ul(subs, level = level + 2))   # create sublist from those points and add it to this line item
      subs = []                                           # empty list of subpoints for later use

    ul += '\n' + tab(3 + level) + '</li>'

  return ul_open + ul + ul_close



# test cases:

lesson1 = '''Lesson 1 - Intro to "serious" programming

computer science
  how to solve problems by breaking them into smaller pieces
  precisely and mechanically describing a sequence of steps to solve a piece in a way that is executable by a computer

computer
  universal machine that can do anything as long as there is a program written for that purpose
  useless machine, that can do nothing unless a program tells it what to do

python
  named after Monty Python [ https://www.youtube.com/watch?v=5Zyv6YHR_UE ]
  high level language
    python interpreter (a program) 'translates' our code into zeros and ones

language ambiguity 
  different people might interpret the same message differently due to following different logical rules (interpretation is highly subjective) 
  reason why we need a programming language (less words, less rules, more strict) 

vocab:
  expression - valid (executable) programming statement
  integer - number without a decimal
  float - number with a decimal
'''

lesson2 = '''Lesson 2 - Variables and Strings

variable
  kind of container that can hold any assigned (stored) value or any other expression under a name of our choice (almost)
  the assigned value or any expression can then be used anywhere and any number of times in the rest of the code
  avoiding repetition, improving readability
  variables are assigned through "=" sign (unlike in math, "=" sign does not mean that left and right sides are equal, it is more like arrow - right side is assigned to left side)
    syntax: variable_name = expression
    to assign value 7 to variable days: days = 7
    python always evaluates the right side first and only then assigns the result to the variable on the left side

string
  sequence of characters between single or double quotes (one or another, but never one at the beginning and the other at the end)
  we can concatenate strings using "+" sign ('uda'+'city' would result in string 'udacity')
  numbers can be part of strings but they "lose" their mathematical properties and become just letters ('2' + '2' would result in string '22')
  each letter in a string has its index number - position within a string -1 (it is -1 because index of first letter is 0)
  sequencing
    we can select part of a string by defining start index position and end(+1) index position of our selection
    good explanation can be found [here]  https://www.udacity.com/course/viewer#!/c-ud552-nd/l-3574398630/m-48687716
'''

lesson3 = '''Lesson 3 - Input -> Function -> Output

function
  sequence of steps that transform given set of inputs into desired set of outputs
  once properly designed/written, functions can be called any number of times and can be used inside other functions

making vs. using a function
  to make a function, we need to define it:
    syntax: dev function_name(inputs):
  to use a function, we just need to call it and based on its purpose, it will (or will not) return some result (output)
  '''

lesson4_5 = '''Lesson 4&5 - Decisions, Repetition and Structured Data

decisions
  one of the core concepts of making programming universal
  achieved through if statements
    basic idea: if something is true, perform a desired action (otherwise do something else)
    syntax example: ######PICTURE######

repetition
  necessary for code efficiency - we do not have to code the same operation again and again
  achieved through while and for statements
    while - while something is true, keep performing a desired action
    for - for defined number of times (usually linked to range, or number of items in a list) perform a desired action (often on/with each of those items)

structured data
  list is an example of structured data
  syntax: [item1, item2, item3, ...]
  list can contain any data type (string, number, other lists) or even a combination
'''

print create_lesson(lesson2)







