#!/usr/bin/env python3
"""Hand-translated German for the battle_message.c strings whose English text
diverged from WalterWoshid (expansion uses newer wording / combined placeholders).
Keyed by label -> new body (the text between _( and ), WITH surrounding quotes)."""
import re, pathlib

M = {
 'gText_PkmnShroudedInMist': r'"Das Team von {B_ATK_TEAM1} wird\nin WEISSNEBEL gehüllt!"',
 'gText_PkmnGettingPumped': r'"{B_DEF_NAME_WITH_PREFIX} steigert\nseine Kampfeslust!"',
 'gText_PkmnsXPreventsSwitching': r'"{B_LAST_ABILITY} von {B_BUFF1}\nverhindert den Wechsel!\p"',
 'gText_DefendersStatRose': r'"{B_BUFF1} von {B_DEF_NAME_WITH_PREFIX}\nsteigt{B_BUFF2}!"',
 'sText_GotAwaySafely': r'"{PLAY_SE SE_FLEE}Flucht geglückt!\p"',
 'sText_PlayerDefeatedLinkTrainer': r'"Du besiegst {B_LINK_OPPONENT1_NAME}!"',
 'sText_TwoLinkTrainersDefeated': r'"Du besiegst {B_LINK_OPPONENT1_NAME}\nund {B_LINK_OPPONENT2_NAME}!"',
 'sText_PlayerLostAgainstLinkTrainer': r'"Du verlierst gegen\n{B_LINK_OPPONENT1_NAME}!"',
 'sText_PlayerLostToTwo': r'"Du verlierst gegen {B_LINK_OPPONENT1_NAME}\nund {B_LINK_OPPONENT2_NAME}!"',
 'sText_PlayerBattledToDrawLinkTrainer': r'"Unentschieden gegen\n{B_LINK_OPPONENT1_NAME}!"',
 'sText_PlayerBattledToDrawVsTwo': r'"Unentschieden gegen {B_LINK_OPPONENT1_NAME}\nund {B_LINK_OPPONENT2_NAME}!"',
 'sText_TwoWildFled': r'"{PLAY_SE SE_FLEE}{B_LINK_OPPONENT1_NAME} und\n{B_LINK_OPPONENT2_NAME} fliehen!"',
 'sText_PlayerDefeatedLinkTrainerTrainer1': r'"Du besiegst\n{B_TRAINER1_NAME_WITH_CLASS}!\p"',
 'sText_WildPkmnAppeared': r'"Ein wildes {B_OPPONENT_MON1_NAME}\nerscheint!\p"',
 'sText_LegendaryPkmnAppeared': r'"Ein wildes {B_OPPONENT_MON1_NAME}\nerscheint!\p"',
 'sText_WildPkmnAppearedPause': r'"Ein wildes {B_OPPONENT_MON1_NAME}\nerscheint!{PAUSE 127}"',
 'sText_TwoWildPkmnAppeared': r'"Ein wildes {B_OPPONENT_MON1_NAME} und ein\nwildes {B_OPPONENT_MON2_NAME} erscheinen!\p"',
 'sText_Trainer1WantsToBattle': r'"Du wirst von {B_TRAINER1_NAME_WITH_CLASS}\nherausgefordert!\p"',
 'sText_LinkTrainerWantsToBattle': r'"Du wirst von {B_LINK_OPPONENT1_NAME}\nherausgefordert!"',
 'sText_TwoLinkTrainersWantToBattle': r'"{B_LINK_OPPONENT1_NAME} und {B_LINK_OPPONENT2_NAME}\nfordern dich heraus!"',
 'sText_Trainer1SentOutPkmn': r'"{B_TRAINER1_NAME_WITH_CLASS} schickt\n{B_OPPONENT_MON1_NAME} in den Kampf!"',
 'sText_Trainer1SentOutTwoPkmn': r'"{B_TRAINER1_NAME_WITH_CLASS} schickt\n{B_OPPONENT_MON1_NAME} und {B_OPPONENT_MON2_NAME}!"',
 'sText_Trainer1SentOutPkmn2': r'"{B_TRAINER1_NAME_WITH_CLASS} schickt\n{B_BUFF1} in den Kampf!"',
 'sText_LinkTrainerSentOutPkmn': r'"{B_LINK_OPPONENT1_NAME} schickt\n{B_BUFF1} in den Kampf!"',
 'sText_LinkTrainerSentOutTwoPkmn': r'"{B_LINK_OPPONENT1_NAME} schickt {B_OPPONENT_MON1_NAME}\nund {B_OPPONENT_MON2_NAME} in den Kampf!"',
 'sText_LinkTrainerSentOutPkmn2': r'"{B_LINK_OPPONENT1_NAME} schickt\n{B_LINK_OPPONENT_MON2_NAME} in den Kampf!"',
 'sText_LinkTrainerMultiSentOutPkmn': r'"{B_LINK_SCR_TRAINER_NAME} schickt\n{B_BUFF1} in den Kampf!"',
 'sText_GoTwoPkmn': r'"Los, {B_PLAYER_MON1_NAME} und\n{B_PLAYER_MON2_NAME}!"',
 'sText_DoItPkmn': r'"Auf geht\'s, {B_BUFF1}!"',
 'sText_YourFoesWeakGetEmPkmn': r'"Der Gegner ist schwach!\nGib ihm den Rest, {B_BUFF1}!"',
 'sText_PkmnThatsEnough': r'"{B_BUFF1}, das reicht!\nKomm zurück!"',
 'sText_PkmnOkComeBack': r'"O.K., {B_BUFF1}!\nKomm zurück!"',
 'sText_PkmnGoodComeBack': r'"Gut gemacht, {B_BUFF1}!\nKomm zurück!"',
 'sText_Trainer1WithdrewPkmn': r'"{B_TRAINER1_NAME_WITH_CLASS} zieht\n{B_BUFF1} zurück!"',
 'sText_LinkTrainer1WithdrewPkmn': r'"{B_LINK_OPPONENT1_NAME} zieht\n{B_BUFF1} zurück!"',
 'sText_LinkTrainer2WithdrewPkmn': r'"{B_LINK_OPPONENT2_NAME} zieht\n{B_BUFF1} zurück!"',
 'sText_WildPkmnPrefix': r'"Das wilde "',
 'sText_FoePkmnPrefix': r'"Das gegnerische "',
 'sText_FoePkmnPrefix2': r'"Gegnerisches"',
 'sText_FoePkmnPrefix3': r'"Gegnerisches"',
 'sText_FoePkmnPrefix4': r'"Gegnerisches"',
 'sText_AttackerUsedX': r'"{B_ATK_NAME_WITH_PREFIX} setzt\n{B_BUFF3} ein!"',
 'sText_Attack': r'"Angriff"',
 'sText_Defense': r'"Vert."',
 'sText_Speed': r'"Init."',
 'sText_TwoInGameTrainersDefeated': r'"Du besiegst {B_TRAINER1_NAME_WITH_CLASS}\nund {B_TRAINER2_NAME_WITH_CLASS}!\p"',
 'gText_WhatWillPkmnDo': r'"Was soll\n{B_BUFF1} tun?"',
 'gText_BattleMenu': r'"KAMPF{CLEAR_TO 56}BEUTEL\nPOKéMON{CLEAR_TO 56}FLUCHT"',
 'gText_SafariZoneMenu': r'"Ball{CLEAR_TO 56}{POKEBLOCK}\nAnnähern{CLEAR_TO 56}FLUCHT"',
 'gText_MoveInterfacePpType': r'"{PALETTE 5}{BACKGROUND DYNAMIC_COLOR5}{TEXT_COLORS DYNAMIC_COLOR4 DYNAMIC_COLOR6 DYNAMIC_COLOR5}AP\nTYP/"',
 'gText_WhichMoveToForget4': r'"{PALETTE 5}{BACKGROUND DYNAMIC_COLOR5}{TEXT_COLORS DYNAMIC_COLOR4 DYNAMIC_COLOR6 DYNAMIC_COLOR5}Welche Attacke soll\nvergessen werden?"',
 'gText_BattleYesNoChoice': r'"{PALETTE 5}{BACKGROUND DYNAMIC_COLOR5}{TEXT_COLORS DYNAMIC_COLOR4 DYNAMIC_COLOR6 DYNAMIC_COLOR5}Ja\nNein"',
 'gText_BattleSwitchWhich': r'"{PALETTE 5}{BACKGROUND DYNAMIC_COLOR5}{TEXT_COLORS DYNAMIC_COLOR4 DYNAMIC_COLOR6 DYNAMIC_COLOR5}Wen aus-\ntauschen?"',
 'gText_SafariBalls': r'"Safari-Bälle"',
 'gText_SafariBallLeft': r'"Übrig: $"',
 'gText_BadEgg': r'"Schlechtes Ei"',
 'gText_Win': r'"{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}Sieg"',
 'gText_Loss': r'"{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}Nied."',
 'gText_Draw': r'"{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}Unent."',
 'sText_TwoTrainersSentPkmn': r'"{B_TRAINER1_NAME_WITH_CLASS} schickt {B_OPPONENT_MON1_NAME}!\p{B_TRAINER2_NAME_WITH_CLASS} schickt {B_OPPONENT_MON2_NAME}!"',
 'sText_Trainer2SentOutPkmn': r'"{B_TRAINER2_NAME_WITH_CLASS} schickt\n{B_BUFF1} in den Kampf!"',
 'sText_TwoTrainersWantToBattle': r'"Du wirst von {B_TRAINER1_NAME_WITH_CLASS}\nund {B_TRAINER2_NAME_WITH_CLASS} herausgefordert!\p"',
 'sText_InGamePartnerSentOutZGoN': r'"{B_PARTNER_NAME_WITH_CLASS} schickt {B_PLAYER_MON2_NAME}!\nLos, {B_PLAYER_MON1_NAME}!"',
 'sText_Trainer1Fled': r'"{PLAY_SE SE_FLEE}{B_TRAINER1_NAME_WITH_CLASS}\nflieht!"',
 'sText_PlayerLostAgainstTrainer1': r'"Du verlierst gegen\n{B_TRAINER1_NAME_WITH_CLASS}!"',
 'sText_PlayerBattledToDrawTrainer1': r'"Unentschieden gegen\n{B_TRAINER1_NAME_WITH_CLASS}!"',
 'gText_RecordBattleToPass': r'"Möchtest du diesen Kampf auf\ndeinem FRONTIER-PASS aufzeichnen?"',
 'gText_BattleRecordedOnPass': r'"Das Kampfergebnis von {B_PLAYER_NAME}\nwurde auf dem FRONTIER-PASS notiert."',
 'sText_LinkTrainerWantsToBattlePause': r'"Du wirst von {B_LINK_OPPONENT1_NAME}\nherausgefordert!\p"',
 'sText_TwoLinkTrainersWantToBattlePause': r'"{B_LINK_OPPONENT1_NAME} und {B_LINK_OPPONENT2_NAME}\nfordern dich heraus!\p"',
}

p = pathlib.Path("/home/denotzgii/pokeemerald-expansion/src/battle_message.c")
txt = p.read_text()
DECL = re.compile(r'(\b(?:static\s+)?(?:ALIGNED\(\d+\)\s+)?const u8 (?P<label>[A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*=\s*)_\(')
def body_span(t, start):
    i=start; depth=1; ins=False; esc=False
    while i<len(t) and depth>0:
        c=t[i]
        if ins:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c=='(': depth+=1
            elif c==')': depth-=1
        i+=1
    return start, i-1
edits=[]
for m in DECL.finditer(txt):
    lbl=m.group('label')
    if lbl in M:
        bs,be = body_span(txt, m.end())
        edits.append((bs,be,M[lbl],lbl))
done=set()
for bs,be,new,lbl in sorted(edits, reverse=True):
    txt = txt[:bs] + new + txt[be:]
    done.add(lbl)
p.write_text(txt)
missing = set(M) - done
print(f"applied {len(done)}/{len(M)}")
if missing: print("NOT FOUND:", missing)
