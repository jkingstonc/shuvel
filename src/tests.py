from core.nodes.relic import Relic

if __name__=="__main__":
    
    r = Relic()
    r.set_origin_directory("E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles")
    r.set_origin_file("meme")
    r.set_creation_date()
    r.set_origin_data_contents("test contents.")
    r.checksum_me()
    print(r)