import mailbox
from collections import Counter
from email.header import Header, decode_header, make_header
import email.utils 
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import matplotlib.pylab as plt

find = re.compile(r"^[^,]*")

def plotDays(daysCounter):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	x = []
	y = []
	x.append('Mon')
	y.append(daysCounter['Mon'])
	x.append('Tue')
	y.append(daysCounter['Tue'])
	x.append('Wed')
	y.append(daysCounter['Wed'])
	x.append('Thu')
	y.append(daysCounter['Thu'])
	x.append('Fri')
	y.append(daysCounter['Fri'])
	x.append('Sat')
	y.append(daysCounter['Sat'])
	x.append('Sun')
	y.append(daysCounter['Sun'])
	ax.plot(x,y)
	#ax.set_xticklabels(x)
	plt.show()


def strRemplaza(texto):    
	"""Reemplazo de múltiples cadenas en Python."""
	
	remplazo = { 
		'&#225;' : 'á', '&#233;' : 'í', '&#237;' : 'í', '&#243;' : 'ó', 
		'&#250;' : 'ú', '=C3=A1' : 'á', '=C3=A9' : 'é', '=C3=AD' : 'í', 
		'=C3=B3' : 'ó', '=C3=BA' : 'ú', '=E1' : 'á', '=E9' : 'é', '=ED' : 'í', 
		'=F3' : 'ó', '=FA' : 'ú', 'a&#x0301;' : 'á', 'e&#x0301;' : 'é', 
		'i&#x0301;' : 'í', 'o&#x0301;' : 'ó', 'u&#x0301;' : 'ú',
		'=C3=81' : 'Á', '=C3=89' : 'É', '=C3=8D' : 'Í', '=C3=93' : 'Ó', 
		'=C3=9A' : 'Ú', '&#191;' : '¿', '=C3=B1' : 'ñ', '=2C' : ',', 
		'n&#x0303;' : 'ñ'
	} 
	regex = re.compile("(%s)" % "|".join(map(re.escape, remplazo.keys())))
	return regex.sub(lambda x: str(remplazo[x.string[x.start() :x.end()]]), texto)

MBOX = 'C:/MGVD/Mail/Recibidos.mbox'
messagesBody = []
messagesFrom = []
days = []
contMessages  = 0

# Create an mbox that can be iterated over
mbox = mailbox.mbox(MBOX)

print('Getting most common contacts --------------------------')
#Get contacts
for message in mbox:
	contMessages +=1
	#get most common messages 
	messageFrom = make_header(decode_header(message.get('from')))
	#messageFrom = message.get('from')
	messagesFrom.append(messageFrom)
	
#get most common contacts
fromCounter = Counter()
for mFrom in messagesFrom:
    fromCounter[str(mFrom)] += 1
print(fromCounter.most_common(10))

contact_id = 4
#for each message we analize if it is from the desired contact 
print('Getting most word used with most common contact --------------------------')
for message in mbox:
	messageFrom = make_header(decode_header(message.get('from')))
	contact = fromCounter.most_common(10)
	day = email.utils.parsedate_to_datetime(message['date']).weekday()
	days.append(day)
	if messageFrom == contact[contact_id][0]:
		for part in message.walk():
			if(part.get_content_type() == "text/plain"):
				txt = make_header(decode_header(part.get_payload()))
				txt = strRemplaza(str(txt))     
				messagesBody.append(txt)
body = Counter()
for mBody in messagesBody:
	words= word_tokenize(str(mBody))
	useful_words = [word  for word in words if word not in stopwords.words('Spanish')]
	for mWord in useful_words:
		if(len(mWord) > 5 and len(mWord) < 15):
			body[str(mWord)] += 1

print(body.most_common(25))


print('Getting days percentage --------------------------')
#get percentage
y= []
daysCounter = Counter(days)
total_days = sum(daysCounter.values())
for key in sorted(daysCounter.keys()):
	percentage = daysCounter[key] / total_days 
	print(key , percentage, '%')
	y.append(daysCounter[key])

#plot days
plt.plot(y)
plt.show()
