from src import paper_link, preprocessings, unique, misc
import argparse
try:
    import bibtexparser
except ImportError:
    print("Please install bibtexparser by running 'pip install bibtexparser'.")


def add_url_to_bib(bib_path, output_path = None, semantics_scholar_api_key = None):
    if output_path is None:
        output_path = bib_path
    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)
        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)
        paper_link.add_url_by_Arxiv_number(library)
        paper_link.add_url_by_doi(library)
        paper_link.add_url_by_scholar_search(library, semantics_scholar_api_key)
        paper_link.final_scan(library)
        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)
        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")


def duplicate_remove(bib_path, output_path = None):
    if output_path is None:
        output_path = bib_path
    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)
        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)
        library, num, instructions = unique.unique(library)
        if num > 0:
            print(f"\033[31m{num} repeated entries are removed.\033[0m")
        else:
            print("\033[32mClean Library.\033[0m")
        if len(instructions) > 0:
            print("\033[31mRequired cite entry replacements:")
            for line in instructions:
                print("\033[31m" + line + "\033[0m")
            with open('replacement.txt', 'w') as instructions_file:
                for line in instructions:
                    instructions_file.write(line + '\n')
            print("\033[31mReplacement instructions are saved to replacement.txt.\033[0m")
        else:
            print("\033[32mNo cite entry replacement required.\033[0m")
        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)
        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")

def capitalize_title(bib_path, output_path = None):
    count = 0
    if output_path is None:
        output_path = bib_path
    if preprocessings.is_utf8(bib_path):
        replacement = preprocessings.non_standard_entrance_replacement()
        replacement.encode(bib_path)
        with open(bib_path, 'rb') as bibtex_file:
            library = bibtexparser.load(bibtex_file)
        for paper in library.entries:
            new_title = misc.capitalize_title(paper['title'])
            if new_title != paper['title']:
                print(f"{paper['title']} -> {new_title}.")
                paper['title'] = new_title
                count += 1
        if count > 0:
            print(f"\033[31m{count} titles are capitalized.\033[0m")
        else:
            print("\033[32mAll title is clean, no capitalization needed.\033[0m")
        with open(output_path, 'w') as bibtex_file:
            bibtexparser.dump(library, bibtex_file)
        replacement.decode(output_path)
    else:
        print(f"{bib_path} is not encoded in UTF-8. Please convert it to UTF-8 and try again.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A small tool to process .bib files efficiently. Maybe for your dissertation?',
        epilog='Written by Yufeng Zhao (alias: Hakaze Cho)'
    )
    parser.add_argument(
        'task',
        type=str,
        help='The task to be executed. Options: "url"; "unique"; "cap".'
    )
    parser.add_argument(
        'bib_path',
        type=str,
        help='The path to the .bib file.'
    )
    parser.add_argument(
        '-o',
        '--output_path',
        type=str,
        help='The path to the output .bib file.'
    )
    parser.add_argument(
        '-k',
        '--semantics_scholar_api_key',
        type=str,
        help='The API key for Semantic Scholar.'
    )
    args = parser.parse_args()
    if args.task == "url":
        add_url_to_bib(args.bib_path, args.output_path, args.semantics_scholar_api_key)
    elif args.task == "unique":
        duplicate_remove(args.bib_path, args.output_path)
    elif args.task == "cap":
        capitalize_title(args.bib_path, args.output_path)
    else:
        print(f"Task {args.task} is not supported. Please choose from 'url' or 'unique'.")