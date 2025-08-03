
#bad - will be confusing in long run as there will be no error message
def function_bad():
    pass

#good - will output an error with specified information
def function_good():
    raise NotImplementedError('function_good() - information')

#main code to be ran
def main() -> None:
    function_bad()
    function_good()

#put code here that only needs to run here and nowhere else
if __name__ == '__main__':
    main()
