# 6:29 to 12:55  The first shower, the washing rules, how long it lasts, the water downside, then the pros (letter c)
# 7:44 to 8:00 stays on Dan on purpose: he shows his own tan ("as you can see", "if you were to zoom in here"), so no clip
# and no lower third sits there (a lower third would also sit over his abs in this waist-up frame).
# 9:19.56 to 9:52.93 (the before / after photo section) and 12:25.08 to 12:31.42 (AI clip A2) belong to the lead editor:
# nothing of this part is within 0.3 s of them.
#
# NEEDS A PICTURE:
#  7:15 "No washcloths for the duration of the tan": neither the library nor the Pexels index has a washcloth; he stays on
#       camera with a lower third (see AI IDEAS).
#  7:22 "glycolic acid or salicylic acid": no plain bottle of an exfoliating product; a hands-with-body-scrub clip covers the line.
#  8:06 to 8:32 very pale skin under a dark tan wears faster, naturally tan skin lasts longer: no stock fits. His real pale and
#       tanned photos side by side would show it (lead editor's photos).
#  8:55 "I have a pool I go in all the time": his real pool is library clip B0437, already claimed by part b, so a stock pool
#       is used here. If part b frees B0437, put it on Cc09.
#  9:00 "I sacrificed that this weekend": his own pool with nobody in it; nothing in the library shows that (B0473 is mostly a
#       dumbbell on the deck). He stays on camera with a lower third.
#  10:12 Bryan Johnson: no picture by rule; a lower third carries the point.
#  12:42 "the tan wears off in three to four days": a real photo of a fading tan would be the lead editor's.
#
# AI IDEAS:
#  7:15 "The washcloth is gonna exfoliate and powerfully remove the tan": a gag. A tanned man at a bathroom sink drags a
#       washcloth once down his forearm and it leaves one clean pale stripe; he stares at the stripe, then at the cloth.
#
# SPECIAL:
#  7:50 "if you were to zoom in here, you can see a slight amount of whitening on the abs": he asks for a zoom. A slow push-in
#       on his abs is a framing step for the lead editor, not a clip.
#  B0184 (the shower head) is on another part's claims list and part d has B0200 (sun through palms), so this part uses
#  neither a shower head nor a sun-in-the-sky shot: the first shower is carried by soap, a rinse and the drain.
PART = [
 dict(id="Gc01", kind="lt", start="Alright, so let's talk about that first", end="that will exfoliate you.", tail=0.3, topic="THE FIRST SHOWER",
      point="Rinse Only: No Soap, No Washcloth", parts=[["Rinse Only:", "In that first shower"], ["No Soap,", "use any soap"], ["No Washcloth", "especially a washcloth"]]),
 dict(id="Cc01", kind="clip", start="In that first shower, you can't", end="that will exfoliate you.", tail=0.1,
      src=[stock("pexels-6693710-bath-soaps-on-a-wooden-board.mp4", 5.0), stock("pexels-7815794-soap-bubble-and-sponge.mp4", 1.0)], **OTHER,
      note="Pexels stock (new), two shots: bars of soap on a wooden board as a hand lifts one away (no soap); then a bar of soap lathered on a scrubbing sponge (nothing that exfoliates)"),
 dict(id="Gc02", kind="lt", start="The tan is basically just a", end="off the tan itself.", tail=0.3, topic="KEY POINT",
      point="The Tan Is On The Surface: Don't Scrub It Off", parts=[["The Tan Is On The Surface:", "The tan is basically"], ["Don't Scrub It Off", "you're scrubbing off the tan"]]),
 dict(id="Cc03", kind="clip", start="There's going to be a bunch", end="tan is going away.", tail=0.1,
      src=[stock("pexels-855311-water-drain.mp4", 9.0)], **NONE,
      note="Pexels stock (new): brown-tinted water swirling down a drain, the brown water of the first shower"),
 dict(id="Gc03", kind="lt", start="a bunch of brown water that", end="the cosmetic makeup that they used", tail=0.3, topic="THE FIRST SHOWER",
      point="Brown Water Is Normal: It's Makeup, Not Tan", parts=[["Brown Water Is Normal:", "bunch of brown water"], ["It's Makeup, Not Tan", "the cosmetic makeup"]]),
 dict(id="Gc04", kind="lt", start="now, after this, you can start", end="duration of the tan.", tail=0.3, topic="AFTER THE FIRST SHOWER",
      point="Soap Is Fine Again, Washcloths Are Not", parts=[["Soap Is Fine Again,", "you can start showering normally"], ["Washcloths Are Not", "No washcloths for the"]]),
 dict(id="Cc04", kind="clip", start="after this, you can start showering", end="normally with soap,", tail=0.2,
      src=[stock("pexels-10574229-soaps-in-bathroom.mp4", 3.0)], **OTHER,
      note="Pexels stock (new): hands set a glass jar of soap bars beside a white bathroom sink and open it"),
 dict(id="Cc05", kind="clip", start="No exfoliating face clubs.", end="glycolic acid or salicylic acid.", tail=0.1,
      src=[stock("pexels-6725505-a-person-applying-scrub-on-her-hands.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): from above, hands rub a grainy scrub in over a tray of scrub bowls and cotton pads"),
 dict(id="Gc05", kind="lt", start="No exfoliating face clubs.", end="kind of things as well.", tail=0.3, topic="AFTERCARE",
      point="No Face Scrubs, No Glycolic Or Salicylic Acid", parts=[["No Face Scrubs,", "No exfoliating face"], ["No Glycolic Or Salicylic Acid", "No chemical exfoliants"]]),
 dict(id="Cc06", kind="clip", start="And generally just try to stay", end="with how you scrub.", tail=0.1,
      src=[stock("pexels-4115328-hands-water-safe-health.mp4", 15.5)], **OTHER,
      note="Pexels stock (new): hands lather soap slowly and gently under a running tap at a white basin"),
 dict(id="Gc06", kind="lt", start="stay as gentle as you can", end="you don't break out", tail=0.3, topic="AFTERCARE",
      point="Gentle Soap, Light Hands, Just The Minimum", parts=[["Gentle Soap,", "stay as gentle"], ["Light Hands,", "how you scrub"], ["Just The Minimum", "Just do the minimum"]]),
 dict(id="Gc07", kind="lt", start="From what I've been told, these", end="pretty good so far.", tail=0.3, topic="HOW LONG IT LASTS",
      point="About 7 Days, And Day 5 Still Looks Good", parts=[["About 7 Days,", "From what I've been told"], ["And Day 5 Still Looks Good", "I'm on day five"]]),
 dict(id="Gc08", kind="lt", start="if you have naturally more tan", end="a little bit longer", tail=0.4, topic="HOW LONG IT LASTS",
      point="Closer To Your Natural Shade Lasts Longer", parts=[["Closer To Your Natural Shade", "if you have naturally more tan"], ["Lasts Longer", "probably gonna last"]]),
 dict(id="Cc07", kind="clip", start="If you go in the water,", end="your tan off faster.", tail=0.04,
      src=[stock("pexels-8686094-a-man-swimming-in-the-pool-while-wearing-his-goggles.mp4", 4.6), stock("pexels-8974074-a-man-walking-towards-the-sea.mp4", 0.5)], **OTHER,
      note="Pexels stock (new), two shots: a swimmer in a cap pushes off the wall of a pool and swims away; then bare feet wade out into shallow open water"),
 dict(id="Gc09", kind="lt", start="If you go in the water,", end="your tan off faster.", tail=0.0, topic="THE DOWNSIDE",
      point="Pool, Lake Or Beach: Water Fades It Faster", parts=[["Pool, Lake Or Beach:", "If you go in the water"], ["Water Fades It Faster", "that is going to wear"]]),
 dict(id="Cc08", kind="clip", start="That's not recommended if you want", end="whatever event you're doing.", tail=0.1,
      src=[stock("pexels-31512200-studio-portrait-photography-session-with-model.mp4", 0.3)], **OTHER,
      note="Pexels stock (new): a photographer shoots a man beside a big round studio light in a brick loft, the photo shoot the tan has to last for"),
 dict(id="Cc09", kind="clip", start="I like going in the water.", end="go in all the time.", tail=0.18,
      src=[stock("pexels-7293598-a-man-dipping-in-the-swimming-pool.mp4", 0.3)], **OTHER,
      note="Pexels stock (new): a smiling man up to his shoulders in a sunny outdoor pool. His own pool (library B0437) is claimed by part b"),
 dict(id="Cc10", kind="clip", start="I go paddleboarding all the time,", end="one of my favorite things.", tail=-0.3,
      src=["B0177@2.0", "B0188@2.0"], **NONE,
      note="Library, two shots: B0177, a lone paddleboarder crossing a calm lake at dusk; then B0188, a pontoon boat cruising a blue lake (boating)"),
 dict(id="Gc10", kind="lt", start="I sacrificed that this weekend for", end="five days in", tail=0.3, topic="WHY I STAYED DRY",
      point="No Water All Weekend For A Fair Day 5 Test", parts=[["No Water All Weekend", "I sacrificed that this weekend"], ["For A Fair Day 5 Test", "a fair example"]]),
 dict(id="Cc11", kind="clip", start="In my normal life I'm", end="the water all the time", tail=0.1,
      src=[stock("pexels-18187089-a-man-swimming-underwater-in-a-pool.mp4", 14.0)], **OTHER,
      note="Pexels stock (new): seen from under the surface, a man swims underwater toward the camera in a clear blue pool"),
 dict(id="Gc11", kind="lt", start="Let's talk about the pros and", end="not get a spray tan?", tail=0.25, topic="UP NEXT",
      point="Pros, Cons, Who It's For, Who Should Skip It", parts=[["Pros, Cons,", "Let's talk about the pros"], ["Who It's For,", "Who is spray tanning right"], ["Who Should Skip It", "who should not get"]]),
 dict(id="Gc12", kind="lt", start="So the most important pro of", end="avoiding sun damage.", tail=0.3, topic="THE BIGGEST PRO",
      point="You Get The Tan WITHOUT The Sun Damage", parts=[["You Get The Tan", "So the most important pro"], ["WITHOUT The Sun Damage", "while avoiding sun"]]),
 dict(id="Cc12", kind="clip", start="And the sun is a lot", end="than people think.", tail=0.7,
      src=[stock("pexels-7892918-woman-sitting-on-the-beach.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): a woman in a blue sundress sits on the sand with her face turned up to the full sun"),
 dict(id="Gc13", kind="lt", start="If you ever notice why the", end="trying to avoid skin damage,", tail=0.3, topic="BRYAN JOHNSON",
      point="He Stays Pale To Avoid Cancer And Skin Damage", parts=[["He Stays Pale", "If you ever notice why"], ["To Avoid Cancer", "trying to avoid cancer"], ["And Skin Damage", "trying to avoid skin damage"]]),
 dict(id="Cc13", kind="clip", start="sun exposure is one of the", end="common causes of cancer.", tail=0.52,
      src=["B0233@1.0"], **OTHER,
      note="Library B0233: a man sitting on a striped beach blanket rubs sunscreen into his forearm"),
 dict(id="Cc14", kind="clip", start="Skin cancer is one of the", end="the most common cancers and", tail=0.0,
      src=["B0208@1.0"], **OTHER,
      note="Library B0208: a skin specialist in a white uniform and gloves talks a young woman through her skin in a bright clinic"),
 dict(id="Cc16", kind="clip", start="Researchers coming out showing that sun", end="different health conditions.", tail=0.1,
      src=["B0013@2.0"], **OTHER,
      note="Library B0013: a doctor at her desk in a bright office explains something to a male patient seen from behind"),
 dict(id="Gc14", kind="lt", start="So even though a natural", end="and is aging you", tail=0.3, topic="KEY POINT",
      point="A Natural Tan Is Sun Damage, Not Health", parts=[["A Natural Tan", "even though a natural"], ["Is Sun Damage, Not Health", "it is not healthy"]]),
 dict(id="Cc17", kind="clip", start="if you look at people who", end="entire life in the Sun", tail=0.0,
      src=[stock("pexels-11493545-drone-video-of-people-on-a-sandy-beach.mp4", 0.3)], **OTHER,
      note="Pexels stock (new): a drone glides along a white sand beach dotted with sunbathers and umbrellas beside turquoise water"),
 dict(id="Gc15", kind="lt", start="if you look at people who", end="in their 50s and 60s", tail=0.3, topic="SUN DAMAGE",
      point="A Lifetime In The Sun Shows By Your 50s", parts=[["A Lifetime In The Sun", "if you look at people who"], ["Shows By Your 50s", "They look visibly more aged"]]),
 dict(id="Cc18", kind="clip", start="They look visibly more aged when", end="result of this sun damage.", tail=0.1,
      src=[stock("pexels-8161090-a-couple-at-the-beach.mp4", 4.0), stock("pexels-8818544-elderly-woman-dancing-on-beach.mp4", 0.5)], **OTHER,
      note="Pexels stock (new), two shots: a white-haired man in a denim jacket carries his partner along the surf; then an older woman in white dances and laughs on the beach"),
 dict(id="Cc19", kind="clip", start="If you did not spend that", end="the heavy sun tanning", tail=0.1,
      src=["B0259@0.5"], **OTHER,
      note="Library B0259: a wide shot of a man lying face down on an empty beach by a turquoise sea, tanning"),
 dict(id="Gc16", kind="lt", start="instead you were placed at with", end="less likely to get cancer.", tail=0.3, topic="SPRAY VS SUN",
      point="Spray, Not Sun: Look Younger, Less Cancer Risk", parts=[["Spray, Not Sun:", "instead you were placed"], ["Look Younger,", "not only look younger"], ["Less Cancer Risk", "less likely to get"]]),
 dict(id="Gc17", kind="lt", start="Maybe you have no choice.", end="could see your veins,", tail=0.3, topic="ANOTHER REASON",
      point="No Choice: Very Pale Skin Burns, Not Tans", parts=[["No Choice:", "Maybe you have no choice"], ["Very Pale Skin Burns, Not Tans", "ultra pale translucent white"]]),
 dict(id="Cc20", kind="clip", start="If you're a ginger, if you", end="could see your veins,", tail=0.1,
      src=[stock("pexels-8724508-a-man-wearing-pink-shirt.mp4", 0.5), stock("pexels-10210876-studio-portrait-of-redheaded-woman.mp4", 1.0)], **OTHER,
      note="Pexels stock (new), two clothed portraits: a red-haired man in a pink sweater against a blue wall; then a very fair red-haired woman in a plain top, studio light"),
 dict(id="Cc21", kind="clip", start="You're just gonna get a sunburn,", end="in the sun too much.", tail=0.1,
      src=[stock("pexels-7467143-people-applying-sunscreen-on-their-faces.mp4", 0.2)], **OTHER,
      note="Pexels stock (new): three friends at the beach dab sunscreen onto their faces and grin at the camera"),
 dict(id="Gc18", kind="lt", start="it's gonna make a difference, believe", end="making your tan last", tail=0.25, topic="IF YOU'RE SUPER PALE",
      point="Go Subtle: It Still Shows And It Lasts Longer", parts=[["Go Subtle:", "it's gonna make a difference"], ["It Still Shows", "even if it's subtle"], ["And It Lasts Longer", "additional benefit of making"]]),
 dict(id="Gc19", kind="lt", start="People that go super dark with", end="wearing off is noticeable.", tail=0.2, topic="HOW LONG IT LASTS",
      point="Very Dark On Very Pale Fades In 3 To 4 Days", parts=[["Very Dark On Very Pale", "People that go super dark"], ["Fades In 3 To 4 Days", "the tan wears off in"]]),
]
