# DS-Musik – verfügbare Tracks (DPPt + HGSS)

366 Tracks aus Diamant/Perl/Platin und HeartGold/SoulSilver.
Das Instrumenten-Fundament ist im ROM; jeder Track hier ist ein Ein-Zeilen-Einbau.

## So wählst du aus
Schick mir einfach eine Liste: **Track-Name → wo er hin soll**, z.B.:
  mus_dp_route209_day        -> Route 101
  mus_hg_national_park       -> Güfu Town
  mus_dp_vs_gym_leader       -> alle Arenakämpfe

Dann mache ich pro Track:  `python3 tools/njieri/add_ds_song.py <name> <MUS_KONSTANTE>`
und setze in Porymap das Feld "Music" der Karte (bzw. im Kampf-Script) auf die neue Konstante.

## Schon eingebaut (zum Testen, R+START -> Sound im Spiel)
- mus_dp_route209_day   = MUS_DP_ROUTE209_DAY
- mus_hg_national_park  = MUS_HG_NATIONAL_PARK
- mus_dp_vs_wild        = MUS_DP_VS_WILD

## Hinweise
- "_day" / "_night": 26 Tracks haben Tag/Nacht-Varianten. Ohne Tag/Nacht-System
  nimm die "_day"-Version.
- mus_rg_* (FireRed/LeafGreen), mus_route101, mus_vs_rayquaza: NICHT in dieser
  Liste – die brauchen andere Instrumentenbänke, extra Aufwand.
- Anhören vorm Auswählen: youtube "Pokemon Platinum <ortsname> music" o.ä.,
  die Namen entsprechen den Original-Spielorten.


# Diamant / Perl / Platin  (190 Tracks)


### Kampf – wild
- `mus_dp_victory_wild`
- `mus_dp_vs_wild`

### Kampf – Trainer
- `mus_dp_encounter_ace_trainer`
- `mus_dp_encounter_artist`
- `mus_dp_encounter_boy`
- `mus_dp_encounter_champion`
- `mus_dp_encounter_cyclist`
- `mus_dp_encounter_elite_four`
- `mus_dp_encounter_galactic`
- `mus_dp_encounter_girl`
- `mus_dp_encounter_hiker`
- `mus_dp_encounter_intense`
- `mus_dp_encounter_lady`
- `mus_dp_encounter_rich`
- `mus_dp_encounter_sailor`
- `mus_dp_encounter_suspicious`
- `mus_dp_encounter_twins`
- `mus_dp_victory_trainer`
- `mus_dp_vs_trainer`

### Kampf – Arenaleiter
- `mus_dp_gym`
- `mus_dp_victory_gym_leader`
- `mus_dp_vs_gym_leader`

### Kampf – Rivale
- `mus_dp_rival`
- `mus_dp_vs_rival`

### Kampf – Champ/Boss
- `mus_dp_legend_appears`
- `mus_dp_victory_champion`
- `mus_dp_victory_elite_four`
- `mus_dp_vs_arceus`
- `mus_dp_vs_champion`
- `mus_dp_vs_dialga_palkia`
- `mus_dp_vs_elite_four`
- `mus_dp_vs_legend`
- `mus_pl_giratina_appears_1`
- `mus_pl_giratina_appears_2`
- `mus_pl_victory_frontier_brain`
- `mus_pl_vs_frontier_brain`
- `mus_pl_vs_giratina`

### Städte & Dörfer
- `mus_dp_canalave_day`
- `mus_dp_canalave_night`
- `mus_dp_eterna_day`
- `mus_dp_eterna_forest`
- `mus_dp_eterna_night`
- `mus_dp_fight_area_day`
- `mus_dp_fight_area_night`
- `mus_dp_floaroma_day`
- `mus_dp_floaroma_night`
- `mus_dp_hearthome_day`
- `mus_dp_hearthome_night`
- `mus_dp_inside_pokemon_league`
- `mus_dp_jubilife_day`
- `mus_dp_jubilife_night`
- `mus_dp_oreburgh_day`
- `mus_dp_oreburgh_gate`
- `mus_dp_oreburgh_mine`
- `mus_dp_oreburgh_night`
- `mus_dp_pokemon_league_day`
- `mus_dp_pokemon_league_night`
- `mus_dp_sandgem_day`
- `mus_dp_sandgem_night`
- `mus_dp_snowpoint_day`
- `mus_dp_snowpoint_night`
- `mus_dp_solaceon_day`
- `mus_dp_solaceon_night`
- `mus_dp_sunyshore_day`
- `mus_dp_sunyshore_night`
- `mus_dp_twinleaf_day`
- `mus_dp_twinleaf_night`
- `mus_dp_veilstone_day`
- `mus_dp_veilstone_night`
- `mus_pl_fight_area_day`
- `mus_pl_twinleaf_music_box`

