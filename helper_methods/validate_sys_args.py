from helper_methods.int_try_parse import int_try_parse
import sys

def validate_sys_args() -> bool:
  flag: bool = True
  
  if len(sys.argv) != 6:
    print("ERROR: Five args required: [start day] [start month] [end day] [end month] [year]")
    flag = False
    return flag

  # Check that all args are int values
  for i in range(1, len(sys.argv)):
    if int_try_parse(sys.argv[i])[1] == False:
      print("ERROR: Non-integer value passed as date")
      flag = False
 
  # Make sure that day, month, and year sys.argv args fall within these ranges
  month = range(1,13) 
  day = range(1,32)

  if int(sys.argv[1]) and int(sys.argv[3]) not in day:
    print("ERROR: Day values do not fall within the range 1-31")
    flag = False
  if int(sys.argv[2]) and int(sys.argv[4]) not in month:
    print("ERROR: Month values do not fall within the range 1-12")
    flag = False

  if int(sys.argv[2]) == int(sys.argv[4]) and int(sys.argv[1]) >= int(sys.argv[3]):
    print("ERROR: Start day is greater than or equal to end day.")
    flag = False
  if int(sys.argv[2]) > int(sys.argv[4]):
    print("ERROR:  Start month is greater than end month.")
    flag = False
  
  return flag