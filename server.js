const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const fetch = require('node-fetch');

const app = express();
app.set('trust proxy', 1); // Required for Railway/proxied environments

// API Keys from environment variables
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const PRINTIFY_API_KEY = process.env.PRINTIFY_API_KEY;
const PRINTIFY_SHOP_ID = process.env.PRINTIFY_SHOP_ID;
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;

if (!ANTHROPIC_API_KEY || !GEMINI_API_KEY) {
  console.error('ERROR: Missing ANTHROPIC_API_KEY or GEMINI_API_KEY environment variables');
  process.exit(1);
}

// Initialize Stripe if configured
let stripeClient = null;
if (STRIPE_SECRET_KEY) {
  try {
    stripeClient = require('stripe')(STRIPE_SECRET_KEY);
  } catch (e) {
    console.warn('WARNING: stripe package not installed. Run: npm install stripe');
  }
}

// ============================================================
// PRODUCT CONFIG — fully populated from Printify catalog
//
// Canvas unframed: blueprint 937 (Matte Canvas Multi-Size), Jondo (105)
// Canvas framed:   blueprint 944 (Matte Canvas Framed),     Jondo (105), Black frame
//   Note: framed not available in 8×10 — smallest framed is 11×14
// Poster:          blueprint 282 (Matte Vertical Posters),  Sensaria (2)
//   Note: smallest available size is 9×11 (≈8×10)
// Keychain acrylic: blueprint 2675 (Single-Sided Charm),    Printdoors (332)
// Keychain metal:   blueprint 790  (Rectangle Photo Keyring), Imagine Your Photos (59)
//
// Each variant carries its own blueprintId/printProviderId so the
// webhook handler can build the Printify order without extra lookups.
// ============================================================
const PRODUCT_CONFIG = {
  canvas: {
    variants: {
      '8x10_unframed':  { blueprintId: 937, printProviderId: 105, variantId: 95212,  price: 3400 },
      '11x14_unframed': { blueprintId: 937, printProviderId: 105, variantId: 82229,  price: 4200 },
      '16x20_unframed': { blueprintId: 937, printProviderId: 105, variantId: 82231,  price: 5400 },
      '18x24_unframed': { blueprintId: 937, printProviderId: 105, variantId: 82232,  price: 6300 },
      '24x36_unframed': { blueprintId: 937, printProviderId: 105, variantId: 82235,  price: 7900 },
      '11x14_framed':   { blueprintId: 944, printProviderId: 105, variantId: 88291,  price: 7500 },
      '16x20_framed':   { blueprintId: 944, printProviderId: 105, variantId: 88293,  price: 8700 },
      '18x24_framed':   { blueprintId: 944, printProviderId: 105, variantId: 88294,  price: 9600 },
      '24x36_framed':   { blueprintId: 944, printProviderId: 105, variantId: 88297,  price: 11200 },
    },
  },
  poster: {
    variants: {
      '9x11':  { blueprintId: 282, printProviderId: 2, variantId: 62103,  price: 1800 },
      '11x14': { blueprintId: 282, printProviderId: 2, variantId: 43135,  price: 2700 },
      '12x16': { blueprintId: 282, printProviderId: 2, variantId: 101110, price: 2400 },
      '18x24': { blueprintId: 282, printProviderId: 2, variantId: 43144,  price: 4400 },
      '24x36': { blueprintId: 282, printProviderId: 2, variantId: 43150,  price: 5200 },
    },
  },
  keychain: {
    variants: {
      'acrylic_small': { blueprintId: 2675, printProviderId: 332, variantId: 147952, price: 900 },
      'acrylic_large': { blueprintId: 2675, printProviderId: 332, variantId: 147953, price: 1200 },
      'metal':         { blueprintId: 790,  printProviderId: 59,  variantId: 74997,  price: 2500 },
    },
  },
};

