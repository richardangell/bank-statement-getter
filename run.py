import bankstatementgetter.export as export


def test():
    
    halifax_statement_file = export.export_halifax_statements()
    
    print(halifax_statement_file)

    
    
    
if __name__ == '__main__':
    
    test()
    