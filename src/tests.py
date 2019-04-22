from core.nodes.relic import Relic
from core.file.projectfiles import ProjectFiles

if __name__=="__main__":
    
    # r = Relic()
    # r.set_creation_date()
    # r.set_storage_data_contents("test contents.")
    # r.checksum_me()
    # r.dump()
    # r_loaded=Relic.load(r.checksum)
    # print(r)


    ProjectFiles.init_project("E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\test_project\\")
    print(ProjectFiles.check_project_in_path("E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\test_project\\"))