// ============================================================
// MIDDLEWARE
// Stripe webhook MUST receive raw body — register its route
// before express.json() so the global parser doesn't consume it.
// ============================================================
app.use(cors());

// ============================================================
// ENDPOINT: Stripe webhook (raw body, no rate-limit)
// ============================================================
app.post('/api/stripe/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  if (!stripeClient) {
    return res.status(503).json({ error: 'Stripe not configured' });
  }
  if (!STRIPE_WEBHOOK_SECRET) {
    return res.status(503).json({ error: 'STRIPE_WEBHOOK_SECRET not configured' });
  }

  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripeClient.webhooks.constructEvent(req.body, sig, STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).json({ error: `Webhook Error: ${err.message}` });
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const { imageId, imagePreviewUrl, productType, size, framed } = session.metadata || {};
    const email = session.customer_details?.email;
    const shipping = session.shipping_details?.address;

    console.log(`Order completed: ${productType} ${size}${framed === 'true' ? ' framed' : ''} for ${email}`);

    // Use previewUrl from upload response; fall back to reconstructed URL for old orders
    const imageSrc = imagePreviewUrl || `https://images-api.printify.com/${imageId}`;

    if (PRINTIFY_API_KEY && PRINTIFY_SHOP_ID && imageSrc && productType && size) {
      const framedBool = framed === 'true';
      const variantKey = productType === 'canvas'
        ? `${size}_${framedBool ? 'framed' : 'unframed'}`
        : size;
      const variant = PRODUCT_CONFIG[productType]?.variants[variantKey];

      if (!variant || !variant.variantId) {
        console.warn(`Printify variant not configured for ${productType}/${variantKey} — order NOT submitted to Printify`);
      } else {
        try {
          const orderPayload = {
            external_id: session.id,
            line_items: [
              {
                blueprint_id: variant.blueprintId,
                print_provider_id: variant.printProviderId,
                variant_id: variant.variantId,
                print_areas: {
                  front: [{ src: '', position: 'front', scale: 1, angle: 0 }],
                },
                quantity: 1,
              },
            ],
            shipping_method: 1,
            send_shipping_notification: true,
            address_to: {
              first_name: session.shipping_details?.name?.split(' ')[0] || '',
              last_name: session.shipping_details?.name?.split(' ').slice(1).join(' ') || '',
              email: email || '',
              phone: '',
              country: shipping?.country || 'US',
              region: shipping?.state || '',
              address1: shipping?.line1 || '',
              address2: shipping?.line2 || '',
              city: shipping?.city || '',
              zip: shipping?.postal_code || '',
            },
          };

          orderPayload.line_items[0].print_areas.front[0].src = imageSrc;
          console.log(`Printify order image src: ${imageSrc}`);

          const printifyRes = await fetch(
            `https://api.printify.com/v1/shops/${PRINTIFY_SHOP_ID}/orders.json`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${PRINTIFY_API_KEY}`,
              },
              body: JSON.stringify(orderPayload),
            }
          );
          const printifyData = await printifyRes.json();
          if (!printifyRes.ok) {
            console.error('Printify order creation failed:', JSON.stringify(printifyData));
          } else {
            console.log('Printify order created:', printifyData.id);
          }
        } catch (err) {
          console.error('Printify order creation error:', err);
        }
      }
    } else if (!PRINTIFY_API_KEY || !PRINTIFY_SHOP_ID) {
      console.warn('Printify not configured — order recorded but not sent to Printify');
    }
  }

  res.json({ received: true });
});

// Global JSON parser (after webhook route so it doesn't consume raw bytes)
app.use(express.json({ limit: '10mb' }));

// Rate limiting: 10 requests per minute per IP
const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  message: 'Too many requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Separate generous limiter for checkout (not an abuse vector)
const checkoutLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 30,
  message: 'Too many requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use(limiter);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Public config for frontend (publishable key is safe to expose)
app.get('/api/config', (req, res) => {
  res.json({
    stripePublishableKey: process.env.STRIPE_PUBLISHABLE_KEY || '',
  });
});

// ============================================================
// ENDPOINT 1: Photo check (Claude Haiku)
// ============================================================
app.post('/api/check-photo', async (req, res) => {
  try {
    const { photoBase64, photoMime } = req.body;

    if (!photoBase64 || !photoMime) {
      return res.status(400).json({ error: 'Missing photoBase64 or photoMime' });
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 16,
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'image',
                source: {
                  type: 'base64',
                  media_type: photoMime,
                  data: photoBase64,
                },
              },
              {
                type: 'text',
                text: `Review this photo for a fitness transformation app and reply with exactly one of these codes:

OK — the person is shirtless, or wearing a sports bra, bikini, swimsuit, swimwear, athletic wear, or underwear-style clothing that clearly exposes their bare midsection/torso. This includes beach photos, pool photos, gym photos, and mirror selfies. Even glamorous or professional-looking photos are OK as long as the clothing is standard swimwear or athletic wear and the pose is not explicitly sexual.

SUGGESTIVE — the photo is clearly sexually provocative: lingerie specifically intended to be erotic (not athletic/swimwear), explicitly sexual posing (spread legs, simulated sex acts), or nudity beyond what would be seen at a beach or gym.

CLOTHED — the person is fully or mostly clothed and their torso is not clearly visible.

EXPLICIT — the image contains pornographic or sexually explicit content.

ILLEGAL — the image shows visible illegal activity such as drug use, weapons, or similar.

MINOR — the subject appears to be under 18 years old.

When in doubt between OK and SUGGESTIVE, choose OK. Only flag SUGGESTIVE if the photo is clearly inappropriate for a fitness context.

Reply with only the single code word, nothing else.`,
              },
            ],
          },
        ],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error?.message || 'Claude API error',
      });
    }

    const code = data?.content?.[0]?.text?.trim().toUpperCase() || 'OK';

    res.json({ code });
  } catch (err) {
    console.error('Photo check error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// ENDPOINT 2: Generate prompt (Claude Sonnet)
// ============================================================
app.post('/api/generate-prompt', async (req, res) => {
  try {
    const { systemPrompt, userJson } = req.body;

    if (!systemPrompt || !userJson) {
      return res.status(400).json({ error: 'Missing systemPrompt or userJson' });
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 2048,
        temperature: 0.4,
        system: systemPrompt,
        messages: [
          {
            role: 'user',
            content: userJson,
          },
        ],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error?.message || 'Claude API error',
      });
    }

    const prompt = data?.content
      ?.filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('\n')
      .trim();

    if (!prompt) {
      return res.status(400).json({
        error: 'Claude returned no text. The prompt may have been blocked by safety filters.',
      });
    }

    res.json({ prompt });
  } catch (err) {
    console.error('Prompt generation error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// ENDPOINT 3: Generate image (Gemini)
// ============================================================
app.post('/api/generate-image', async (req, res) => {
  try {
    const { prompt, photoBase64, photoMime } = req.body;

    if (!prompt || !photoBase64 || !photoMime) {
      return res.status(400).json({
        error: 'Missing prompt, photoBase64, or photoMime',
      });
    }

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=${encodeURIComponent(GEMINI_API_KEY)}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [
              { text: prompt },
              {
                inline_data: {
                  mime_type: photoMime,
                  data: photoBase64,
                },
              },
            ],
          },
        ],
        generationConfig: {
          responseModalities: ['TEXT', 'IMAGE'],
        },
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error?.message || 'Image generation error',
      });
    }

    const parts = data?.candidates?.[0]?.content?.parts || [];
    const imgPart = parts.find((p) => p.inline_data || p.inlineData);

    if (!imgPart) {
      const textBlock = parts.find((p) => p.text)?.text;
      return res.status(400).json({
        error:
          textBlock ||
          'Image generation was blocked — this is usually caused by a photo that is too suggestive or explicit. For best results, use a simple shirtless photo (men) or sports bra / swimsuit photo (women) with neutral pose and lighting.',
      });
    }

    const imageBase64 = (imgPart.inline_data || imgPart.inlineData).data;

    res.json({ imageBase64 });
  } catch (err) {
    console.error('Image generation error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// ENDPOINT 4: Upload image to Printify
// ============================================================
app.post('/api/printify/upload-image', checkoutLimiter, async (req, res) => {
  if (!PRINTIFY_API_KEY) {
    return res.status(503).json({ error: 'Printify not configured. Add PRINTIFY_API_KEY to environment variables.' });
  }

  try {
    const { imageBase64, fileName } = req.body;
    if (!imageBase64 || !fileName) {
      return res.status(400).json({ error: 'Missing imageBase64 or fileName' });
    }

    const response = await fetch('https://api.printify.com/v1/uploads/images.json', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${PRINTIFY_API_KEY}`,
      },
      body: JSON.stringify({
        file_name: fileName,
        contents: imageBase64,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      console.error('Printify upload error:', JSON.stringify(data));
      return res.status(response.status).json({ error: data?.message || 'Printify upload failed' });
    }

    res.json({ imageId: data.id, previewUrl: data.preview_url });
  } catch (err) {
    console.error('Printify upload error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// ENDPOINT 5: Create Stripe Embedded Checkout session
// ============================================================
app.post('/api/stripe/create-checkout', checkoutLimiter, async (req, res) => {
  if (!stripeClient) {
    return res.status(503).json({ error: 'Stripe not configured. Add STRIPE_SECRET_KEY to environment variables.' });
  }

  try {
    const { productType, size, framed, priceInCents, imageId, imagePreviewUrl, productLabel, returnUrl } = req.body;
    if (!productType || !size || !priceInCents || !returnUrl) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const displayName = `${productLabel || productType} — ${size}${framed ? ' (Framed)' : ''}`;

    const session = await stripeClient.checkout.sessions.create({
      ui_mode: 'embedded',
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: displayName,
              description: 'Your AI-generated future self, printed and shipped to you.',
            },
            unit_amount: priceInCents,
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      return_url: returnUrl,
      shipping_address_collection: {
        allowed_countries: [
          'US', 'CA', 'GB', 'AU', 'DE', 'FR', 'ES', 'IT', 'NL', 'SE', 'NO', 'DK',
          'FI', 'AT', 'BE', 'CH', 'IE', 'NZ', 'JP', 'SG', 'HK', 'MX', 'BR',
        ],
      },
      automatic_tax: { enabled: false },
      metadata: {
        imageId: imageId || '',
        imagePreviewUrl: imagePreviewUrl || '',
        productType,
        size,
        framed: String(!!framed),
      },
    });

    res.json({ clientSecret: session.client_secret });
  } catch (err) {
    console.error('Stripe checkout creation error:', err);
    res.status(500).json({ error: err.message || 'Internal server error' });
  }
});

// ============================================================
// ENDPOINT 6: Check Stripe session status (after redirect back)
// ============================================================
app.get('/api/stripe/session-status', async (req, res) => {
  if (!stripeClient) {
    return res.status(503).json({ error: 'Stripe not configured' });
  }

  try {
    const { session_id } = req.query;
    if (!session_id) {
      return res.status(400).json({ error: 'Missing session_id' });
    }

    const session = await stripeClient.checkout.sessions.retrieve(session_id);
    res.json({ status: session.status });
  } catch (err) {
    console.error('Session status error:', err);
    res.status(500).json({ error: err.message || 'Internal server error' });
  }
});

// ============================================================
// STATIC FILES & FALLBACK
// ============================================================
const path = require('path');
app.use(express.static(path.join(__dirname)));

// Serve index.html for all non-API routes (SPA fallback)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Abs By AI backend running on port ${PORT}`);
});