### Routen
- `mus_dp_route201_day`
- `mus_dp_route201_night`
- `mus_dp_route203_day`
- `mus_dp_route203_night`
- `mus_dp_route205_day`
- `mus_dp_route205_night`
- `mus_dp_route206_day`
- `mus_dp_route206_night`
- `mus_dp_route209_day`
- `mus_dp_route209_night`
- `mus_dp_route210_day`
- `mus_dp_route210_night`
- `mus_dp_route216_day`
- `mus_dp_route216_night`
- `mus_dp_route225_day`
- `mus_dp_route225_night`
- `mus_dp_route228_day`
- `mus_dp_route228_night`

### Höhlen & Dungeons
- `mus_dp_b_tower`
- `mus_dp_galactic_hq`
- `mus_dp_galactic_hq_basement`
- `mus_dp_lake`
- `mus_dp_lake_caverns`
- `mus_dp_lake_event`
- `mus_dp_mt_coronet`
- `mus_dp_spear_pillar`
- `mus_dp_valor_lakefront_day`
- `mus_dp_valor_lakefront_night`
- `mus_dp_victory_galactic`
- `mus_dp_vs_galactic`
- `mus_dp_vs_galactic_boss`
- `mus_dp_vs_galactic_commander`

### Innenräume & Gebäude
- `mus_dp_contest`
- `mus_dp_contest_dress_up`
- `mus_dp_contest_lobby`
- `mus_dp_contest_results`
- `mus_dp_contest_winner`
- `mus_dp_game_corner`
- `mus_dp_poke_center_day`
- `mus_dp_poke_center_night`
- `mus_dp_poke_mart`
- `mus_dp_rowan_lab`
- `mus_pl_contest_beauty`
- `mus_pl_contest_cool`
- `mus_pl_contest_cute`
- `mus_pl_contest_smart`
- `mus_pl_contest_tough`

### Events & Jingles
- `mus_dp_caught_intro`
- `mus_dp_credits`
- `mus_dp_evolution`
- `mus_dp_evolved`
- `mus_dp_heal`
- `mus_dp_intro`
- `mus_dp_level_up`
- `mus_dp_obtain_accessory`
- `mus_dp_obtain_badge`
- `mus_dp_obtain_berry`
- `mus_dp_obtain_item`
- `mus_dp_obtain_key_item`
- `mus_dp_obtain_tmhm`
- `mus_dp_title`
- `mus_dp_tv_broadcast`
- `mus_dp_tv_end`
- `mus_dp_tv_station`
- `mus_dp_victory_road`
- `mus_pl_intro`
- `mus_pl_looker`
- `mus_pl_obtain_arcade_points`
- `mus_pl_obtain_b_points`
- `mus_pl_obtain_castle_points`
- `mus_pl_spin_trade`
- `mus_pl_title`
- `mus_pl_tv_broadcast`
- `mus_pl_tv_end`

### Natur & Ambiente
- `mus_dp_azure_flute`
- `mus_dp_cycling`
- `mus_dp_surf`
- `mus_dp_underground`
- `mus_pl_global_terminal`

