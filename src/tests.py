from core.file.fileio import FileIO
from core.utils.conversions import Conversions

if __name__=="__main__":
    path="E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme"

    FileIO.clear_file(path)
    FileIO.write_string_append(path,"line1\n")
    FileIO.write_string_append(path,"line2\n")
    FileIO.write_string_append(path,"line3\n")
    FileIO.write_string_append(path,"line4\n")
    content = FileIO.read_string_full("E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme")
    print(content)


    FileIO.write_string_insert_line(path, "overwride", 2)
    content = FileIO.read_string_full("E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme")
    print(content)


    FileIO.write_string_overwride_line(path, "", 2, newline=False)
    content = FileIO.read_string_full("E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme")
    print(content)