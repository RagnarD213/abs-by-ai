# 12:55 to 17:46  The cons, who should and should not spray tan, the photo shoot tips, the wrap-up (part d)
# He does not number the cons or the "who" list (only "Number one, vampires", which is the lead editor's A1), so the labels
# are plain: CON: ..., WHO SHOULD TAN, WHO SHOULD WAIT, SHOOT TIP: ...
# Left on camera on purpose: 14:05 to 14:14 ("if you look at me, I'm not looking too orange right now", he is showing his tan);
# 15:56 to 16:08 ("you're rich, you're ripped ... you're poor, you're fat", said straight to the viewer, no stomach pictured);
# 17:30 to 17:36 and the last line of the wrap-up (his closing recommendation, eye contact).
#
# NEEDS A PICTURE:
#  13:40 (820.1) "you can self-apply at home ... if you don't have a partner and you can't reach your whole body": Pexels has only
#        sunscreen and bare-skin cream close-ups, nothing that reads as self tanner. On camera with a lower third.
#  13:52 (832.0) "for certain people, such as myself, who naturally tan very well": one of his real photos with a natural tan.
#  14:14 (854.1) "home tanning products or very cheap spray tan": the home tanning products he means (bottle, mousse, mitt).
#  15:05 (905.7) "at least do the tanning wipes or the tanning spray": the wipes and the spray themselves.
#  15:29 (929.8) "once you already have the body to show off in photo shoots": covered with his real posing footage (B0459); one of
#        his real pool shoot photos would be stronger if the lead editor wants it there.
#  16:50 (1010.3) "the work that you put into getting this body": a real photo from the pool shoot.
# AI IDEAS:
#  13:44 (824.7) "If you don't have a partner and you can't reach your whole body, it's going to be less even": a gag. A man alone in
#        his bathroom twists and strains to reach the middle of his back with a tanning mitt; he turns round proud, and his back is
#        evenly tanned except one pale mitt-shaped patch right in the middle that he cannot see.
# SPECIAL:
#  A1 (14:43.1 to 14:49.7, 883.09 to 889.65) is the lead editor's; Gd06 starts 1.3 s after it and Cd04 ends 2.8 s before it.
#  Cd02 is an AI library clip (A0081), so it carries the AI-GENERATED label; every other clip here is real footage.
#  B0218, B0200, B0249, B0251 and B0191 were in the earlier Claude cut of this same film (library "used_in"), nowhere else in this plan.
PART = [
 dict(id="Gd01", kind="lt", start="So the most obvious con is", end="50 to $100 per tan.", tail=0.3, topic="CON: THE COST",
      point="A Pro Tan Runs $50 To $100 Every Time", parts=[["A Pro Tan Runs", "If you do professional spray"], ["$50 To $100 Every Time", "between 50 to"]]),
 dict(id="Cd01", kind="clip", start="You don't have enough money for", end="or a GLP -1 or TRT", tail=0.15,
      src=["B0141@0.5", "B0093@1.0", "B0483@2.0"], **OTHER,
      note="Three library stock shots on the three things he lists: a row of treadmills in a gym with members walking past (gym membership), hands packing a table of meal prep containers (meal prep service), hands drawing a dose from a vial into a syringe on a plain blue field (GLP-1, TRT; no brand visible)"),
 dict(id="Gd02", kind="lt", start="a great gym membership or a", end="lower priority than that.", tail=0.3, topic="WHAT TO BUY FIRST",
      point="Gym And Meal Prep First, Then The Tan", parts=[["Gym And Meal Prep First,", "a great gym membership"], ["Then The Tan", "a spray tan is a lower"]]),
 dict(id="Cd02", kind="clip", start="a great gym membership or a", end="or a meal prep service,", tail=0.1,
      src=["A0081@0.3"], **AIL, **OTHER,
      note="Library AI clip (WV-01): a man in a tank top in a garage home gym with a rack and dumbbells, drinking water between sets: the gym or home gym he says comes first"),
 dict(id="Cd03", kind="clip", start="If on the other hand you", end="lots of money left over,", tail=0.1,
      src=[stock("pexels-5466769-a-person-counting-money.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): hands counting a stack of dollar bills on a table: the funds and the money left over"),
 dict(id="Gd03", kind="lt", start="If you don't have a partner", end="come with its own drawbacks.", tail=0.2, topic="CON: DOING IT YOURSELF",
      point="No Partner? Expect A Less Even Tan", parts=[["No Partner?", "If you don't have a partner"], ["Expect A Less Even Tan", "going to be less even"]]),
 dict(id="Gd04", kind="lt", start="I would say that's more applicable", end="actually look very natural.", tail=0.0, topic="CON: THE COLOR",
      point="Cheap Looks Orange, Premium Looks Natural", parts=[["Cheap Looks Orange,", "more applicable to home tanning"], ["Premium Looks Natural", "If you go premium,"]]),
 dict(id="Gd05", kind="lt", start="like I mentioned before, is it", end="more subtle on dark skin.", tail=0.1, topic="THE BIGGEST CON",
      point="Lasts About A Week, Less If You Go Dark", parts=[["Lasts About A Week,", "is it wears off in"], ["Less If You Go Dark", "a little sooner if you"]]),
 dict(id="Cd04", kind="clip", start="So, if you go in the", end="another significant drawback.", tail=0.0,
      src=["B0218@4.0", stock("pexels-7020150-woman-applying-body-scrub-to-her-arms.mp4", 2.0)], **OTHER,
      note="Two shots, one per sentence: a swimmer doing front crawl down a pool lane, seen from above (library stock), then a woman in a dress rubbing a body scrub into her forearm, face out of frame (Pexels stock, new)"),
 dict(id="Gd06", kind="lt", start="otherwise your skin is gonna look", end="You want to look good.", tail=0.3, topic="WHO SHOULD TAN",
      point="Very Pale? A Spray Tan Is A Must", parts=[["Very Pale? A Spray Tan Is A Must", "otherwise your skin is gonna"]]),
 dict(id="Gd07", kind="lt", start="if you're strapped for fonts,", end="acceptable with clothes on.", tail=0.3, topic="VERY PALE, LOW BUDGET",
      point="At Least Use Tanning Wipes Or Spray", parts=[["At Least Use Tanning Wipes Or Spray", "at least do the tanning"]]),
 dict(id="Gd08", kind="lt", start="People who are poor should not", end="home gym, the essentials,", tail=0.3, topic="WHO SHOULD WAIT",
      point="Money Tight? Essentials Before A Pro Tan", parts=[["Money Tight?", "People who are poor"], ["Essentials Before A Pro Tan", "If you can't afford that"]]),
 dict(id="Cd05", kind="clip", start="People who are poor should not", end="these professional spray tans.", tail=0.16,
      src=[stock("pexels-11099870-close-up-view-of-empty-wallet.mp4", 2.0)], **OTHER,
      note="Pexels stock (new): a man in a grey hoodie opens his wallet and finds it empty, framed on the wallet and his hands"),
 dict(id="Cd06", kind="clip", start="If you can't afford that meal", end="home gym, the essentials,", tail=0.1,
      src=["B0441@0.5", "B0449@0.0"], **DAN,
      note="Dan's own footage, two shots: sealing glass containers of salad on his kitchen island (meal prep), then seated dumbbell presses on a chair by his pool, starting on the press (his home gym)"),
 dict(id="Gd09", kind="lt", start="Invest in that now, and then", end="then invest in the spray tan.", tail=0.0, topic="KEY POINT",
      point="Build The Body FIRST, Then Add The Tan", parts=[["Build The Body FIRST,", "Invest in that now"], ["Then Add The Tan", "once you already have"]]),
 dict(id="Cd07", kind="clip", start="Invest in that now, and then", end="show off in photo shoots,", tail=0.3,
      src=["B0439@0.0", "B0459@0.5"], **DAN,
      note="Dan's own footage, two shots: kettlebell swings on the mat by the lawn (invest in that now), then his side chest pose beside the pool (the body to show off in photo shoots)"),
 dict(id="Gd10", kind="lt", start="if your money substantially depends on", end="if you're an influencer,", tail=0.1, topic="WHO SHOULD TAN",
      point="When Your Income Depends On Your Looks", parts=[["When Your Income Depends On Your Looks", "if your money substantially"]]),
 dict(id="Cd08", kind="clip", start="if you're going on camera,", end="if you're an influencer,", tail=0.54,
      src=[stock("pexels-6332246-a-man-recording-a-video.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): a man films himself talking, seen through the phone in a ring light: on camera, an influencer"),
 dict(id="Cd09", kind="clip", start="if you're dealing with clients in", end="person all the time,", tail=0.23,
      src=["B0024@6.5"], **OTHER,
      note="Library stock (first use): a man in a suit stands, shakes a visitor's hand across the desk and waves him to a seat: clients in person"),
 dict(id="Cd10", kind="clip", start="If you're in an industry like", end="appearance is very important,", tail=0.1,
      src=[stock("pexels-855563-video-of-women-modelling.mp4", 7.0), "B0251@1.0"], **OTHER,
      note="Two shots on the two industries he names: a fashion model walks toward the camera in a bare brick studio (Pexels stock, new), then a hairdresser trims a client's hair in a bright salon (library stock)"),
 dict(id="Gd11", kind="lt", start="Most of you guys are gonna", end="photos or shooting videos", tail=0.3, topic="MOST PEOPLE",
      point="In The Middle? Tan For The Big Moments", parts=[["In The Middle?", "Most of you guys"], ["Tan For The Big Moments", "make sense sometimes"]]),
 dict(id="Cd11", kind="clip", start="like when you're shooting photos or", end="a wedding to go to.", tail=0.1,
      src=["B0192@1.0", stock("pexels-7514334-a-man-using-smartphone-for-video-recording.mp4", 3.0), "B0191@0.3"], **OTHER,
      note="Three quick shots on the three occasions: a photographer directing a model under a studio softbox (library stock, first use), a man filming on a phone on a tripod (Pexels stock, new), a bride and groom walking up the aisle under confetti (library stock)"),
 dict(id="Cd12", kind="clip", start="sometimes, maybe in the winter when", end="you can't naturally tan,", tail=0.2,
      src=[stock("pexels-7026845-video-of-a-man-walking.mp4", 4.0)], **OTHER,
      note="Pexels stock (new): a man in a hooded parka walks toward the camera across a snow field: the winter, when you can't tan naturally"),
 dict(id="Cd13", kind="clip", start="If you're a real baller, you", end="a regular beauty procedure,", tail=0.1,
      src=[stock("pexels-7754480-a-client-paying-cashless-at-a-beauty-salon.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): a client pays by card at the front desk of a beauty salon: a regular weekly beauty appointment"),
 dict(id="Gd12", kind="lt", start="then you really want to maximize", end="most out of your spray tan", tail=0.25, topic="MAXIMIZE YOUR TAN",
      point="Book A Photo Shoot While You're Tanned", parts=[["Book A Photo Shoot While You're Tanned", "Do a photo shoot during"]]),
 dict(id="Cd14", kind="clip", start="Do a photo shoot during that", end="when you do that photo shoot,", tail=0.1,
      src=[stock("pexels-10251024-woman-taking-photo-of-a-man-leaning-on-a-railing.mp4", 2.0)], **OTHER,
      note="Pexels stock (new): a photographer shoots a man posed on a fire escape against a brick wall: an outdoor photo shoot"),
 dict(id="Gd13", kind="lt", start="Make sure that you have good", end="that golden hour lighting.", tail=0.2, topic="SHOOT TIP: LIGHTING",
      point="Skip Flat Noon Sun, Shoot At Golden Hour", parts=[["Skip Flat Noon Sun,", "Ideally you avoid noon"], ["Shoot At Golden Hour", "Ideally you get that golden"]]),
 dict(id="Cd15", kind="clip", start="Ideally you avoid noon time lighting", end="that golden hour lighting.", tail=0.58,
      src=["B0200@1.0", "B0249@1.0"], **OTHER,
      note="Two library stock shots, one per sentence: the high midday sun in a hard blue sky over palm and pine tops (flat overhead noon light), then a woman's face in warm, low golden hour sun with lens flare"),
 dict(id="Cd16", kind="clip", start="Make sure that you have a", end="using a good camera.", tail=0.1,
      src=[stock("pexels-7206358-a-photographer-looking-in-the-camera-viewfinder.mp4", 2.0)], **OTHER,
      note="Pexels stock (new): a photographer by a big window raises a professional camera and directs his subject with his free hand"),
 dict(id="Gd14", kind="lt", start="Get a pump before you're shooting.", end="so that way you maximize", tail=0.1, topic="SHOOT TIP: PUMP UP",
      point="Before You Shoot: Push-Ups, Curls, Abs", parts=[["Before You Shoot:", "Get a pump before"], ["Push-Ups,", "do some push ups,"], ["Curls,", "do some curls,"], ["Abs", "do some ab exercises"]]),
 dict(id="Cd17", kind="clip", start="By that I mean just do", end="ab exercises before you shoot", tail=0.25,
      src=["B0547@0.0", "B0458@0.0", "B0467@0.0"], **DAN,
      note="Dan's own workout footage, one shot per exercise he names, each starting on a rep: push-ups on the blue mat by the pool in low sun, standing dumbbell curls facing the camera in daylight, lying toe-touch crunches on a mat in bright sun"),
 dict(id="Gd15", kind="lt", start="And then you wanna shoot fasted.", end="shoot to get the best", tail=0.3, topic="SHOOT TIP: FASTING",
      point="Don't Eat Before The Shoot: It Shows", parts=[["Don't Eat Before The Shoot:", "Don't eat food before"], ["It Shows", "visibly affect your body"]]),
 dict(id="Cd18", kind="clip", start="Don't eat food before you shoot,", end="visibly affect your body.", tail=0.1,
      src=["B0064@0.0", "B0066@0.0"], **OTHER,
      note="Two short library stock shots of the food to skip: a whole pizza turning in its delivery box, then a man forking up a plate of eggs and toast"),
 dict(id="Gd16", kind="lt", start="Finally, before your shoot, spend five", end="about basic poses,", tail=0.2, topic="SHOOT TIP: POSING",
      point="Spend 5 To 10 Minutes On Your Poses", parts=[["Spend 5 To 10 Minutes", "spend five to 10"], ["On Your Poses", "maximizing your posing."]]),
 dict(id="Cd19", kind="clip", start="Just watch a few videos on", end="about basic poses,", tail=0.36,
      src=[stock("pexels-6447692-man-watching-online-yoga-lessons.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): over a man's hands as he watches an instruction video on his phone held sideways"),
 dict(id="Cd20", kind="clip", start="look in the mirror, and just", end="pictures like a professional.", tail=0.1,
      src=["B0438@0.5"], **DAN,
      note="Dan's own footage (first use): he sets his hands on his hips and opens into a front lat spread beside the pool, sunglasses on: posing like a professional"),
 dict(id="Gd17", kind="lt", start="At regular times of the year,", end="get your spray tan.", tail=0.0, topic="THE BOTTOM LINE",
      point="Save The Pro Tan For The Days That Count", parts=[["Save The Pro Tan", "At regular times of"], ["For The Days That Count", "for those critical times,"]]),
 dict(id="Cd21", kind="clip", start="At regular times of the year,", end="or do a cheaper option,", tail=0.0,
      src=[stock("pexels-7893015-shirtless-adult-man-at-the-beach.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): a man sits smiling in full sun on a beach, shoulders up, sunglasses pushed up on his head: tanning naturally"),
]
