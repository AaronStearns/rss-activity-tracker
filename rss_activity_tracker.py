from helper_methods.company_activity_tracker import company_activity_tracker
from helper_methods.validate_sys_args import validate_sys_args
import sys

def main():
  is_valid: bool = validate_sys_args()

  if is_valid:
    print(company_activity_tracker(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])))

if __name__ == "__main__":
  main()
