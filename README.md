#Programowanie w języku Python

#PyTank



Autorzy:
Paweł Kaleciński
Tomasz Rzepka






#Spis Treści
	1.Informacje Wstępne........................................................................3
	2.Opis Gry..........................................................................................3
		2.1 Cechy Gry............................................................................3
		2.2 Zasady Gry...........................................................................3
		2.3 Przedmioty...........................................................................3
		2.4 Możliwości gracza...............................................................4
	3. Hierarchia klas................................................................................4
	4. Wymagania.....................................................................................5
		5.1 Wymagania systemowe........................................................4
		5.2 Wymagania użyteczności.....................................................4























#1.Informacje wstępne:

		Projekt PyTank realizowany jest w ramach przedmiotu Programowanie w języku 	Python.
		PyTank jest adaptacją gry Tank 1990 pochodządzej z platformy Pegasus. 	Implementacja odbyła się w języku Python 2.7. 
		Dokumentacja ta ma na celu opisać program, by ułatwić użytkowanie oraz służyć 	jako pomoc dla osób, które będą go modyfikować, bądź rozwijać w przyszłości.

#2. Opis Gry:
 
#2.1 Cechy Gry:
		    Gra umożliwia rozgrywkę dla wielu graczy(max. 4). Sterowanie odbywa się za 		pomocą klawiatury. Gracze mogą walczyć między sobą lub z AI(max. 4). W grze 		zawarta jest również fizyka, która odpowiada za odbijanie się pocisków od 			ścian. Do dyspozycji graczy są różnego rodzaju bonusy typu dodatkowe życie, 			tarcza. Celem gry jest wyeliminowanie wszystkich przeciwników na planszy.

#2.2 Zasady Gry:
Gracz wygrywa, gdy pokona wszystkich przeciwników na planszy
Gracz przegrywa, gdy stan jego życia dojdzie do 0

#2.3 Przedmioty:

    Gracz w trakcie rozgrywki będzie znajdował przedmioty. Mogą to być przedmioty leczące – odnawiające część utraconego zdrowia, dodatkowe życia, czasowe premie do ataku i obrony. Przedmioty te będą leżały na planszy. 

                                       
                 		      Speed – zwiększa szybkość ruchów


   
  	Bonus Damage - 1 strzal zadajacy 5 dmg 




	   	      Health – dodaje dodatkowe 5 pkt HP



         Attack Speed – 10 pocisków ma zwiększoną szybkość 



#2.4 Możliwości Gracza:

Gracz ma możliwość strzelania, ruchu w przód, w tył oraz rotacji czołgu
Na planszy znajdują się różnego rodzaju przeszkody, które gracz może wykorzystywać do ukrywania się przed pociskami przeciwników. Gracz może również wykorzystywać przeszkody do uszkadzania przeciwników, dzięki fizyce, która zapewnia odbicie pocisku.

#3. Hierarchia Klas:

			W projekcie PyTank znajduje się kilkanaście klas, które zostały 			      zgrupowane w  2 główne moduły: game_core oraz menu 

1. Moduł game_core zawiera rdzeń całej gry:
actor zawiera informacje na temat czołgow, strzelania, modeli ścian oraz bonusów
game zawiera informacje o pustej planszy
game_data generuje nową grę , importuje informacje pochodzące z actora, zawiera AI przeciwników

2. Moduł menu zawiera menu główne gry w tym ustawienia oraz 
informacje o autorach:
game_menu tworzy menu główne gry, zawiera obsługę klawiatury oraz myszy
menu_item zawiera elementy menu takie jak New Game, Settings, Credist, Exit
credist zawiera informacje o autorach
settings czyli ustawienia gry , możliwość konfiguracji klawiszy, włączania/wyłączania bonusów
KeyConfig konfigurator klawiszy
new_game odpowiada za kreator nowej gry, wybór ilości graczy, modeli czołgów oraz ilość NPC












#4.Wymagania funkcjonalne:

Animacja czołgow
Fizyka odbicia pocisków
Obsługa klawiatury
Dźwięki
Interakcja graczy z bonusami
AI przeciwników

