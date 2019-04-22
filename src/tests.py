from core.nodes.relic import Relic

if __name__=="__main__":
    
    r = Relic()
    r.set_creation_date()
    r.set_storage_data_contents("test contents.")
    r.checksum_me()
    print(r)