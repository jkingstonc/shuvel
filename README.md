# shuvel
A virtual file system for storing, archiving and updating data objects

# commands
* initialise a project `shuvel init`                      
* View project status `shuvel status`
* Create a new file named test_file of type relic in the root directory `shuvel new -n test_file -t relic -d root`
* Create a new file of type collection (folder) `shuvel new -n subfolder -t collection`
* Move test_file to subfolder `shuvel move -n test_file d subfolder`                                                           
* Pipe a text file into test_file and override it `shuvel add -n test_file -w overwride -i file -m to_add.txt`                                                      
* Append some text to test_file `shuvel add -n test_file -w append -i text -m "appending whooo"`                                     
* Archive test_file `shuvel archive -n "archiving test_file" -d test_file -m "overwritten test_file and added stuff"`   
* View the creation date of test_file `shuvel peek -n test_file -d  creation_date`                                                       
* Pipe the contents of test_file into a file on disk `shuvel peek -p test_file test_file_data.txt`
* Peek the contents of a file with specified shorthand hash `shuvel peek -n 123adf`                                                               
