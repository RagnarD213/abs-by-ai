const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, HeadingLevel, AlignmentType,
} = require('docx');

const MEDIA = path.join(__dirname, 'outline_x', 'word', 'media');

// display sizes (px @96dpi), preserving aspect ratio
const IMG = {
  'image1.jpg': { w: 864, h: 1184 },
  'image2.png': { w: 675, h: 900 },
  'image3.jpg': { w: 980, h: 801 },
  'image4.jpg': { w: 1374, h: 2048 },
  'image5.jpg': { w: 1638, h: 2048 },
  'image6.jpg': { w: 1639, h: 2048 },
};

function img(name, displayW) {
  const { w, h } = IMG[name];
  const dw = displayW, dh = Math.round((h / w) * displayW);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 240 },
    children: [new ImageRun({
      type: name.endsWith('.png') ? 'png' : 'jpg',
      data: fs.readFileSync(path.join(MEDIA, name)),
      transformation: { width: dw, height: dh },
    })],
  });
}

function cue(text) {
  return new Paragraph({
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, color: '7A6A2E', size: 22, font: 'Arial' })],
  });
}

function spoken(text) {
  return new Paragraph({
    spacing: { before: 120, after: 120, line: 320 },
    children: [new TextRun({ text, size: 28, font: 'Arial' })],
  });
}

function note(text) {
  return new Paragraph({
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, italics: true, color: '666666', size: 20, font: 'Arial' })],
  });
}

function heading(text, level) {
  return new Paragraph({ heading: level, spacing: { before: 360, after: 160 }, children: [new TextRun({ text })] });
}

