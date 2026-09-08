MauvilleCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MauvilleCity_Gym_OnLoad
	.byte 0

MauvilleCity_Gym_OnLoad:
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_DeactivatePuzzle
	switch VAR_MAUVILLE_GYM_STATE
	case 0, MauvilleCity_Gym_EventScript_UpdateBarriers
	case 1, MauvilleCity_Gym_EventScript_Switch1Pressed
	case 2, MauvilleCity_Gym_EventScript_Switch2Pressed
	case 3, MauvilleCity_Gym_EventScript_Switch3Pressed
	case 4, MauvilleCity_Gym_EventScript_Switch4Pressed
	end

MauvilleCity_Gym_EventScript_UpdateBarriers::
	goto_if_set FLAG_MAUVILLE_GYM_BARRIERS_STATE, MauvilleCity_Gym_EventScript_SetAltBarriers
	end

MauvilleCity_Gym_EventScript_SetAltBarriers::
	setmetatile 3, 11, METATILE_MauvilleGym_RedBeamV1_On, TRUE
	setmetatile 3, 12, METATILE_MauvilleGym_RedBeamV2_On, TRUE
	setmetatile 3, 13, METATILE_MauvilleGym_PoleTop_On, TRUE
	setmetatile 4, 10, METATILE_MauvilleGym_RedBeamH1_On, FALSE
	setmetatile 5, 10, METATILE_MauvilleGym_RedBeamH2_On, FALSE
	setmetatile 4, 11, METATILE_MauvilleGym_RedBeamH3_On, TRUE
	setmetatile 5, 11, METATILE_MauvilleGym_RedBeamH4_On, TRUE
	setmetatile 7, 10, METATILE_MauvilleGym_RedBeamH1_On, FALSE
	setmetatile 8, 10, METATILE_MauvilleGym_RedBeamH2_On, FALSE
	setmetatile 7, 11, METATILE_MauvilleGym_RedBeamH3_On, TRUE
	setmetatile 8, 11, METATILE_MauvilleGym_RedBeamH4_On, TRUE
	setmetatile 4, 13, METATILE_MauvilleGym_GreenBeamH1_Off, FALSE
	setmetatile 5, 13, METATILE_MauvilleGym_GreenBeamH2_Off, FALSE
	setmetatile 4, 14, METATILE_MauvilleGym_GreenBeamH3_Off, FALSE
	setmetatile 5, 14, METATILE_MauvilleGym_GreenBeamH4_Off, FALSE
	setmetatile 1, 10, METATILE_MauvilleGym_GreenBeamH1_Off, FALSE
	setmetatile 2, 10, METATILE_MauvilleGym_GreenBeamH2_Off, FALSE
	setmetatile 1, 11, METATILE_MauvilleGym_GreenBeamH3_Off, FALSE
	setmetatile 2, 11, METATILE_MauvilleGym_GreenBeamH4_Off, FALSE
	setmetatile 6, 8, METATILE_MauvilleGym_PoleBottom_On, TRUE
	setmetatile 6, 9, METATILE_MauvilleGym_FloorTile, FALSE
	setmetatile 6, 10, METATILE_MauvilleGym_PoleTop_Off, FALSE
	setmetatile 4, 6, METATILE_MauvilleGym_GreenBeamH1_Off, FALSE
	setmetatile 5, 6, METATILE_MauvilleGym_GreenBeamH2_Off, FALSE
	setmetatile 4, 7, METATILE_MauvilleGym_GreenBeamH3_Off, FALSE
	setmetatile 5, 7, METATILE_MauvilleGym_GreenBeamH4_Off, FALSE
	end

MauvilleCity_Gym_EventScript_Switch1Pressed::
	setvar VAR_0x8004, 0
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_Switch2Pressed::
	setvar VAR_0x8004, 1
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_Switch3Pressed::
	setvar VAR_0x8004, 2
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_Switch4Pressed::
	setvar VAR_0x8004, 3
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_DeactivatePuzzle::
	special MauvilleGymDeactivatePuzzle
	end

MauvilleCity_Gym_EventScript_Wattson::
	lock
	faceplayer
	goto_if_set FLAG_BADGE02_GET, MauvilleCity_Gym_EventScript_WattsonPostBattle
	trainerbattle_double TRAINER_WATTSON_1, MauvilleCity_Gym_Text_WattsonIntro, MauvilleCity_Gym_Text_WattsonDefeat, MauvilleCity_Gym_Text_WattsonNotEnoughMons, MauvilleCity_Gym_EventScript_WattsonDefeated
	release
	end

