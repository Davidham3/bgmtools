#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import time
import random
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
	string = '么么哒'
	return HttpResponse(string)

def bgmtools(request):
	a = ''
	b = ''
	f = open('log.txt', 'a')
	s = '***************new viewer****************'
	print s
	f.write(s + '\n')
	dic = {'rand' : random.randint(0, 6)}
	if request.method == 'POST':
		cat = request.POST['cat']
		txt = request.POST['search_text']
		txt = txt.strip()
		txt = txt.split()

		if len(txt) == 2:
			a = txt[0].strip()
			b = txt[1].strip()
		elif len(txt) == 1:
			a = txt[0].strip()
			b = getrand(5, cat)
		elif len(txt) == 0:
			a = getrand(3, cat)
			b = getrand(3, cat)
		ss = '-------------------new post---------------------  ' + a + ' ' + b + ' type ' + str(len(txt)) + '  cat ' + cat
		print ss
		f.write(ss + '\n')
		dic = run(a, b, f, cat)
		f.close()

	return render(request, 'bgmtools.html', {'dic' : dic})

def getrand(times, cat):
	mxusr = 373679
	mxcnt = 0
	rt = ''
	for i in range(0 , times):
		tcnt = 0
		a = str(random.randint(1, mxusr))
		myheaders = {'User-Agent': 'Chrome/61.0.3163.100'}
		urla = 'https://bgm.tv/' + cat + '/list/' + a + '/collect'
		reqa = urllib2.Request(url=urla, headers=myheaders)
		stra = urllib2.urlopen(reqa).read()
		soupa = BeautifulSoup(stra, 'html.parser', from_encoding='utf-8')
		ss = str(soupa.find('ul', class_='navSubTabs'))
		p1 = ss.find('过')
		if p1 == -1:
			tcnt = 0
		else:
			p2 = ss.find('(', p1)
			p3 = ss.find(')', p2)
			tcnt = int(ss[p2 + 1 : p3])
		if tcnt >= mxcnt:
			rt = a
			mxcnt = tcnt
	return rt

