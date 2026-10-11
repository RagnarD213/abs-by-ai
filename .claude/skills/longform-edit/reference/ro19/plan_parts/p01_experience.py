# 1:55 to 6:29  His first spray tan: asking his AI, finding a studio, what it cost, tanning at home, the appointment, drying time
# Library first: Dan's own footage (B0437 phone by the pool, B0427 ab wheel, B0432 curls), then library stock, then two Pexels clips.
# The briefs / boxers / thong lines (4:21 to 5:37) stay on camera on purpose, with lower thirds: nothing there is pictured.
# Lead editor ranges left clear with 0.3 s either side: 180.25-186.50 (P03), 256.93-260.93 (A4), 378.11-383.48 (A3).
#
# NEEDS A PICTURE:
#  2:07 (126.9) "I uploaded my shitty pictures from the last photo shoot up into my AI": one of his real pale pictures from the
#       earlier shoot (lead editor's photos). 126.9 to 131.1 is left free of clips for it.
#  2:51 (170.9) "the contouring, which is extra shadowing on the abs to enhance the muscle definition": a real close picture of
#       his abs after the tan, where the contouring shows.
#  3:31 (211.2) "There are also tanning wipes that you can use": a tanning wipe or a pack of them (nothing in the library or the
#       Pexels index).
#  5:51 (351.1) "I needed to wait eight hours ... a full 24 hours": a wall clock or a phone timer (nothing in the library or the
#       index); the lower third Gb15 carries the two numbers.
# AI IDEAS:
#  5:51 (351.1) "I needed to wait eight hours before taking the shower": a gag, a freshly tanned man in a bathrobe sits on a
#       stool outside his own shower, arms folded, staring up at a wall clock; the shower door has yellow caution tape across it.
# SPECIAL:
#  6:06.4 to 6:11.7 repeats the sentence before it almost word for word ("From what my tanning specialist told me, there's not a
#       huge difference in the longevity"): it looks like a retake left in the locked cut. Nothing of mine sits on it.
#  4:17 "in and out of there in about 10 minutes" sits under A4, so no lower third of mine carries the 10 minutes.
#  3:06 the transcript reads "for ads by AI": he says "Abs By AI" (captions).
#  Gb17 ends at 388.3, just before the next part starts at 388.7.
PART = [
 dict(id="Cb01", kind="clip", start="didn't really know much about", end="being a man,", tail=0.1,
      src=[stock("pexels-7987790-woman-applying-makeup-on-a-client.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): a make-up artist brushes powder onto a client's face in a pink beauty salon, the 'beauty procedures' he says he knew nothing about"),
 dict(id="Cb02", kind="clip", start="then I asked my AI,", end="go get a spray tan.", tail=0.1, src=["B0437@0.3"], **DAN,
      note="Dan's own footage (library B0437): he stands by his pool reading and tapping on his phone, asking his AI"),
 dict(id="Gb01", kind="lt", start="then I asked my AI,", end="go get a spray tan.", tail=0.3, topic="HOW IT STARTED",
      point="My AI's Fix For Bad Photos: A Spray Tan", parts=[["My AI's Fix For Bad Photos:", "then I asked my AI"], ["A Spray Tan", "you need to go get"]]),
 dict(id="Cb03", kind="clip", start="for spray tan studios in my", end="away from my house.", tail=0.1, src=["B0220@1.0"], **NONE,
      note="Library stock (B0220): hands hold a phone and zoom in on a map with a pin, the studio a few miles from his house"),
 dict(id="Cb04", kind="clip", start="Go to Claude, go to", end="Gemini and say,", tail=0.08, src=["A0043@0.3"], **AIL, **OTHER,
      note="Library AI clip (A0043, AI-Dan): he types at a desk with several AI chat windows open side by side on three monitors, one per assistant he names. Ends before the fitness plan screen at the clip's tail"),
 dict(id="Gb02", kind="lt", start="Go to Claude, go to", end="best options around there,", tail=0.3, topic="FINDING A STUDIO",
      point="Ask AI For The 3 Best Studios Near You", parts=[["Ask AI", "Go to Claude"], ["For The 3 Best Studios Near You", "find me the three best"]]),
 dict(id="Cb05", kind="clip", start="I wanna do a spray", end="best options around there,", tail=0.1,
      src=[stock("pexels-10374923-close-up-on-man-hands-typing-message-on-phone.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): close on a man's hands typing a message on his phone, the request he tells the viewer to type"),
 dict(id="Cb06", kind="clip", start="So for me, I bought a", end="options you can buy.", tail=0.1, src=["B0242@0.5"], **NONE,
      note="Library stock (B0242): a customer's card goes into the handheld terminal a cashier holds out, paying for the premium tan"),
 dict(id="Gb03", kind="lt", start="and the contouring, which is", end="this was about $100", tail=0.6, topic="WHAT IT COST",
      point="$80 Base Tan, $20 Contouring: About $100", parts=[["$80 Base Tan,", "and the contouring"], ["$20 Contouring:", "about $20"], ["About $100", "about $100"]]),
 dict(id="Cb07", kind="clip", start="you wanna do it a little", end="a cheaper studio.", tail=0.1, src=["B0207@1.0"], **NONE,
      note="Library stock (B0207): hands count a small stack of twenty dollar bills on a dark table, the cheaper price"),
 dict(id="Gb04", kind="lt", start="you can get a spray tan", end="a cheaper studio.", tail=0.25, topic="THE CHEAPER ROUTE",
      point="About $50 If You Skip The Contouring", parts=[["About $50", "about $50"], ["If You Skip The Contouring", "if you skip the contouring"]]),
 dict(id="Cb08", kind="clip", start="There are aerosol do-it-yourself", end="tans that you can do.", tail=0.1, src=["B0225@0.5"], **NONE,
      note="Library stock (B0225): a hand presses the nozzle of an unbranded aerosol can and a fine mist sprays out"),
 dict(id="Gb05", kind="lt", start="want to look good, say,", end="where you're wearing clothes", tail=0.4, topic="TANNING AT HOME",
      point="For A Date Or A Wedding, With Clothes On", parts=[["For A Date Or A Wedding,", "on a date or for"], ["With Clothes On", "where you're wearing clothes"]]),
 dict(id="Cb09", kind="clip", start="for a wedding or for some", end="going to be visible.", tail=0.1, src=["B0197@0.5"], **OTHER,
      note="Library stock (B0197): a groom in a waistcoat and a bride in a lace gown laugh together outdoors, fully dressed, only faces and hands showing"),
 dict(id="Cb10", kind="clip", start="So if you're just going to", end="things like that.", tail=0.1, src=["B0318@1.0"], **OTHER,
      note="Library stock (B0318): a couple on a dinner date clink wine glasses across a restaurant table, forearms and hands in the shot"),
 dict(id="Cb11", kind="clip", start="if you have someone who can", end="places you can't reach,", tail=0.1, src=["B0232@0.5"], **OTHER,
      note="Library stock (B0232): a woman rubs lotion into the back of a man sitting on a garden lounger, the help with the places he cannot reach"),
 dict(id="Gb06", kind="lt", start="someone who can spray that aerosol", end="strapped for budget.", tail=0.25, topic="ON A BUDGET",
      point="With Help On Your Back, It Works For A Shoot", parts=[["With Help On Your Back,", "someone who can spray"], ["It Works For A Shoot", "it can also work even"]]),
 dict(id="Gb07", kind="lt", start="If you have the money though,", end="and for the contouring.", tail=0.25, topic="MY RECOMMENDATION",
      point="Go Pro For Even Coverage And Contouring", parts=[["Go Pro", "I recommend going professional"], ["For Even Coverage And Contouring", "just for full even coverage"]]),
 dict(id="Gb08", kind="lt", start="awkward part for those of", end="when you go there.", tail=0.25, topic="THE APPOINTMENT",
      point="The Awkward Part: Stripping To Your Briefs", parts=[["The Awkward Part:", "awkward part for those"], ["Stripping To Your Briefs", "strip down to your briefs"]]),
 dict(id="Gb09", kind="lt", start="then your spray tan is not", end="down to your thigh.", tail=0.25, topic="WHAT TO WEAR",
      point="Boxers Leave A Big Untanned Area", parts=[["Boxers Leave", "then your spray tan"], ["A Big Untanned Area", "a big untanned area"]]),
 dict(id="Gb10", kind="lt", start="I just wore a pair of", end="discarded them afterwards.", tail=0.3, topic="WHAT I WORE",
      point="Briefs I Was Fine With Throwing Away", parts=[["Briefs", "a pair of briefs"], ["I Was Fine With Throwing Away", "comfortable destroying"]]),
 dict(id="Gb11", kind="lt", start="get a male thong that", end="of a tan line.", tail=0.25, topic="NEXT TIME",
      point="Less Fabric, Less Tan Line", parts=[["Less Fabric,", "get a male thong"], ["Less Tan Line", "even less of a tan"]]),
 dict(id="Gb12", kind="lt", start="then I recommend you do this", end="to get in shape.", tail=0.15, topic="IF YOU'RE SELF-CONSCIOUS",
      point="Do It ANYWAY. It Pushes You To Get In Shape", parts=[["Do It ANYWAY.", "then I recommend you do"], ["It Pushes You To Get In Shape", "why it's going to be important"]]),
 dict(id="Cb12", kind="clip", start="why it's going to be important", end="getting in better shape", tail=0.1, src=["B0427@0.0", "B0432@1.2"], **DAN,
      note="Dan's own footage, two shots: ab wheel rollouts on a mat by his pool (B0427), then standing dumbbell curls by the pool (B0432), getting in shape"),
 dict(id="Gb13", kind="lt", start="Keep in mind though, these people", end="that they're tanning.", tail=0.3, topic="KEEP IN MIND",
      point="They're Professionals Who See This All Day", parts=[["They're Professionals", "these people are professionals"], ["Who See This All Day", "all the time"]]),
 dict(id="Gb14", kind="lt", start="So one downside of the spray", end="after you get the tan.", tail=0.25, topic="AFTERCARE",
      point="The Downside: No Shower Right Away", parts=[["The Downside:", "one downside of"], ["No Shower Right Away", "you can't take a shower"]]),
 dict(id="Cb13", kind="clip", start="that you can't take a shower", end="after you get the tan.", tail=0.1, src=["B0184@1.0"], **NONE,
      note="Library stock (B0184): a dry chrome shower head on a white tiled wall, turned off, the shower he has to wait for"),
 dict(id="Gb15", kind="lt", start="a rapid drying tan, I needed", end="a full 24 hours", tail=0.5, topic="HOW LONG TO WAIT",
      point="Rapid Tan: 8 Hours. Other Tans: 24 Hours.", parts=[["Rapid Tan:", "a rapid drying tan"], ["8 Hours.", "eight hours"], ["Other Tans:", "For other types of tans"], ["24 Hours.", "24 hours"]]),
 dict(id="Gb16", kind="lt", start="I personally recommend the rapid drying", end="the longevity of these tans.", tail=0.3, topic="MY PICK",
      point="Rapid Dry: It Lasts About As Long", parts=[["Rapid Dry:", "I personally recommend"], ["It Lasts About As Long", "there's not a huge difference"]]),
 dict(id="Gb17", kind="lt", start="recommend that rapid dry tan,", end="you get into bed", tail=0.1, topic="MY ADVICE",
      point="Tan Early In The Day, Shower Before Bed", parts=[["Tan Early In The Day,", "get it early in the day"], ["Shower Before Bed", "then shower before"]]),
]
