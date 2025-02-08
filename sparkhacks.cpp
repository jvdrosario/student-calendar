
#include <iostream>

// Include the memory header to use smart pointers (std::unique_ptr).
#include <memory>

// Include the string header for using std::string.
#include <string>

#include <poppler-document.h>

#include <poppler-page.h>


/
int main(int argc, char* argv[]) {
    //Pdf
    std::string pdf_path = C:\Users\skpra\Downloads\Syllabus;
    
    
    // Store the provided PDF file name in a std::string.
    std::string filename = argv[1];
    
    
    // Load the PDF document using Poppler.
    std::unique_ptr<poppler::document> doc(poppler::document::load_from_file(filename));
    
   //total page
    int num_pages = doc->pages();
    
    // Loop through all the pages in the document.
    for (int i = 0; i < num_pages; ++i) {
        
        std::unique_ptr<poppler::page> page(doc->create_page(i));

        std::string page_text = page->text();

        // Optionally, print a header indicating the page number.

        std::cout << "---- Page " << (i + 1) << " ----" << std::endl;

        // Output the extracted text to the console.
        std::cout << page_text << std::endl;
    }
    
  
    return 0;
}
