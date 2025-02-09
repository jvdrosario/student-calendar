import sys


from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    # Try to load the PDF document using pypdf (previously PyPDF2)
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"Error: Could not load the document at {pdf_path}. {e}")
        return

    result = ""

    # Get the total number of pages in the document
    num_pages = len(reader.pages)


    # Loop through all the pages in the document
    for i in range(num_pages):
        page = reader.pages[i]


        # Extract the text from the page
        page_text = page.extract_text()


        # Print a header for the page
        result += f"---- Page {i + 1} ----\n"


        # Output the extracted text to the console
        if page_text:
            result += page_text
        else:
            print(f"Error: No text found on page {i + 1}")

    # print(result)

    return result


if __name__ == "__main__":
    # The first argument is the path to the PDF
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_pdf>")
    else:
        pdf_path = sys.argv[1]
        extract_text_from_pdf(pdf_path)





