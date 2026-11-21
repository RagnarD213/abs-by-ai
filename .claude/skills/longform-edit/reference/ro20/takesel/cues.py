"""output times of the excuse-voice lines and the picture cues: each is found by a phrase in words_out.json"""
import json, re
W = "/Volumes/Extreme/_edit_work/ro20"; WO = json.load(open(f"{W}/words_out.json"))
n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower()); T = [n(w["w"]) for w in WO]
def ms(t): t = int(t); return f"{t//60}:{t%60:02d}"
def at(phrase, after=0.0, nwords=None):
    toks = [n(x) for x in phrase.split() if n(x)]
    for i in range(len(T)):
        if WO[i]["t0"] < after: continue
        k = i; ok = True
        for t in toks:
            acc = ""
            while k < len(T) and len(acc) < len(t): acc += T[k]; k += 1
            if acc != t: ok = False; break
        if ok:
            j = k
            if nwords: j = min(len(WO), i+nwords)
            else:
                while j < len(WO) and WO[j-1]["w"][-1:] not in ".?!": j += 1
            return WO[i]["t0"], " ".join(w["w"] for w in WO[i:j])
    raise SystemExit("not found: " + phrase)
EXC = [("They think I need to make", 34), ("hmm, my husband's getting", 13), ("oh, my husband just doesn't", 36), ("oh, my man has a six-pack", 13), ("oh, my man is so funny", 22),
 ("oh I don't need to spend more money on my health", 19), ("oh, well I'm just not going to spend that hour", 27), ("oh I can just deal with average", 21),
 ("maybe I won't be around", 24), ("I'm in my 20s or 30s", 26), ("oh well damn that's easy", 34), ("oh, Dan, I don't have the money for a personal trainer", 20), ("well, I need some entertainment", 5),
 ("oh, I don't have the money to get in shape, Dan", 19), ("oh, well, I just need a treat", 12), ("I need a vacation. I deserve", 11), ("I can't afford healthy food, Dan", 26),
 ("oh, Dan, I don't have the money for $30", 15), ("oh, Dan, I can't afford $30", 9), ("oh, I can't afford 400 bucks", 18), ("you can't afford it, you can't afford it", 8), ("oh I got such a busy schedule", 17)]
