from core.nodes.relic import Relic

if __name__=="__main__":
    
    r = Relic()
    r.set_file_type("json")
    r.set_raw_data("{'hello world'}")
    r.create()
    print(r)
    print(r.get_checksum_short())