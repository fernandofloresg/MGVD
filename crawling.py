# System modules
from queue import Queue
from threading import Thread
from boilerpipe.extract import Extractor
import time, re

# Set up some global variables
num_threads = 6
page_number = 1 - num_threads
URLs_queue  = Queue(maxsize=5000)
initial_URL ='http://www.uabc.mx/'

#Prevent the crawling of visitated urls
visitated_urls = []
obtained_links = 0
retained_links = 0
repeated_links = 0 
zero_links = 0
min_links = 0 
extraction_failed_links = 0
reserve_url = []

def getURLs(URL):
    extractor = Extractor(extractor='KeepEverythingExtractor', url=URL)
    pageContent = extractor.getHTML()
    URLs = re.findall('href=[\'"]?(.[^\'" >]+)', pageContent)
    return URLs

def populateQueue(URLs):
    global URLs_queue
    print("URls : ", len(URLs))
    print("Queue size : ", URLs_queue.qsize())
    for entry in URLs:
        if (entry.startswith("http")):
            URLs_queue.put(entry)
    print("Queue size after inserting new URLs: " , URLs_queue.qsize())
    
def populateSet(URLs):
    global reserve_url
    for url in URLs:
        if (url.startswith("http")):
            reserve_url.append(url)


def ExtractPageContent(i, q):
    """By using an infinite loop, this function processes URLs in the queue, one after another.  
    Only exit when the main thread ends.
    """
    global page_number
    global obtained_links
    global retained_links
    global repeated_links
    global zero_links
    global min_links
    global extraction_failed_links
    global URLs_queue
    global reserve_url
    char_number_tolerance = 100
    queue_limit = 1000
    
    while not q.empty():
        url = q.get()
        if(url in visitated_urls):
            repeated_links += 1
        if (url.startswith("http")):
            obtained_links += 1
        if (url.startswith("http") and url not in visitated_urls) :
            try:
                retained_links = retained_links + 1
                extractor = Extractor(extractor='ArticleExtractor', url=url)
                pageContent = extractor.getText()
                if (len(pageContent) == 0):
                    zero_links += 1
                else:
                    if(len(pageContent) < char_number_tolerance ):
                        min_links +=1
                        
                if (len(pageContent) > char_number_tolerance ): 
                    page_number +=1
                    file_name = "C:\MGVD\FC\webPage-" + str(page_number) + ".txt" 

                    f = open(file_name,"w+", encoding="utf-8")
                    f.write(pageContent)
                    f.close()

                    if (page_number <1):
                        URLs = getURLs(url)
                        populateSet(URLs)
                    visitated_urls.append(url)
            except :
                extraction_failed_links += 1
        if (q.qsize() == 1):
            print("set populated " , i)
            if len(reserve_url) > queue_limit:
                populateQueue(reserve_url[:queue_limit])
                auxiliar_url = reserve_url[:]
                reserve_url.clear()
                populateSet(auxiliar_url[queue_limit:])
            else:
                populateQueue(reserve_url)
                reserve_url.clear()
        q.task_done()




# Download the initial web-page and get its URLs
URLs = getURLs(initial_URL)
print('*********', len(URLs), '******** \n')


# Put the URLs into the queue.
URLs_queue.put(initial_URL)
if len(URLs) > 2000:
    populateQueue(URLs[:1800])
    populateSet(URLs[1800:])
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
print('Obtained links: ', obtained_links)
print('Retained links: ', retained_links)
print('Repeated links: ', repeated_links)
print('Empty links: ', zero_links)
print('Under tolerance links: ', min_links)
print('Extraction failed links: ', extraction_failed_links)