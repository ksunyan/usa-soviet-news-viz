# Tools for Bulk Newspaper Data Download, Extraction, and Tokenization

## Download Script
`get_bulk_files_by_newspaper.py` is a Python script for downloading bulk OCR data from the Chronicling America database. 

### Example Usage
```
python get_bulk_files_by_newspaper.py https://chroniclingamerica.loc.gov/lccn/sn83045499.json 1917-01-01 1953-12-31 -o files
```
downloads all bulk OCR data files that contain issues of The Daily Alaska Empire from between January 1, 1917 and December 31, 1953. All files are downloaded to the `files` subdirectory. 

### Command Line Options
Coming soon

## Extract and Merge Script
`extmerge.sh` is a shell script for extracting text files from `.tar.bz2` files. It extracts only the `.txt` files while preserving the original directory structure (LCCN/year/month/day/edition/sequence).

### Steps
1. Copy `extmerge.sh` to the directory containing the `.tar.bz2` files.
2. Navigate to the directory containing the `.tar.bz2` files.
3. Modify the script by changing instances of `snxxxxxxxx` to the LCCN for that publication. The LCCN can be found on the "About" page for the publication on the Chronicling America website. Do not include spaces when specifying the LCCN in the script. For example, the LCCN for *The Daily Alaska Empire* is sn83045499. 
4. Run the following command from the present working directory:
    ```
    for FILE in *.tar.bz2; do ./extmerge.sh $FILE; done;
    ```
5. Remove the `.tar.bz2` files and any remaining directories with names formatted `snxxxxxxxx`.

## Tokenization Script
### Dependencies
* `nltk.corpus.words` and `nltk.corpus.stopwords`. Use a Python interpreter to run the following: 
    ```
    import nltk
    nltk.download()
    ```