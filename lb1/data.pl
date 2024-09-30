% создание персонажей

character(nicole).
character(ellen).
character(nekomata).
character(koleda).
character(grace).
character(rina).
character(lycaon).
character(soldier_11).
character(lucy).
character(piper).
character(nicole).
character(anby).
character(billy).
character(ben).
character(anton).
character(corin).
character(soukaku).
character(qingyi).
character(jane).
character(seth).
character(zhu).

% создание ролей

role(jane, anomaly).
role(grace, anomaly).
role(piper, anomaly).

role(koleda, stun).
role(lycaon, stun).
role(qingyi, stun).
role(anby, stun).

role(rina, support).
role(lucy, support).
role(nicole, support).
role(soukaku, support).

role(seth, defense).
role(ben, defense).

role(ellen, attack).
role(nekomata, attack).
role(soldier_11, attack).
role(zhu, attack).
role(anton, attack).
role(billy, attack).
role(corin, attack).



% создание фракций

fraction(ellen, victoria_Housekeeping_Co).
fraction(rina, victoria_Housekeeping_Co).
fraction(lycaon, victoria_Housekeeping_Co).
fraction(corin,victoria_Housekeeping_Co).

fraction(lucy, sons_of_Calydon).
fraction(piper, sons_of_Calydon).

fraction(soukaku, section_6).

fraction(soldier_11, obols_Squad).

fraction(nicole, cunning_Hares).
fraction(anby, cunning_Hares).
fraction(billy, cunning_Hares).
fraction(nekomata, cunning_Hares).


fraction(grace, belobog_Heavy_Industries).
fraction(koleda,belobog_Heavy_Industries).
fraction(anton, belobog_Heavy_Industries).
fraction(ben, belobog_Heavy_Industries).

fraction(qingyi,cisrt).
fraction(jane, cisrt).
fraction(seth, cisrt).
fraction(zhu, cisrt).

% создание стихий

element(ellen, ice).
element(lycaon, ice).
element(soukaku, ice).

element(nekomata, physical).
element(piper, physical).
element(billy, physical).
element(corin, physical).
element(jane, physical).

element(grace, electric).
element(rina, electric).
element(anby, electric).
element(anton, electric).
element(qingyi, electric).
element(seth, electric).

element(koleda, fire).
element(soldier_11, fire).
element(ben, fire).
element(lucy, fire).

element(nicole, ether).
element(zhu, ether).
% создание правил

% Правило синхронизации по элементу, роли или фракции
synhronise(Char, Partner) :-
    element(Char, Element), element(Partner, Element), Char \= Partner;
    %role(Char, Role), role(Partner, Role), Char \= Partner;
    fraction(Char, Fraction), fraction(Partner, Fraction), Char \= Partner.

% Правило саппорта под персонажа (саппорт той же стихии).
good_support(Char, Support) :- 
    element(Char, Element), element(Support, Element), role(Support, support), Char \= Support;
    role(Char, anomaly), Support = seth, Char \= Support.

% Правило керри под персонажа (керри той же стихии или анамолист под саппорта анамолиста).
good_carry(Carry, Support) :- 
    element(Carry, Element), element(Support, Element), role(Carry, attack), Carry \= Support;
    role(Carry, anomaly), Support = seth, Carry \= Support.

synchronized_team(Char1, Char2, Char3) :-
  (synhronise(Char1, Char2), synhronise(Char1, Char3)), Char1 \= Char2, Char1 \= Char3, Char2 \= Char3;
  (synhronise(Char1, Char2), synhronise(Char2, Char3)), Char1 \= Char2, Char1 \= Char3, Char2 \= Char3;
  (synhronise(Char1, Char3), synhronise(Char2, Char3)), Char1 \= Char2, Char1 \= Char3, Char2 \= Char3.

% ?- element(Char, ice), \+ fraction(Char, victoria_Housekeeping_Co). Запрос на персонажей с определенной стихией, которые не принадлежат фракции victoria_Housekeeping_Co
% ?- good_support(ellen, Support). Запрос на поиск саппорта под Эллен
% ?- synchronized_team(jane, Char2, Char3). Поиск синхронизироанной команды где будет Джейн
% ?- role(Char1, attack), role(Char2, stun), good_support(Char1, Char3), synchronized_team(Char1, Char2, Char3). поиску синхронизированной команды, где первый персонаж роли attack, второй роли stun, а 3 - саппорт, который подходит под первого персонажа
