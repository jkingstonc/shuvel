from core.file.fileio import FileIO
from core.utils.conversions import Conversions

if __name__=="__main__":
    path="E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme"

    FileIO.clear_file(path)
    FileIO.write_string_append(path,"line1\n")
    FileIO.write_string_append(path,"line2\n")
    FileIO.write_string_append(path,"line3\n")
    FileIO.write_string_append(path,"line4\n")

    content = FileIO.read_string_line_num("E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme", 1,3)
    print(content)