MauvilleCity_Gym_EventScript_WattsonPostBattle::
	msgbox MauvilleCity_Gym_Text_WattsonGoForthAndEndeavor, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_WattsonDefeated::
	message MauvilleCity_Gym_Text_ReceivedDynamoBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_DEFEATED_MAUVILLE_GYM
	setflag FLAG_BADGE02_GET
	special MauvilleGymDeactivatePuzzle
	special DrawWholeMapView
	msgbox MauvilleCity_Gym_Text_WattsonGoForthAndEndeavor, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_GiveShockWave2::
	giveitem ITEM_TM_SHOCK_WAVE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox MauvilleCity_Gym_Text_ExplainShockWave, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_SHOCK_WAVE
	release
	end

MauvilleCity_Gym_EventScript_GiveShockWave::
	giveitem ITEM_TM_SHOCK_WAVE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox MauvilleCity_Gym_Text_ExplainShockWave, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_SHOCK_WAVE
	return

MauvilleCity_Gym_EventScript_CompletedNewMauville::
	msgbox MauvilleCity_Gym_Text_WattsonGoForthAndEndeavor, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_WattsonRematch::
	trainerbattle_rematch_double TRAINER_WATTSON_1, MauvilleCity_Gym_Text_WattsonPreRematch, MauvilleCity_Gym_Text_WattsonRematchDefeat, MauvilleCity_Gym_Text_WattsonRematchNeedTwoMons
	msgbox MauvilleCity_Gym_Text_WattsonPostRematch, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Switch1::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 1, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 1
	setvar VAR_0x8004, 0
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_Switch2::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 2, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 2
	setvar VAR_0x8004, 1
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_Switch3::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 3, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 3
	setvar VAR_0x8004, 2
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_Switch4::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 4, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 4
	setvar VAR_0x8004, 3
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_PressFloorSwitch::
	special MauvilleGymSetDefaultBarriers
	special MauvilleGymPressSwitch
	special DrawWholeMapView
	playse SE_UNLOCK
	goto_if_set FLAG_MAUVILLE_GYM_BARRIERS_STATE, MauvilleCity_Gym_EventScript_ClearBarriersAltState
	goto_if_unset FLAG_MAUVILLE_GYM_BARRIERS_STATE, MauvilleCity_Gym_EventScript_SetBarriersAltState
	releaseall
	end

MauvilleCity_Gym_EventScript_SwitchDoNothing::
	releaseall
	end

MauvilleCity_Gym_EventScript_SetBarriersAltState::
	setflag FLAG_MAUVILLE_GYM_BARRIERS_STATE
	releaseall
	end

MauvilleCity_Gym_EventScript_ClearBarriersAltState::
	clearflag FLAG_MAUVILLE_GYM_BARRIERS_STATE
	releaseall
	end

MauvilleCity_Gym_EventScript_Kirk::
	trainerbattle_double TRAINER_KIRK, MauvilleCity_Gym_Text_KirkIntro, MauvilleCity_Gym_Text_KirkDefeat, MauvilleCity_Gym_Text_KirkNotEnoughMons
	msgbox MauvilleCity_Gym_Text_KirkPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Shawn::
	trainerbattle_double TRAINER_SHAWN, MauvilleCity_Gym_Text_ShawnIntro, MauvilleCity_Gym_Text_ShawnDefeat, MauvilleCity_Gym_Text_ShawnNotEnoughMons
	msgbox MauvilleCity_Gym_Text_ShawnPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Ben::
	trainerbattle_double TRAINER_BEN, MauvilleCity_Gym_Text_BenIntro, MauvilleCity_Gym_Text_BenDefeat, MauvilleCity_Gym_Text_BenNotEnoughMons
	msgbox MauvilleCity_Gym_Text_BenPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Vivian::
	trainerbattle_double TRAINER_VIVIAN, MauvilleCity_Gym_Text_VivianIntro, MauvilleCity_Gym_Text_VivianDefeat, MauvilleCity_Gym_Text_VivianNotEnoughMons
	msgbox MauvilleCity_Gym_Text_VivianPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Angelo::
	trainerbattle_double TRAINER_ANGELO, MauvilleCity_Gym_Text_AngeloIntro, MauvilleCity_Gym_Text_AngeloDefeat, MauvilleCity_Gym_Text_AngeloNotEnoughMons
	msgbox MauvilleCity_Gym_Text_AngeloPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_GymGuidePostVictory
	msgbox MauvilleCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_GymGuidePostVictory::
	msgbox MauvilleCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE03_GET, MauvilleCity_Gym_EventScript_GymStatueCertified
	goto MauvilleCity_Gym_EventScript_GymStatue
	end

MauvilleCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE03_GET, MauvilleCity_Gym_EventScript_GymStatueCertified
	goto MauvilleCity_Gym_EventScript_GymStatue
	end

MauvilleCity_Gym_EventScript_GymStatueCertified::
	msgbox MauvilleCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

MauvilleCity_Gym_EventScript_GymStatue::
	msgbox MauvilleCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

MauvilleCity_Gym_Text_GymGuideAdvice:
	.string "Hey, how's it going, CHAMPION-\n"
	.string "bound {PLAYER}?\p"
	.string "WATTSON, the LEADER of MAUVILLE\n"
	.string "GYM, uses ELECTRIC-type POKéMON.\p"
	.string "If you challenge him with WATER-type\n"
	.string "POKéMON, he'll zap them! Bzzt!\p"
	.string "And, he's put in switch-controlled\n"
	.string "doors all over his GYM! Eccentric!\p"
	.string "Hey, go for it!$"

MauvilleCity_Gym_Text_GymGuidePostVictory:
	.string "Whoa, you're electrifying!\n"
	.string "You've powered the door open!$"

MauvilleCity_Gym_Text_KirkIntro:
	.string "Ich schwör, warum will\n"
	.string "Nati nüüt vo mir?$"

MauvilleCity_Gym_Text_KirkDefeat:
	.string "Why u so funny?$"

MauvilleCity_Gym_Text_KirkPostBattle:
	.string "Das isch truurig bro.$"

MauvilleCity_Gym_Text_KirkNotEnoughMons:
	.string "Du bruchsch mindestens zwei\n"
	.string "Pokemon für en Doppelkampf.$"

MauvilleCity_Gym_Text_ShawnIntro:
	.string "Min Brüeder schafft ide\n"
	.string "Coop Tankstell.$"

MauvilleCity_Gym_Text_ShawnDefeat:
	.string "Jebemimamu$"

MauvilleCity_Gym_Text_ShawnPostBattle:
	.string "Lauf wiiter Kolleg...$"

MauvilleCity_Gym_Text_ShawnNotEnoughMons:
	.string "Du bruchsch mindestens zwei\n"
	.string "Pokemon für en Doppelkampf.$"

MauvilleCity_Gym_Text_BenIntro:
	.string "Ich bin Waluigi Fan!$"

MauvilleCity_Gym_Text_BenDefeat:
	.string "WAAAAAAA!!!$"

MauvilleCity_Gym_Text_BenPostBattle:
	.string "Ja denn halt...\n"
	.string "de AJ schlahsch defür\l"
	.string "niemals.$"

MauvilleCity_Gym_Text_BenNotEnoughMons:
	.string "Du bruchsch mindestens zwei\n"
	.string "Pokemon für en Doppelkampf.$"

MauvilleCity_Gym_Text_VivianIntro:
	.string "Ich wär vill besser\n"
	.string "g eignet als Arenaleiterin,\l"
	.string "als de AJ.\p"
	.string "Ich bewies der das jetzt!$"

MauvilleCity_Gym_Text_VivianDefeat:
	.string "Ach...$"

MauvilleCity_Gym_Text_VivianPostBattle:
	.string "Ich will nöd zuegeh,\n"
	.string "dass du mich besiegt hesch.$"

MauvilleCity_Gym_Text_VivianNotEnoughMons:
	.string "Du bruchsch mindestens zwei\n"
	.string "Pokemon für en Doppelkampf.$"


MauvilleCity_Gym_Text_AngeloIntro:
	.string "Ich muss nacher ide Snus\n"
	.string "go ackere, also chum\l"
	.string "machemer schnell de Fight.$"

MauvilleCity_Gym_Text_AngeloDefeat:
	.string "Kächi!$"

MauvilleCity_Gym_Text_AngeloPostBattle:
	.string "Negscht mal, wenn du en\n"
	.string "Burger bi eus bstellsch,\l"
	.string "lahn ich din Patty schnell\l"
	.string "überem dreckige Fuessbode\l"
	.string "los.$"

