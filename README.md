A collection of tools for revising `.bib` files efficiently. Maybe useful for thesis or dissertation writing.

Author: Hakaze Cho.

## Get started from `Python`

1. Clone this repository to your local machine.

```bash
git clone https://github.com/hc495/bibtools.git
```

2. Install the required packages.

```bash
pip install bibtexparser requests
```

3. Run the script.

```bash
python bibtools.py <task> <input_path> [-o OUTPUT_PATH] [-k SEMANTICS_SCHOLAR_API_KEY]
```

## Get started from `.exe` release (TBA)

1. Download the `.exe` file from the [release page]()

2. Run the script.

```bash
bibtools <task> <input_path> [-o OUTPUT_PATH] [-k SEMANTICS_SCHOLAR_API_KEY]
```

### Tasks `<task>`

- `url`: Add the URL field to each paper in the `.bib` file. Semantic Scholar API Key *can be* used to **accelerate** the process for only efficiency but not accuracy.
   <font color=red>
   Notice: Some papers are not returned with a URL. Please check the command line output and handle them manually.
   </font>
- `unique`: Merge the duplicate papers in the `.bib` file. The papers are considered as duplicates if they have the same title.
    <font color=red>
   During the merging process, some BibTeX entries (citation keys) may be removed. Please check the command line output and manually replace these removed entries in your `\cite{}` with the merged ones.
   </font>
- `cap`: Capitalize the first letter of each word (except the function word) in the title field.

### Input file `<input_path>`

The path to the `.bib` file to be processed.

### Optional arguments

- `-o OUTPUT_PATH`: The path to the output `.bib` file. If not specified, the operation will be done in place.
- `-k SEMANTICS_SCHOLAR_API_KEY`: The API key for the Semantic Scholar API. Semantic Scholar API Key *can be* used to **accelerate** the process for only efficiency but not accuracy.