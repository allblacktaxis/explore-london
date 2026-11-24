# Explore London – shared to-do list

Tick items off (`- [x]`) when they're done, and add anything new Matt asks for.

## Time-sensitive
- [ ] Re-check Christmas Day prices nearer the day: Le Pont de la Tour (no price yet), Gaucho (£125 not confirmed), The Alexandra (free lunch not yet announced for 2026), Claridge's / Kerridge's / Holly Bush / Red Lion & Sun / Mad Hatter / Prince Albert / Hand & Flower (price on booking)
- [ ] Re-check New Year's Eve prices nearer the day, especially Oscar (£45 may be old), Kinz (not yet confirmed for NYE) and the Thames cruises

## Still open from 9 Nov
- [ ] App buzz needs the next app-store builds: iPhone app needs the Capacitor Haptics plugin added (the code already uses it if it's there); Android app now has the VIBRATE permission, which takes effect at the next Android build
- [ ] Suggest a place: at the start of each session, check new suggestions in Netlify (Forms → "suggest") and show them to Matt – no email needed (Matt chose this, 17 Nov)
- [ ] www address: needs Matt to say what he meant and who looks after the allblacktaxis.co.uk address – can't be done from the app's files (DNS + Netlify domain settings)

## Translation (agreed 17 Nov: option C – everything, in stages; Spanish, French, German, Italian, Chinese; row of 6 small flags under "Explore London" on Home, UK flag to switch back; auto-pick phone language)
- [x] Stage 1: flags + the app's own words (641 phrases × 5 languages, lang/*.json) – live 17 Nov. Search still English-only (box says so); WhatsApp/suggest messages stay English
- [ ] Stage 2: most-visited places, walks and Cabbie's Stories
- [ ] Stage 3: everything else, area by area (and translate each new place as it's added)

## Content
- [ ] Oldest pubs: set a `year` for other old pubs that still have none (e.g. The Anchor Bankside, The Dove, The Gatehouse, The Grenadier, The Gun) – check dates first
- [ ] Photos – fix the photos on every place where the photo isn't correct (go through all places, Matt to confirm the wrong ones).
- [ ] Restaurant batch, area by area (held list from the old chat is lost, so building fresh): done Battersea, Richmond & Kew, Greenwich, King's Cross, Kensington, Docklands (first pass) – Matt wants to talk more about Kensington
- [ ] Fish & chips: King's Cross still has no chippy in its own area (nearest is North Sea Fish, Leigh Street, filed under Bloomsbury) – leave unless Matt wants it moved

- [ ] Batch 24 Nov – still to confirm: The Bull is in Charlbury, Oxfordshire (added under Beyond London – keep or remove?); "Virtual Arena" at Battersea doesn't exist, added DNA VR Battersea instead; Veeraswamy lease case in court (Nov 2026) – re-check it's still open; car hire opening hours came from search results, not the firms' own pages – spot-check (Enterprise Paddington and Europcar Heathrow hours unknown); "Arcades" pill still includes bingo/board-game bars (Hijingo, Dabbers, Draughts, Fairgame) – rename to "Arcades & games"?
- [ ] Translation stage 2/3 not started, so the 41 new places are English only for now (new buttons and labels are translated)

## To discuss
- [x] Built 17 Nov – Home screen redesign (mock-up: https://claude.ai/artifact/49YuMGTNF89FiYZsDcKcYL): 4 group buttons (History & sights first) with hints; Near me now + Tube & Trains at the top; bigger "Plan your day" cards; keep search, Where are you staying?, On this day. Matt chose A (options open underneath on the same screen) and the list layout (one group per row, not 2×2). Headings: "Things to do in London" above the 4 groups, "Plan your day" above the cards. Keep the app's existing category icons and tile colours exactly (catIcon / CAT colours) – the mock-up's emoji are placeholders only. Built and live 17 Nov.
- [x] Built 17 Nov – Suggestions box wording → "Share a London favourite" / "A place you love, or an idea for the app" (Matt chose 17 Nov); add an "It's an idea for the app" option to the form so a place name isn't required
- [ ] First-time help cards + "Tell us what interests you" (combined): mock-up https://claude.ai/artifact/7SCjgzjbFtRAoA4Gs3mB53 – 3 how-it-works cards, then 3 questions (interests, who's with you, where staying), then "Picked for you" on Home. Matt wants more time to think about it (17 Nov) – saved, NOT to be built until he decides. Options on the table: (a) cards + questions at first open, (b) a "Make it yours" button on Home instead, so nobody is slowed down
- [ ] Blue Plaques – agreed 17 Nov (option C): (1) add 5–10 more plaques per theme near the existing clusters so walks have 6–8 stops – show Matt the list first; (2) ready-made themed walks (Musicians of Mayfair, Writers of Chelsea, Scientists of Soho & Bloomsbury, Royals & leaders of Mayfair, Film & TV of Kensington, Artists of Chelsea) with buzz + stories; (3) "build your own" plaque walk: pick themes, app builds from nearest plaques (reuse Build my walk). Do after translation Stage 1 and the new Home screen
- [ ] Per-area targets – proposed 17 Nov: central 25+ restaurants & 8+ pubs; day-out areas 15+ & 6+; local neighbourhoods 8+ & 4+. Pubs are the main gap (Marylebone, Mayfair, South Bank, King's Cross, Notting Hill, Peckham, Bermondsey). Matt to confirm
- [ ] How new places get added

## Parked
- [ ] Stadium/hotel-area pubs and restaurants (ask Matt first) – Twickenham/Richmond rugby pubs done 17 Nov; other grounds still to do
- [ ] Eat & drink nearby on the remaining walks
- [ ] Walks: oldest pubs, Ted Lasso, London on Film, Banksy
- [ ] Audio guide
- [ ] Make My Walk
- [ ] Making money

## Done
- [x] Bottom tab bar fixed for good (24 Nov): the bar is now lifted out of the page box straight into <body> on every page (so nothing around it can make it scroll away), centred without a transform, and every page leaves room for it plus the iPhone home-bar gap, so the last item on each list is never hidden
- [x] Batch round 3 (24 Nov): Karaoke (6 new + 6 tagged, new Karaoke collection, "Arcade & karaoke" pill now "Arcades"); The Horses, The Hero, The Bull + "From the team behind…" line on all six; new Car hire category (20 branches by 7 stations, Heathrow and City Airport, Congestion Charge/ULEZ banner, cabbie's tip on each, "Nearest car hire" on every day trip); 41–42 Cloth Fair; "London's oldest" collection (27 places, Home link + History pill); Dickens Tavistock Square plaque, Charles Dickens's London walk, Down House; Sandbox VR ×3, DNA VR Battersea, VR & gaming collection; Dickens Inn now under Pubs too; Lucky Voice updated (Islington and Waterloo closed Oct 2026); Rock & Sole Plaice was already in the app, so tagged rather than added
- [x] London's oldest pubs banner now shows every pub from before 1800 (25 today) instead of a top 10 – live 17 Nov
- [x] London's oldest pubs fixed: list now uses a `year` in places.json when set (The Guinea 1423, Prospect of Whitby 1520, Town of Ramsgate 1545, Mayflower 1550, George Inn 1542, The Grapes 1583, Spaniards Inn 1585, Seven Stars 1602, The Flask 1663) and 5 famous old City pubs added (Hand & Shears 1532, Jamaica Wine House 1652, Olde Wine Shades 1663, Ye Olde Watling 1668, The Old Bell Tavern 1678). Dates are the earliest pub on the site, as most guides quote them – live 17 Nov
- [x] Pubs batch 17 Nov: Bankside & Borough +10 (Anchor Bankside, Market Porter, Rake, Royal Oak, Southwark Tavern, Globe Tavern, Ship, Old Thameside Inn, Mudlark, Founders Arms); Shoreditch +5 (Pride of Spitalfields, Water Poet, Commercial Tavern, Golden Heart, Old Blue Last); Battersea +3 (Duke of Cambridge, Battersea Brewery Tap Room, Four Thieves). Approx pins: The Ship Borough, Battersea Brewery Tap Room
- [x] Tidy-ups 17 Nov: exact addresses/pins for 14 places (Richmond, Kensington, Docklands); Light of India moved to its real address on Gloucester Road (Kensington); Tower House location corrected; Roti King Battersea address; Wandercrust (at the Pelton Arms) and Madre Pinzeria added in Greenwich; The Grapes now listed for fish & chips (fills Docklands gap); Latchmere looks open (refurbished Jan 2026)
- [x] "Suggest a place" box now also on every place page (under Also nearby; not on blue plaques) – 17 Nov
- [x] Kensington (Matt's picks): Khan's of Kensington, Ffiona's, Bottega 35, Yashin Sushi, Akira at Japan House, Caffè Concerto, Como Garden, Zaika (approx pin – check address), Locanda Ottoemezzo – 17 Nov
- [x] Kensington: Kitchen W8, Pascor, Samad Al Iraqi, Pravaas; Chelsea: Light of India, Elystan Street; Docklands: Hawksmoor Wood Wharf, Marceline, Hovarda, Emilia's, Blacklock, Pergola – 17 Nov. Approx pins to fix: Samad Al Iraqi, Pravaas, Light of India, all six Docklands, plus Tower House, Peggy Jean, Sebastian's, Alexander Pope
- [x] King's Cross: El Pastor CDY, Coal Office, Parrillan, Vermuteria, Morty & Bob's, Rotunda – 17 Nov
- [x] Greenwich: Sticks'n'Sushi, Tai Won Mein, Kinaara + pubs Gipsy Moth, Old Brewery, Plume of Feathers, Richard I – 17 Nov
- [x] Richmond & Kew: 9 restaurants/food pubs + 3 rugby pubs (Sun Inn, Old Ship, Alexander Pope; Orange Tree also tagged rugby); White Cross and White Swan now also under Restaurants – 17 Nov. Pins for Tower House, Peggy Jean, Sebastian's and Alexander Pope are approximate.
- [x] Battersea: 9 restaurants added (Vagabond, Wright Brothers, Noci, Roti King, Arcade, Fiume, Where the Pancakes Are, Boqueria, The Latchmere) – 17 Nov
- [x] Fish & chips: added Fish! Borough Market, Applebee's, Fishers, Baileys, Geales; Hereford Arms now mentions fish and chips – 17 Nov
- [x] deploy-check.txt – not in either app, nothing to delete – 17 Nov
- [x] "Suggest a place" form (Home + bottom of each category) and "Explore London customer comment" on place pages (add `"comment": {"text": "...", "name": "..."}` to a place) – 17 Nov
- [x] Walk alerts: "Start walk" button – phone buzzes and the stop's note + Cabbie's Story pops up within 35 m of each stop – 17 Nov
- [x] Smooth map zoom – already fixed when the map moved to MapLibre; confirmed by Matt 17 Nov
- [x] London Museum card now says "open from 28 November 2026" – 17 Nov
- [x] "See the Changing the Guard route" button on every place that's a stop on that walk (Buckingham Palace, St James's Palace, Horse Guards Parade, Wellington Arch, Guards Museum) – 17 Nov
- [x] Guards Museum added (#1337) and linked from the Wellington Barracks stop on the Changing the Guard walk – 17 Nov
- [x] Duplicates checked: only one Weezie's in the app; the two Shoryu Ramens are different branches (Soho and Covent Garden); #150 is The Marlborough – nothing to remove – 17 Nov
- [x] New Year's Eve: 24 places tagged (7 already in the app, 17 new) – 17 Nov
- [x] Christmas Day: 39 places tagged (17 already in the app, 22 new) – 17 Nov
- [x] Seasonal pill: Christmas Day / New Year's Eve places all the time, plus Thanksgiving places up to 26 Nov (no longer matches "seasonal menu") – 17 Nov
- [x] Top-left pill (Restaurants and Pubs) shows the nearest season: Thanksgiving up to 26 Nov, then Christmas & New Year – 17 Nov