def run(a, b, f, cat):
	ss = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print ss
	f.write(ss + '\n')
	nicka = ''; nickb = ''; avatera = ''; avaterb = ''
	itemsa = []; itemsb = []
	id = []; img = []; namechs = []; namejp = []; tip = []
	stara = []; starb = []; tagsa = []; tagsb = []
	datea = []; dateb = []; txta = []; txtb = []
	rand = random.randint(0, 6)
	myheaders = {'User-Agent': 'Chrome/61.0.3163.100'}
	flaga = 1
	flagb = 1
	for i in range(1, 999999):
		print 'page' + str(i)
		f.write('page' + str(i) + '\n')
		if flaga == 1:
			urla = 'https://bgm.tv/' + cat + '/list/' + a + '/collect?page=' + str(i)
			reqa = urllib2.Request(url=urla, headers=myheaders)
			stra = urllib2.urlopen(reqa).read()
			soupa = BeautifulSoup(stra, 'html.parser', from_encoding='utf-8')
			titemsa = soupa.find('ul', class_='browserFull')
		if flagb == 1:
			urlb = 'https://bgm.tv/' + cat + '/list/' + b + '/collect?page=' + str(i)
			reqb = urllib2.Request(url=urlb, headers=myheaders)
			strb = urllib2.urlopen(reqb).read()
			soupb = BeautifulSoup(strb, 'html.parser', from_encoding='utf-8')
			titemsb = soupb.find('ul', class_='browserFull')

		if i == 1:
			if (stra.find('数据库中没有查询到该用户的信息') != -1 or strb.find('数据库中没有查询到该用户的信息') != -1):
				ss = 'error ' + a + ' ' + b
				print ss
				f.write(ss + '\n')
				return {'error': 'error', 'rand': random.randint(0, 6)}

			nicka = soupa.find('h1', class_='nameSingle').find('div', class_='inner').a.get_text()
			ta = soupa.find('h1', class_='nameSingle').find('small', class_='grey').get_text()
			a = ta[1 : ]
			avatera = str(soupa.find('span', class_='avatarNeue avatarSize75'))
			avatera = avatera[avatera.find('/') + 2 : avatera.find(')') - 1]

			nickb = soupb.find('h1', class_='nameSingle').find('div', class_='inner').a.get_text()
			tb = soupb.find('h1', class_='nameSingle').find('small', class_='grey').get_text()
			b = tb[1 : ]
			avaterb = str(soupb.find('span', class_='avatarNeue avatarSize75'))
			avaterb = avaterb[avaterb.find('/') + 2 : avaterb.find(')') - 1]

			print nicka,nickb
			ss = a + ' ' + b
			f.write(ss + '\n')

		if len(titemsa) == 0 and len(titemsb) == 0:
			break
		if len(titemsa) == 0:
			flaga = 0
		if len(titemsb) == 0:
			flagb = 0
		for itema in titemsa:
			itemsa.append(itema)
		for itemb in titemsb:
			itemsb.append(itemb)
		if len(itemsa) == 0 or len(itemsb) == 0:
			break

	for itema in itemsa:
		itemida = itema.a['href']
		itemida = itemida[itemida.rfind('/') + 1 : ]
		for itemb in itemsb:
			itemidb = itemb.a['href']
			itemidb = itemidb[itemidb.rfind('/') + 1 : ]
			if itemida == itemidb:
				id.append(itemida)
				img.append(itema.img['src'])
				tip.append(itema.find('p', class_='info tip').get_text())
				namechs.append(itema.find('a', class_='l').get_text())
				tnamejp = itema.find('small', class_='grey')
				if not tnamejp is None:
					namejp.append(tnamejp.get_text())
				else:
					namejp.append('')

				staraflag = 0
				for i in range(1, 11):
					tstara = itema.find('span', class_='sstars' + str(i) + ' starsinfo')
					if not tstara is None:
						staraflag = 1
						stara.append('sstars' + str(i) + ' starsinfo')
						break
				if staraflag == 0:
					stara.append('None')
				datea.append(itema.find('span', class_='tip_j').get_text())
				ttagsa = itema.find('span', class_='tip')
				if not ttagsa is None:
					tagsa.append(ttagsa.get_text())
				else:
					tagsa.append('')
				ttxta = itema.find('div', class_='text')
				if not ttxta is None:
					txta.append(ttxta.get_text())
				else:
					txta.append('')

				starbflag = 0
				for i in range(1, 11):
					tstarb = itemb.find('span', class_='sstars' + str(i) + ' starsinfo')
					if not tstarb is None:
						starbflag = 1
						starb.append('sstars' + str(i) + ' starsinfo')
						break
				if starbflag == 0:
					starb.append('None')
				dateb.append(itemb.find('span', class_='tip_j').get_text())
				ttagsb = itemb.find('span', class_='tip')
				if not ttagsb is None:
					tagsb.append(ttagsb.get_text())
				else:
					tagsb.append('')
				ttxtb = itemb.find('div', class_='text')
				if not ttxtb is None:
					txtb.append(ttxtb.get_text())
				else:
					txtb.append('')

				break
	ss = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print ss
	f.write(ss + '\n')
	ss = 'suc end'
	print ss
	f.write(ss + '\n')
	id1 = [[], [], []]; img1 = [[], [], []]; namechs1 = [[], [], []]; namejp1 = [[], [], []]; stara1 = [[], [], []]; starb1 = [[], [], []]
	tagsa1 = [[], [], []]; tagsb1 = [[], [], []]; datea1 = [[], [], []]; dateb1 = [[], [], []]; txta1 = [[], [], []]; txtb1 = [[], [], []]; tip1 = [[], [], []]

	for i in range(0, len(id)):
		if stara[i] == 'None' or starb[i] == 'None':
			sa = 10
			sb = 1
		else:
			sa = int(stara[i][6 : stara[i].find(' ')])
			sb = int(starb[i][6 : starb[i].find(' ')])
		if sa >= 7 and sb >= 7:
			id1[0].append(id[i]); img1[0].append(img[i]); namechs1[0].append(namechs[i]); namejp1[0].append(namejp[i])
			stara1[0].append(stara[i]); starb1[0].append(starb[i]); tagsa1[0].append(tagsa[i]); tagsb1[0].append(tagsb[i])
			datea1[0].append(datea[i]); dateb1[0].append(dateb[i]); txta1[0].append(txta[i]); txtb1[0].append(txtb[i]); tip1[0].append(tip[i])
		elif sa < 7 and sb < 7:
			id1[1].append(id[i]); img1[1].append(img[i]); namechs1[1].append(namechs[i]); namejp1[1].append(namejp[i])
			stara1[1].append(stara[i]); starb1[1].append(starb[i]); tagsa1[1].append(tagsa[i]); tagsb1[1].append(tagsb[i])
			datea1[1].append(datea[i]); dateb1[1].append(dateb[i]); txta1[1].append(txta[i]); txtb1[1].append(txtb[i]); tip1[1].append(tip[i])
		else:
			id1[2].append(id[i]); img1[2].append(img[i]); namechs1[2].append(namechs[i]); namejp1[2].append(namejp[i])
			stara1[2].append(stara[i]); starb1[2].append(starb[i]); tagsa1[2].append(tagsa[i]); tagsb1[2].append(tagsb[i])
			datea1[2].append(datea[i]); dateb1[2].append(dateb[i]); txta1[2].append(txta[i]); txtb1[2].append(txtb[i]); tip1[2].append(tip[i])

	dic = {'a' : a, 'b' : b, 'nicka' : nicka, 'nickb' : nickb, 'avatera' : avatera, 'avaterb' : avaterb, 'rand' : rand, 'cat' : cat,
		'info0' : zip(id1[0], img1[0], namechs1[0], namejp1[0], stara1[0], starb1[0], tagsa1[0], tagsb1[0], datea1[0], dateb1[0], txta1[0], txtb1[0], tip1[0]),
		'info1': zip(id1[1], img1[1], namechs1[1], namejp1[1], stara1[1], starb1[1], tagsa1[1], tagsb1[1], datea1[1], dateb1[1], txta1[1], txtb1[1], tip1[1]),
		'info2': zip(id1[2], img1[2], namechs1[2], namejp1[2], stara1[2], starb1[2], tagsa1[2], tagsb1[2], datea1[2], dateb1[2], txta1[2], txtb1[2], tip1[2])}
	return dic


