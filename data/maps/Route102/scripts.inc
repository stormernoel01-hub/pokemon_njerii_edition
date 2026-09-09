Route102_MapScripts::
	.byte 0

Route102_EventScript_LittleBoy::
	msgbox Route102_Text_ImNotVeryTall, MSGBOX_NPC
	end

Route102_EventScript_RouteSignOldale::
	msgbox Route102_Text_RouteSignOldale, MSGBOX_SIGN
	end

Route102_EventScript_RouteSignPetalburg::
	msgbox Route102_Text_RouteSignPetalburg, MSGBOX_SIGN
	end

Route102_EventScript_Boy::
	msgbox Route102_Text_CatchWholeBunchOfPokemon, MSGBOX_NPC
	end

Route102_EventScript_Calvin::
	trainerbattle_double TRAINER_CALVIN_1, Route102_Text_CalvinIntro, Route102_Text_CalvinDefeat, Route102_Text_CalvinNotEnoughMons
	msgbox Route102_Text_CalvinAfter, MSGBOX_AUTOCLOSE
	end

Route102_EventScript_CalvinRegisterMatchCallAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	goto_if_set FLAG_HAS_MATCH_CALL, Route102_EventScript_CalvinRegisterMatchCall
	release
	end

Route102_EventScript_CalvinRegisterMatchCall::
	msgbox Route102_Text_CalvinRegisterShort, MSGBOX_DEFAULT
	register_matchcall TRAINER_CALVIN_1
	release
	end

Route102_EventScript_CalvinTryRegister::
	goto_if_set FLAG_HAS_MATCH_CALL, Route102_EventScript_CalvinRegister
	msgbox Route102_Text_CalvinPostBattle, MSGBOX_DEFAULT
	release
	end

Route102_EventScript_CalvinRegister::
	msgbox Route102_Text_CalvinRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_CALVIN_1
	release
	end

Route102_EventScript_CalvinRematch::
	trainerbattle_rematch TRAINER_CALVIN_1, Route102_Text_CalvinRematchIntro, Route102_Text_CalvinRematchDefeated
	msgbox Route102_Text_CalvinRematchPostBattle, MSGBOX_AUTOCLOSE
	end

Route102_EventScript_Rick::
	trainerbattle_double TRAINER_RICK, Route102_Text_RickIntro, Route102_Text_RickDefeat, Route102_Text_RickNotEnoughMons
	msgbox Route102_Text_RickAfter, MSGBOX_AUTOCLOSE
	end

Route102_EventScript_Tiana::
	trainerbattle_double TRAINER_TIANA, Route102_Text_TianaIntro, Route102_Text_TianaDefeat, Route102_Text_TianaNotEnoughMons
	msgbox Route102_Text_TianaAfter, MSGBOX_AUTOCLOSE
	end

Route102_EventScript_Allen::
	trainerbattle_double TRAINER_ALLEN, Route102_Text_AllenIntro, Route102_Text_AllenDefeat, Route102_Text_AllenNotEnoughMons
	msgbox Route102_Text_AllenAfter, MSGBOX_AUTOCLOSE
	end

Route102_Text_WatchMeCatchPokemon:
	.string "HEIKO: {PLAYER}…\n"
	.string "POKéMON verstecken sich in hohem Gras\l"
	.string "wie diesem hier, oder?\p"
	.string "Bitte bleib hier und schau, ob ich sie\n"
	.string "auch richtig fange.\p"
	.string "… Whoa!$"

Route102_Text_WallyIDidIt:
	.string "HEIKO: Ich habe es geschafft… Es\n"
	.string "gehört mir… Mein POKéMON!!!$"

Route102_Text_LetsGoBack:
	.string "{PLAYER}, danke schön!\n"
	.string "Lass uns zurück zur ARENA gehen!$"

Route102_Text_ImNotVeryTall:
	.string "Mis lieblings Pokemon\n"
	.string "isch GIRAFARIG.\p"
	.string "Mer schriibt sin Name\n"
	.string "Rückwärts genau\p"
	.string "so wie Vorwärts$"

Route102_Text_CatchWholeBunchOfPokemon:
	.string "Ich han mis ganze Geld für\n"
	.string "Pokebäll usgeh!$"

Route102_Text_RouteSignOldale:
	.string "ROUTE 102\n"
	.string "{RIGHT_ARROW} BASI$"

Route102_Text_RouteSignPetalburg:
	.string "ROUTE 102\n"
	.string "{LEFT_ARROW} GRASWINKEL TOWN$"