### Sonstige
- `mus_dp_amity_square`
- `mus_dp_catastrophe`
- `mus_dp_dance_difficult`
- `mus_dp_dance_easy`
- `mus_dp_dawn`
- `mus_dp_dex_rating`
- `mus_dp_flag_captured`
- `mus_dp_follow_me`
- `mus_dp_great_marsh`
- `mus_dp_gts`
- `mus_dp_hall_of_fame`
- `mus_dp_hall_of_fame_room`
- `mus_dp_hall_of_origin`
- `mus_dp_lets_go_together`
- `mus_dp_lucas`
- `mus_dp_move_deleted`
- `mus_dp_mystery_gift`
- `mus_dp_old_chateau`
- `mus_dp_poffins`
- `mus_dp_poke_radar`
- `mus_dp_poketch`
- `mus_dp_rowan`
- `mus_dp_slots_jackpot`
- `mus_dp_slots_unused`
- `mus_dp_slots_win`
- `mus_dp_stark_mountain`
- `mus_dp_vs_uxie_mesprit_azelf`
- `mus_dp_wfc`
- `mus_pl_b_arcade`
- `mus_pl_b_castle`
- `mus_pl_b_factory`
- `mus_pl_b_hall`
- `mus_pl_distortion_world`
- `mus_pl_lilycove_bossa_nova`
- `mus_pl_mystery_gift`
- `mus_pl_vs_regi`
- `mus_pl_wifi_minigames`
- `mus_pl_wifi_parade`
- `mus_pl_wifi_plaza`
- `mus_pl_win_minigame`


# HeartGold / SoulSilver  (176 Tracks)


### Kampf – wild
- `mus_hg_victory_wild`
- `mus_hg_vs_wild`
- `mus_hg_vs_wild_kanto`

### Kampf – Trainer
- `mus_hg_encounter_boy_1`
- `mus_hg_encounter_boy_2`
- `mus_hg_encounter_girl_1`
- `mus_hg_encounter_girl_2`
- `mus_hg_encounter_kimono_girl`
- `mus_hg_encounter_rival`
- `mus_hg_encounter_rocket`
- `mus_hg_encounter_sage`
- `mus_hg_encounter_suspicious_1`
- `mus_hg_encounter_suspicious_2`
- `mus_hg_radio_trainer`
- `mus_hg_victory_trainer`
- `mus_hg_vs_trainer`
- `mus_hg_vs_trainer_kanto`

### Kampf – Arenaleiter
- `mus_hg_gym`
- `mus_hg_victory_gym_leader`
- `mus_hg_vs_gym_leader`
- `mus_hg_vs_gym_leader_kanto`

### Kampf – Rivale
- `mus_hg_rival_exit`
- `mus_hg_vs_rival`

### Kampf – Champ/Boss
- `mus_hg_ho_oh_appears`
- `mus_hg_lugia_appears`
- `mus_hg_route42`
- `mus_hg_route47`
- `mus_hg_victory_frontier_brain`
- `mus_hg_vs_arceus`
- `mus_hg_vs_champion`
- `mus_hg_vs_frontier_brain`
- `mus_hg_vs_ho_oh`
- `mus_hg_vs_kyogre_groudon`
- `mus_hg_vs_lugia`

### Städte & Dörfer
- `mus_hg_azalea`
- `mus_hg_celadon`
- `mus_hg_cerulean`
- `mus_hg_cherrygrove`
- `mus_hg_cianwood`
- `mus_hg_cinnabar`
- `mus_hg_ecruteak`
- `mus_hg_goldenrod`
- `mus_hg_lavender`
- `mus_hg_pallet`
- `mus_hg_pewter`
- `mus_hg_pokemon_league`
- `mus_hg_vermilion`
- `mus_hg_violet`
- `mus_hg_viridian_forest`

### Routen
- `mus_hg_radio_route101`
- `mus_hg_radio_route201`
- `mus_hg_route1`
- `mus_hg_route11`
- `mus_hg_route24`
- `mus_hg_route26`
- `mus_hg_route29`
- `mus_hg_route3`
- `mus_hg_route30`
- `mus_hg_route34`
- `mus_hg_route38`

### Höhlen & Dungeons
- `mus_hg_b_tower`
- `mus_hg_b_tower_reception`
- `mus_hg_bell_tower`
- `mus_hg_burned_tower`
- `mus_hg_ice_path`
- `mus_hg_mt_moon_square`
- `mus_hg_radio_rocket`
- `mus_hg_rock_tunnel`
- `mus_hg_rocket_takeover`
- `mus_hg_ruins_of_alph`
- `mus_hg_sinjou_ruins`
- `mus_hg_sprout_tower`
- `mus_hg_team_rocket_hq`
- `mus_hg_union_cave`
- `mus_hg_vs_rocket`