PIC = [("So let's say you're applying for a new job", "job interview"), ("over 70% of people", "70% meet on dating apps"), ("they swipe left on you", "swipe left"), ("top 10% best looking", "top 10% of guys"), ("it 10x my matches", "10x matches"), ("The bottom 80%", "bottom 80% get nothing"),
 ("I work out an hour every morning", "his hour every morning"), ("you hire a personal chef to make you a salad", "meal prep, chef, salad"), ("rather than going to Taco Bell", "Taco Bell"), ("I know people my age, 40 years old", "40-year-olds at the doctor, prescriptions, arthritis"),
 ("then you have to go to drive to pick up that prescription", "pharmacy pickup"), ("go to a psychologist", "therapy every week"), ("psychiatric medication and then", "psychiatric medication"), ("especially in the United States", "US health insurance"),
 ("The lawyer who's working 100 hours", "lawyer, doctor, 100 hours a week"), ("they get diabetes or they become obese", "diabetes, obesity, heart, cancer"), ("Insulin injections all the time", "insulin"), ("You have to get an ambulance", "ambulance: 5, 10, 15 grand a trip"),
 ("He had to get a toe amputated", "amputated toe"), ("injections into his eyes", "eye injections"), ("stop putting that money in your 401k", "401k"), ("both sets of grandparents", "family inheritance lawsuit"), ("Hard vacations where", "walking vacation"),
 ("Days at the pool", "pool, paddle board, beach"), ("Having that gigantic house", "big house, stairs"), ("rent on a luxury crib", "luxury rent vs basic"), ("a car payment on a very basic car", "basic car"), ("going to bars and clubs", "bars and clubs"),
 ("spending 100, 200, $300 per week", "$100 to $300 a week"), ("those $20 drinks in the club", "$20 drinks"), ("a 30 rack of beer", "30 rack of beer"), ("credit card statement", "credit card statement, restaurants"), ("five-star Google review", "5-star Google review"),
 ("much more butter", "butter, sugar in restaurant food"), ("take a picture of it with our phone", "Abs By AI meal photo tracking"), ("the chips, the candy", "chips, candy, soda"), ("I fast until 2pm", "fasting until 2 pm"), ("2 or 3 pounds of fat", "2 to 3 lb a vacation week"),
 ("pancakes and whatever", "pancakes, 5 to 6 lb a week"), ("frees up $5,000", "$5,000 to $15,000 a vacation"), ("your subscriptions, your Netflix", "Netflix, car payment, clothes, dates"), ("living in the cardboard box", "cardboard box"), ("is a yoga mat", "yoga mat, push-up handles, light dumbbells, kettlebell, ab wheel, jump rope"),
 ("for under $100", "under $100"), ("very cheaply at Costco", "Costco membership"), ("chicken thighs or drumsticks", "chicken, rice, Brussels sprouts, broccoli, cabbage"), ("You can do rice and beans", "rice and beans"), ("wild-caught Alaskan sockeye salmon", "sockeye salmon $20/lb vs chicken thighs $3/lb"),
 ("is the filet mignon", "filet mignon $25 to $30/lb at Costco"), ("my $30 a pound tuna", "tuna $30/lb"), ("shrimp and lobster tail", "shrimp, lobster tail, steak"), ("grass fed beef", "grass-fed beef"), ("omega-3 fatty acids to omega-6", "omega-3 to omega-6"),
 ("Salmon or putting that money in the stock market", "salmon vs stock market"), ("10 year old broken mattress", "sagging 10-year-old mattress"), ("two or three percent", "2 to 3% better sleep, $2,000 to $3,000"), ("is the Purple Mattress", "Purple Mattress"), ("because it's a gel grid", "gel grid vs springs"),
 ("This mattress can last 20 years", "20 years vs 7"), ("there's a lot of sweat going into", "what soaks into a mattress, bacteria, mold"), ("a leg press machine", "leg press, leg curl, full dumbbell rack"), ("even though I spent $20,000", "his $20,000 home gym"), ("a bodybuilding gym about 10 minutes", "his bodybuilding gym"),
 ("bodybuilders and fitness models", "bodybuilders, fitness models"), ("for $80, $100, $120 a month", "$80 to $120 a month"), ("I personally wear the Oura Ring", "Oura Ring"), ("a mandatory 7 per month", "$7 a month subscription"), ("The Whoop is a thin wearable", "Whoop"),
 ("track your sleep with the Apple Watch", "Apple Watch"), ("a silicon band", "silicone band slipping"), ("the finger is significantly more accurate", "finger vs wrist study"), ("GLP, weight loss medication", "tirzepatide, retatrutide, Ozempic"), ("400 bucks a month", "$400 a month"),
 ("I plan on staying on Zepbound", "Zepbound for life"), ("that $400 per month", "$400 saved on restaurants, junk food, alcohol"), ("Cash out that college account", "college fund, 401k"), ("TRT. Now, I haven't started", "TRT"), ("Higher testosterone men", "testosterone and income"),
 ("I personally take 10 supplements", "his 10 supplements"), ("is a fish oil or Omega supplement", "fish oil: 100 for $20 to $30"), ("your heart health, your brain health", "heart, brain, joints, hair, skin, nails"), ("about 70% of the U.S", "70% vitamin D deficient"), ("the Athletic Greens vitamin D", "Athletic Greens liquid vitamin D and dropper (he promises it on screen)"),
 ("about 50% of the US population", "50% magnesium deficient"), ("is magnesium glycinate", "magnesium glycinate before bed"), ("the big three", "fish oil, vitamin D, magnesium"), ("is a home gym. Now you can build", "home gym for $10,000"), ("between 20 and $30,000", "$20,000 to $30,000 separate building"),
 ("a very big shed in my backyard", "his backyard shed"), ("I put in insulation", "insulation, air conditioning, rubber floor"), ("back during COVID", "COVID gym closures"), ("You can work out shirtless", "shirtless, own music on speakers"), ("A meal prep service or even better", "meal prep service, personal chef"),
 ("called Clean Eats", "Clean Eats, Austin"), ("For about $120 per week", "$120 a week vs $80 to $120 cooking"), ("each meal is 300 to 500 calories", "300 to 500 calorie meals"), ("a full-time personal chef", "full-time personal chef"), ("they don't have a maid", "maid, laundry service, dishes"),
 ("a human personal trainer or nutritionist", "human trainer and nutritionist"), ("in that top 1%", "top 1% trainer"), ("paying 200, 300, $400 an hour", "$200 to $400 an hour"), ("red light therapy machines", "red light therapy"), ("exotic peptides like BPC157", "BPC-157, growth hormone"),
 ("check out Brian Johnson's YouTube channel", "Bryan Johnson's channel"), ("investing $500 to $1000 in your health", "$500 to $1,000 a month"), ("you can upload a picture of yourself", "absbyai.com upload and result"), ("We have an AI personal trainer", "AI trainer, AI nutritionist, AI sleep coach")]
L = ["# RO-20 cues (companion to take_map_notes.md)", "", "Output times are on the cut timeline (shots.json).", "", "## Voices: excuse voice and imitations", ""]
exc = []
for ph, nw in EXC:
    t, txt = at(ph, 0, nw); exc.append((t, txt)); L.append(f"- {ms(t)} {txt}")
L += ["", "## Picture cues", ""]
pic = []; last = 0.0
for ph, lab in PIC:
    t, txt = at(ph); pic.append((t, lab)); L.append(f"- {ms(t)} [{lab}] {txt}")
    if t < last - 1: print("ORDER?", ph, ms(t))
    last = t
open(f"{W}/picture_cues.md", "w").write("\n".join(L) + "\n")
print("EXC: " + "; ".join(f"{ms(t)} {' '.join(x.split()[:5])}" for t, x in exc))
print("PIC: " + "; ".join(f"{ms(t)} {lab}" for t, lab in pic))
