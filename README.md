# BI_2020_fastq_filtrator
Simple FASTQ filtration script made by Ignat Sonets and Anna Kvach as a part of our BI 2020 Python course.

Usage:
```
python3 filter.py [--keep-filtered] --min-length [int] --gc_bounds [float1] [float2](optional) --output_base_name [text] your_fastq_file.fastq
```
Arguments to specify:
1) ``` --keep-filtered ```: if activated, it allows to store both passed and failed reads in seperate .fastq files;
2) ```--min-length ``` : describes minimal read length to pass QC (if read is shorter than this length, this read will be discarded);
3) ```--gc_bounds ```: describes either right bound of GC% interval (so reads with bigger GC% will be discarded) (1 float number from input will be taken as a right bound) or left and right bounds of desired GC% interval (so 1st float number from input will be taken as a left bound and 2nd number will be taken as a right bound. Usage of 2 bounds is optional) NB! If desired, bounds could be specified as integers;
4) ```--output_base_name ```: allows to change name of your .fastq result(s) file(s). If not specified, result(s) filenames wiil be:
```your_fastq_file_passed.fastq/your_fastq_file_failed.fastq ```

Enjoy!

Please report any bugs to ignatsonets@gmail.com

