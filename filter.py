import sys

# ANNA PART

list_flags_and_options = sys.argv[1:]
last_ind_in_list_flags_and_options = len(list_flags_and_options) - 1

# default values for filtration start
str_new_name = list_flags_and_options[last_ind_in_list_flags_and_options].split('.')[0]
int_min_length = 0
float_left_gc_bound = 0.0
float_right_gc_bound = 0.0
bool_error_output_permission = False

# check is the argument in sys.argv[1:] is a flag
def is_flag(x):
    if "--" in str(x):
        return True
    else:
        return False

# check is the argument in sys.argv[1:] is a int
def isint(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

# check is the argument in sys.argv[1:] is a float
def isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

# check is the argument after flag is ok
def fun(z):
    try:
        x = z
        y = list_flags_and_options.index(x) + 1
        if x in list_flags_and_options:
            if (is_flag(list_flags_and_options[y]) == True) or (y == last_ind_in_list_flags_and_options):
                sys.exit("Ypu forgot to specify values after arguments!")
            else:
                return True
    except ValueError:
        return False

# check is the argument after-after flag is ok
def fun_fun(zz):
    try:
        x = zz
        y = list_flags_and_options.index(x) + 2
        if x in list_flags_and_options:
            if (is_flag(list_flags_and_options[y]) == True) or (y == last_ind_in_list_flags_and_options):
                return False
            else:
                return True

    except ValueError:
        return False

# 1 part
if ".fastq" in str(list_flags_and_options[last_ind_in_list_flags_and_options]):
    str_path_to_dir_with_files = sys.path[0]
    str_input_fastq_file_name = str(sys.argv[len(sys.argv) - 1])
    str_path_to_input_fastq_file = str_path_to_dir_with_files + "/" + str_input_fastq_file_name
else:
    sys.exit("Last argument should be .fastq file name!")

# 2 part
if (is_flag(list_flags_and_options[0]) == False) and (".fastq" not in str(list_flags_and_options[0])):
    sys.exit("You should specify at least 1 flag and file name to start filtering!(or just a file name to remove error message (although filtration won't start)")

# 3 part
z1 = "--output_base_name"

if fun(z1):
    y1 = list_flags_and_options.index(z1) + 1
    list_ = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
    if any(word in str(list_flags_and_options[y1]) for word in list_):
        sys.exit("Your file name contains forbidden symbols such as: < >: \" / \ | ? *. Rename your file to start filtering!")
    else:
        str_new_name = str(list_flags_and_options[y1])


# 4 part
z2 = "--min_length"
fun(z2)

if fun(z2):
    y2 = list_flags_and_options.index(z2) + 1
    if isint(list_flags_and_options[y2]) and (int(list_flags_and_options[y2]) > 0):
        int_min_length = int(list_flags_and_options[y2])
    else:
        sys.exit("Min length value should be integer and be > 0!")


# 5 part
z3 = "--gc_bounds"
fun(z3)

if fun(z3):
    y3 = list_flags_and_options.index(z3) + 1
    if not (isfloat(list_flags_and_options[y3]) or (float(list_flags_and_options[y3]) > 0)):
        sys.exit("Lower GC% bound value should be float and be > 0!")
    elif isfloat(list_flags_and_options[y3]) and (float(list_flags_and_options[y3]) > 0):
        float_left_gc_bound = float(list_flags_and_options[y3])
        zz = z3
        if fun_fun(zz):
            if not (isfloat(list_flags_and_options[y3]) or (float(list_flags_and_options[y3]) > 0)):
                sys.exit("Upper GC% bound value should be float and be > 0!")
            elif isfloat(list_flags_and_options[y3 + 1]) and (float(list_flags_and_options[y3 + 1]) > 0):
                float_right_gc_bound = float(list_flags_and_options[y3 + 1])
                if float_left_gc_bound >= float_right_gc_bound:
                    sys.exit("Lower GC% bound value should be strictly less than upper GC bound!")


if "--keep_filtered" in list_flags_and_options:
    error_output_permission = True
else:
    error_output_permission = False



# IGNAT PART

# GC count caculation
def gc_count(read):
    count = 0
    for base in read:
        if base == 'C' or base == 'G':
            count += 1
    return count * 100 / len(read)
# ez
# check for good reads
def passed(read, int_min_length, float_left_gc_bound, float_right_gc_bound):
    if "--min_length" in list_flags_and_options:
        if len(read) < int_min_length:  # if l(read) < min length => F
            return False
        else:
            return True

    if "--gc_bounds" in list_flags_and_options:
        less = gc_count(read) < float_left_gc_bound # if less than left GC bound => True
        more = gc_count(read) > float_right_gc_bound # if more than right GC bound => True
        if less or more == True:
            return False
        return True
# ez
# save in file
def file_output(readlines, file):
    file.write('\n'.join(readlines) + '\n')
# ez af
# open file
fastq_input = open(str_input_fastq_file_name, 'r')
# read all input lines
all_reads = fastq_input.read().splitlines()
# N of reads in file
total_reads = str(len(all_reads) // 4)
# create output blank file and creating failed .fastq if necessary 
fastq_passed = open(str_new_name+ '_passed.fastq', 'w')  
if error_output_permission == True:
    fastq_failed = open(str_new_name + '_failed.fastq', 'w')
    
# counter for passed/failed reads and their filtration
reads_passed = 0
reads_failed = 0
for i in range(0, len(all_reads), 4): #we need to read lines by 4, e.g. 1-4, 5-8, 9-12 etc.
    current_read = all_reads[i:i + 4] # reading 2nd line where ATGC's are
    if i == 0: # check if empty
        print()
    if passed(current_read[1], int_min_length, float_left_gc_bound, float_right_gc_bound):  
        file_output(current_read, fastq_passed)
        reads_passed += 1
    else:
        if error_output_permission == True: 
            file_output(current_read, fastq_failed)
        reads_failed += 1
        
# don't forget to close file
print('Done!')
print('Total reads number is ' + str_input_fastq_file_name + ': ' + total_reads)
print(str(reads_passed) + ' (' + str(round(reads_passed * 100 / int(total_reads), 2)) + '%) reads passed filtering.')
print(str(reads_failed) + ' (' + str(round(reads_failed * 100 / int(total_reads), 2)) + '%) reads failed filtering.')

fastq_passed.close()
fastq_input.close()
if error_output_permission == True:
    fastq_failed.close()
