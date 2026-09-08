GraniteCave_1F_MapScripts::
	.byte 0

GraniteCave_1F_EventScript_Hiker::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_FLASH, GraniteCave_1F_EventScript_ReceivedFlash
	msgbox GraniteCave_1F_Text_GetsDarkAheadHereYouGo, MSGBOX_DEFAULT
	giveitem ITEM_HM_FLASH
	setflag FLAG_RECEIVED_HM_FLASH
	msgbox GraniteCave_1F_Text_ExplainFlash, MSGBOX_DEFAULT
	release
	end

GraniteCave_1F_EventScript_ReceivedFlash::
	msgbox GraniteCave_1F_Text_ExplainFlash, MSGBOX_DEFAULT
	release
	end

GraniteCave_1F_Text_GetsDarkAheadHereYouGo:
	.string "Ouh NJIERI!\p"
	.string "Lueg, ich gib der jetzt\n"
	.string "die VM BLITZ.\p"
	.string "Kei Angst, du bruchsch\n"
	.string "de Scheiss nöd eimal\l"
	.string "innere Höhli da,\p"
	.string "aber villicht wotsch ja\n"
	.string "e Attacke wo d' Genauigkeit\l"
	.string "vo dine Gegner verringered.$"

GraniteCave_1F_Text_ExplainFlash:
	.string "No ein Tipp!\p"
	.string "I dere Höhli gits uere\n"
	.string "vill verschiedeni Viecher.\p"
	.string "Uf jedere Ebeni findsch\n"
	.string "wieder was Neus!\p"
	.string "Pass uf dich uf, NJIERI.$"