const children = [
  heading('Abs By AI — Ads Batch 1: Finalized Teleprompter Scripts', HeadingLevel.HEADING_1),
  note('Spoken words are in regular text — read these on the teleprompter. Bracketed gold lines are edit/visual cues — do not read them. Images show the exact asset for each cue.'),

  heading('AD 1 — How AI Got Me Abs', HeadingLevel.HEADING_2),
  note('~610 spoken words ≈ 3:45–4:15 at normal pace.'),

  cue('[SKIP STOPPER — OPEN TIGHT ON POSTER, ZOOM IN]'),
  img('image1.jpg', 300),
  spoken('This picture got me abs.'),
  cue('[ZOOM OUT TO DAN TALKING, HOLDING POSTER]'),
  spoken("And it's not even real."),
  cue('[RECORD SCRATCH SOUND EFFECT]'),

  cue('[BELIEVABLE PROMISE]'),
  spoken('I generated this picture with AI back when I was two hundred pounds.'),
  cue('[SHOW BEFORE PICTURE ON SCREEN]'),
  img('image2.png', 300),
  spoken('I made it my phone lockscreen, and I looked at it every single day for more than a year.'),
  cue('[B-ROLL: PHONE LOCKSCREEN]'),
  spoken("And this is where I'm at today."),
  cue('[SHOW 3–4 BEST PHOTO SHOOT PICTURES]'),
  img('image3.jpg', 340),
  img('image6.jpg', 300),
  img('image4.jpg', 300),
  img('image5.jpg', 300),
  spoken("In today's episode, I'm going to show you how I got limitless motivation to work out, to eat healthy, and to do what I needed to do to lose my belly fat and get six-pack abs. And I'll show you how you can generate a goal picture of yourself with abs — for free."),

  cue('[CONDITIONING CONTENT 1]'),
  spoken("Let's be honest. You already know that if you had the motivation to work out regularly and eat clean, you'd lose your belly fat. The knowledge isn't the problem. The problem is that finding that motivation is really, really hard when you're living a busy, stressful life."),
  spoken("Visualizing your goal is one of the most powerful ways to motivate yourself — and to attract the body you want into your life. This isn't woo-woo stuff. Fitness models and bodybuilders have done this for decades. Some of them would literally photoshop their own face onto a picture of their dream physique and stare at it every day."),
  cue("[SHOW RIDICULOUS CRUDE PHOTOSHOP: AVERAGE GUY'S FACE ON FITNESS MODEL BODY]"),
  spoken("The problem is — it looked ridiculous. Deep down, you knew that wasn't really you."),
  spoken('But now, AI has changed the game. With AI, you can create a picture of YOURSELF — your face, your body — with the ripped six-pack abs you\'ve always wanted.'),
  cue('[SHOW LABELED ABS BY AI BEFORE + AI-GENERATED FUTURE AFTER]'),
  spoken("And once you see yourself with abs — the real you, not some fitness model — everything changes. You realize how amazing you'd look if you lost your stomach fat. You realize how much better your life would be. And you're filled with motivation to make your dream body a reality."),

  cue('[CTA 1]'),
  spoken('And right now, you can generate an AI image of yourself with ripped six-pack abs, completely free. Just tap the button below to see yourself with abs.'),

  cue('[CONDITIONING CONTENT 2]'),
  spoken("Listen — losing your belly fat and getting six-pack abs changes your whole life. You're more attractive to women. Men respect you more. You feel better, you've got more energy, your health improves — and you'll probably live longer too."),
  spoken("And here's the truth. If you're not working out at least five days a week and eating healthy right now, you don't need more knowledge. You need the motivation to execute what you already know."),
  spoken("That's exactly the situation I was in a few years ago."),
  cue('[SHOW BEFORE PICTURE AGAIN]'),
  img('image2.png', 300),
  spoken('I wanted to get my abs back so bad. But I just could not find the motivation to hit the gym or eat healthy as a thirty-eight-year-old dad living a busy, stressful life.'),
  spoken('Nothing worked to motivate me — until I generated this picture and made it my phone lockscreen.'),
  spoken('I looked at it many times a day, every single day. And it made me realize: this is how I\'m supposed to look. This is how I NEED to look.'),
  spoken("And that's what gave me the fire to train hard and consistently. To meal prep every week. To track my calories. To do the simple but difficult things that you have to do to lose your belly fat."),
  spoken("This one AI picture helped me so much that I created an app that helps other guys generate a picture of their fitness goal for free. It's designed purely for making fitness transformation images of men like you — so it's far superior to making these images with ChatGPT or any general-purpose AI."),

  cue('[CTA 2]'),
  spoken('To generate an image of yourself with abs for free, tap the button below.'),

  cue("[PRODUCT DETAIL — IT'S A FULL PROGRAM, NOT JUST A PICTURE]"),
  spoken("And here's the part most people don't expect. The picture is just step one."),
  spoken('Once you generate an image of yourself with abs, we build you a personalized AI fitness plan to make it real.'),
  spoken('Our AI scans your current picture to assess your body fat percentage and your training status. Then it scans your goal picture to see exactly where you want to be. And then it builds you a customized workout and nutrition plan — personalized just for you and your goal.'),
  spoken('Your workout plan works around your injuries, targets your lagging body parts, and uses the specific equipment you actually have. Your nutrition plan is calibrated exactly for your goal — and it\'s built around the healthy foods you like best, so you can actually stick to it.'),
  spoken('Generating an image of yourself with abs is the first step. After that, our personalized AI fitness program helps you make it real.'),

  cue('[CTA 3]'),
  spoken('To get started losing your belly fat and getting six-pack abs — tap the button below.'),

  cue('[END]'),

  heading('Production notes', HeadingLevel.HEADING_2),
  note('"Tap the button below" is speakable for any CTA button text. If the final Google Ads button is specific ("See My Abs" / "Try Free"), you can name it on CTA 2 or 3 for reinforcement.'),
  note('When the before/after example appears on screen (Conditioning 1), keep the "AI-GENERATED" tag burned onto the after image — same treatment as "The Upload" ad. Dan\'s real photo-shoot pictures need no label; the goal image does.'),
];

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 } } },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(path.join(__dirname, 'abs-by-ai ads batch 1 finalized scripts for teleprompter.docx'), buf);
  console.log('written', buf.length, 'bytes');
});