MauvilleCity_Gym_Text_AngeloNotEnoughMons:
	.string "Du bruchsch mindestens zwei\n"
	.string "Pokemon für en Doppelkampf.$"

MauvilleCity_Gym_Text_ReceivedDynamoBadge:
	.string "{PLAYER} het de PLASTIK ORDE\n"
	.string "vo AJ erhalte.$"

MauvilleCity_Gym_Text_ExplainDynamoBadgeTakeThis:
	.string "Mit dem PLASTIK ORDE chönd\n"
	.string "Pokemon ZERTRÜMMERER\l"
	.string "usserhalb vom Kampf bruche.\p"
	.string "Usserdem werded dini\n"
	.string "Pokemon chli schneller...\p"
	.string "Glaub ich zumindest.\p"
	.string "Nimm no die TM da.$"

MauvilleCity_Gym_Text_ExplainShockWave:
	.string "Die TM34 enthält\n"
	.string "SCHOCKWELLE.\p"
	.string "Die Attacke trifft immer,\n"
	.string "also eigentlich recht OP.\p"
	.string "Jetzt wirsch dich aber nie\n"
	.string "chönne entscheide, wem du\l"
	.string "sie biibringsch.$"

MauvilleCity_Gym_Text_RegisteredWattson:
	.string "AJ isch im POKENAV\n"
	.string "gspeicheret worde.$"

MauvilleCity_Gym_Text_WattsonIntro:
	.string "Was? Ob ich stoned bin?\n"
	.string "Lächerlich.\p"
	.string "Ich zeig der jetzt wie\n"
	.string "mer richtig kämpft.$"

MauvilleCity_Gym_Text_WattsonDefeat:
	.string "Wow.$"

MauvilleCity_Gym_Text_WattsonPostBattle:
	.string "Okay krass.\p"
	.string "Ich hett nie denkt,\n"
	.string "dass öpper mich mit mine\l"
	.string "OP-Viecher besiegt.\p"
	.string "Janu, jetzt gib ich dir\n"
	.string "no so en Plastik Orde\l"
	.string "und e TM wo du dich nie\l"
	.string "wirsch chönne entscheide,\l"
	.string "wem dass sie biibringsch.$"

MauvilleCity_Gym_Text_WattsonNotEnoughMons:
	.string "Du bruchsch mindestens zwei\n"
	.string "Pokemon für en Doppelkampf.$"

MauvilleCity_Gym_Text_WattsonGoForthAndEndeavor:
	.string "Gang jetzt wiiter...\p"
	.string "Und tue so, als wär das\n"
	.string "alles voll normal gsi.$"

MauvilleCity_Gym_Text_GymStatue:
	.string "DÜBI POKEMON ARENA$"

MauvilleCity_Gym_Text_GymStatueCertified:
	.string "DÜBI POKEMON ARENA\p"
	.string "AJ'S ZERTIFIZIERTI TRAINER:\n"
	.string "{PLAYER}$"

MauvilleCity_Gym_Text_WattsonPreRematch:
	.string "AJ: Ah, du bisch wieder da.\p"
	.string "Du wettsch sicher no mal\n"
	.string "gege mini OP-Viecher\l"
	.string "kämpfe, oder?\p"
	.string "Denn chum.\n"
	.string "Ich bin immer parat.$"

MauvilleCity_Gym_Text_WattsonRematchDefeat:
	.string "Wow...\n"
	.string "Scho wieder.$"

MauvilleCity_Gym_Text_WattsonPostRematch:
	.string "AJ: Okay, ich glaub ich\n"
	.string "muss mini Strategie\l"
	.string "nochmal überdänke.\p"
	.string "Oder mini Viecher eifach\n"
	.string "no meh OP mache.\p"
	.string "Chum später wieder,\n"
	.string "wenn du dich traust.$"

MauvilleCity_Gym_Text_WattsonRematchNeedTwoMons:
	.string "AJ: Ah, du bisch wieder da.\p"
	.string "Aber wart mal...\n"
	.string "Du hesch nur eis Pokemon?\p"
	.string "Das isch en Doppelkampf,\n"
	.string "Kolleg.\p"
	.string "Chum mit mindestens zwei\n"
	.string "Pokemon zrugg.$"

