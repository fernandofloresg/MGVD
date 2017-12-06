# System modules
from queue import Queue
from threading import Thread
from boilerpipe.extract import Extractor
import time, re

# Set up some global variables
num_threads = 10
page_number = 1 - num_threads
URLs_queue  = Queue()
initial_URL ='https://es.wikipedia.org/wiki/Filipinas'

def getURLs(URL):
    extractor = Extractor(extractor='KeepEverythingExtractor', url=URL)
    pageContent = extractor.getHTML()
    URLs = re.findall('href=[\'"]?(.[^\'" >]+)', pageContent)
    return URLs

def populateQueue(URLs):
    global URLs_queue
    for entry in URLs:
        if (entry.startswith("http")):
            print ('Queuing:', entry)
            URLs_queue.put(entry)


def ExtractPageContent(i, q):
    """By using an infinite loop, this function processes URLs in the queue, one after another.  
    Only exit when the main thread ends.
    """
    global page_number
    
    while True:
        print ('\n %s: Looking for the next URL' % i)
        url = q.get()
        if url.startswith("http"):
            try:
                print ('\n %s: Downloading:' % i, url)
                extractor = Extractor(extractor='ArticleExtractor', url=url)
                pageContent = extractor.getText()
                
                page_number +=1
                file_name = "C:\MGVD\FC\webPage-" + str(page_number) + ".txt" 
                print(file_name)
        
                f = open(file_name,"w+", encoding="utf-8")
                f.write(pageContent)
                f.close()
                
                if (page_number < 10):
                    URLs = getURLs(url)
                    populateQueue(URLs)
            except:
                print("\n**** Extraction failed **** \n")
                
        q.task_done()


# Download the initial web-page and get its URLs
URLs = getURLs(initial_URL)
print('*********', len(URLs), '******** \n')

# Put the URLs into the queue.
URLs_queue.put(initial_URL)
populateQueue(URLs)
time.sleep(1)    
    
# Set up some threads to fetch web-pages data
for i in range(num_threads):
        worker = Thread(target=ExtractPageContent, args=(i, URLs_queue,))
        worker.setDaemon(True)
        worker.start()
time.sleep(1)

start_time = time.clock()

# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
print ('*** Main thread waiting *** \n')
URLs_queue.join()
print ('*** Done *** \n')

# Elapsed time estimation
elapsed_time = time.clock() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)