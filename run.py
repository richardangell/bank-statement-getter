import bankstatementgetter.export as export


def run_exporter():
    
    exporter = export.BankStatementGetter()
    exporter.run()
    
    
    
    
if __name__ == '__main__':
    
    run_exporter()
    