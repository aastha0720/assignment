#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
PDF_file = "file_1.pdf"


# In[2]:


pages = convert_from_path("file_3.pdf", 500)


# In[3]:


import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
stop = stopwords.words('english')
def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names
image_counter = 1
# Iterate through all the pages stored above 
for page in pages: 
  
    # Declaring filename for each page of PDF as JPG 
    # For each page, filename will be: 
    # PDF page 1 -> page_1.jpg 
    # PDF page 2 -> page_2.jpg 
    # PDF page 3 -> page_3.jpg 
    # .... 
    # PDF page n -> page_n.jpg 
    filename = "page_"+str(image_counter)+".jpg"
      
    # Save the image of the page in system 
    page.save(filename, 'JPEG') 
  
    # Increment the counter to update filename 
    image_counter = image_counter + 1
  
''' 
Part #2 - Recognizing text from the images using OCR 
'''

# Variable to get count of total number of pages 
filelimit = image_counter-1
  
# Creating a text file to write the output 
outfile = "out_text.txt"
  
# Open the file in append mode so that  
# All contents of all images are added to the same file 
f = open(outfile, "a") 
  
# Iterate from 1 to total number of pages 
for i in range(1, filelimit + 1): 
  
    # Set filename to recognize text from 
    # Again, these files will be: 
    # page_1.jpg 
    # page_2.jpg 
    # .... 
    # page_n.jpg 
    filename = "page_"+str(i)+".jpg"
          
    # Recognize the text as string in image using pytesserct 
    text = str(((pytesseract.image_to_string(Image.open(filename))))) 
    f.write(text) 
f.close() 
f = open(outfile, "r") 
text = f.read()
f.close()
names = list(set(extract_names(text)))
print(names)    


# In[4]:


for name in names:
    if len(re.findall(r'accused\s*'+name,text)) != 0:
        print(name)
text = text.lower()
if re.search("acquited",text):
    print("Acquited")
elif re.search("convicted",text):
    print("Convited")   
print(re.findall(r'(\d+/\d+/\d+)',text)[-1])


# In[5]:


l = re.findall(r'sec.\w*\s*\d*',text)
lt = ' '.join(map(str, l)) 
s = list(set(re.sub(r'sec.\w*','',lt).split()))
print(s)


# In[ ]:




