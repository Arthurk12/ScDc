import requests
from bs4 import BeautifulSoup
from selenium import webdriver

chrome_path = "/media/arthur/Arthur/environments/my_env/chromedriver"


print("--Prototipo de Scraper de Hoteis--")
city = input("Cidade: ")
arq = open("hoteis.txt", "w")


if(city.lower() == "porto alegre"):
    city = 5822
    cityu = "Porto Alegre"
elif(city.lower() == "brasilia"):
    city = 926
    cityu = "Brasilia"
elif(city.lower() == "fortaleza"):
    city = 2302
    cityu = "Fortaleza"
elif(city.lower() == "maceio"):
    city = 4430
    cityu = "Fortaleza"
elif(city.lower() == "rio de janeiro"):
    city = 6381
    cityu = "Rio de Janeiro"
elif(city.lower() == "vitoria"):
    city = 7907
    cityu = "Vitoria"
else:
    city = 6574
    cityu = "São Paulo"

arq.write("Lista de Hoteis para " + cityu + "\n")

page=1
quit=0

while(quit==0):
    url = 'https://www.decolar.com/hoteis/hl/' + str(city) + '/i' + str(page)

    driver = webdriver.Chrome(chrome_path)
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()


    html_soup = BeautifulSoup(res,"lxml")
    html_notfound = html_soup.find('p', {'class' : 'eva-3-p message-text'})

    if(hasattr(html_notfound, 'text') and html_notfound.text == "Não encontramos hospedagens disponíveis com as características selecionadas.  Remover os filtros para ver todos os hospedagens."):
        quit = 1
        pass

    hotels_container = html_soup.find('div', {'id' : 'hotels'})
    all_hotels_box = hotels_container.find_all('div', {'class' : 'results-cluster-container'})

    for sno, hotels in enumerate(all_hotels_box, 1):
        title = hotels.find('a', {'class' : 'upatracker'})
        preco = hotels.find('li', {'class' : '-lg hf-pricebox-price hf-robot-price'})
        nota = hotels.find('span', {'class' : '-eva-3-tc-white rating-text -eva-3-bold'})

        space = "   "
        if(hasattr(title, 'text')):
            print(sno, title.text)
            arq.write(str(sno) + " " + title.text + "\n")
        else:
            print(sno, space + "s/t")
            arq.write(str(sno) + " " + space + "s/t" + "\n")

        if(hasattr(preco, 'text')):
            print(space + preco.text)
            arq.write(space + preco.text + "\n")
        else:
            print(space + "s/p")
            arq.write(space + "s/p" + "\n")

        if(hasattr(nota, 'text')):
            print(space + nota.text)
            arq.write(space + nota.text + "\n")
        else:
            print(space + "s/n")
            arq.write(space + "s/n" + "\n")

    page+=1

arq.write("Fim da Busca!")
arq.close()