### Innenräume & Gebäude
- `mus_hg_bug_catching_contest`
- `mus_hg_bug_contest_1st_place`
- `mus_hg_bug_contest_2nd_place`
- `mus_hg_bug_contest_3rd_place`
- `mus_hg_bug_contest_prep`
- `mus_hg_elm_lab`
- `mus_hg_game_corner`
- `mus_hg_game_corner_win`
- `mus_hg_poke_center`
- `mus_hg_poke_mart`
- `mus_hg_radio_lullaby`
- `mus_hg_safari_zone`
- `mus_hg_safari_zone_gate`

### Events & Jingles
- `mus_hg_caught`
- `mus_hg_credits`
- `mus_hg_evolution`
- `mus_hg_evolution_no_intro`
- `mus_hg_evolved`
- `mus_hg_heal`
- `mus_hg_intro`
- `mus_hg_level_up`
- `mus_hg_oak`
- `mus_hg_obtain_accessory`
- `mus_hg_obtain_arcade_points`
- `mus_hg_obtain_b_points`
- `mus_hg_obtain_badge`
- `mus_hg_obtain_berry`
- `mus_hg_obtain_castle_points`
- `mus_hg_obtain_egg`
- `mus_hg_obtain_item`
- `mus_hg_obtain_key_item`
- `mus_hg_obtain_tmhm`
- `mus_hg_pokeathlon_event`
- `mus_hg_radio_jingle`
- `mus_hg_radio_oak`
- `mus_hg_spin_trade`
- `mus_hg_title`
- `mus_hg_victory_road`

### Natur & Ambiente
- `mus_hg_cycling`
- `mus_hg_global_terminal`
- `mus_hg_national_park`
- `mus_hg_pokeathlon_1st_place`
- `mus_hg_pokeathlon_before`
- `mus_hg_pokeathlon_end`
- `mus_hg_pokeathlon_finals`
- `mus_hg_pokeathlon_lobby`
- `mus_hg_pokeathlon_ready`
- `mus_hg_pokeathlon_results`
- `mus_hg_pokeathlon_start`
- `mus_hg_pokeathlon_winner`
- `mus_hg_pokewalker`
- `mus_hg_radio_poke_flute`
- `mus_hg_ss_aqua`
- `mus_hg_surf`

### Sonstige
- `mus_hg_b_arcade`
- `mus_hg_b_castle`
- `mus_hg_b_factory`
- `mus_hg_b_hall`
- `mus_hg_card_flip`
- `mus_hg_card_flip_game_over`
- `mus_hg_clair`
- `mus_hg_dance_theater`
- `mus_hg_dex_rating_1`
- `mus_hg_dex_rating_2`
- `mus_hg_dex_rating_3`
- `mus_hg_dex_rating_4`
- `mus_hg_dex_rating_5`
- `mus_hg_dex_rating_6`
- `mus_hg_dragons_den`
- `mus_hg_end`
- `mus_hg_ethan`
- `mus_hg_eusine`
- `mus_hg_follow_me_1`
- `mus_hg_follow_me_2`
- `mus_hg_gts`
- `mus_hg_hall_of_fame`
- `mus_hg_kimono_girl`
- `mus_hg_kimono_girl_dance`
- `mus_hg_lets_go_together`
- `mus_hg_lighthouse`
- `mus_hg_lyra`
- `mus_hg_magnet_train`
- `mus_hg_move_deleted`
- `mus_hg_mystery_gift`
- `mus_hg_new_bark`
- `mus_hg_new_game`
- `mus_hg_pokegear_registered`
- `mus_hg_radio_buena`
- `mus_hg_radio_march`
- `mus_hg_radio_unown`
- `mus_hg_radio_variety`
- `mus_hg_receive_pokemon`
- `mus_hg_spiky_eared_pichu`
- `mus_hg_vs_entei`
- `mus_hg_vs_raikou`
- `mus_hg_vs_suicune`
- `mus_hg_wfc`
- `mus_hg_wifi_minigames`
- `mus_hg_wifi_parade`
- `mus_hg_wifi_plaza`
- `mus_hg_win_minigame`
