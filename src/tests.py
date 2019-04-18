from core.file.fileio import FileIO
from core.utils.conversions import Conversions

if __name__=="__main__":

    FileIO.write_bytes_overwride(
        "E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme",
        Conversions.int_to_bytes(1234)
    )
    FileIO.write_bytes_append(
        "E:\\university\\OneDrive - Lancaster University\\programming\\python\\shuvel\\res\\testfiles\\meme",
        Conversions.str_to_bytes("hehhee")
    )