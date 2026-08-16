# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: control.spec.ts >> differential functional control
- Location: python_app/avaliacao_prompts/resilience_campaigns/campaign_20260728_01/runtime/playwright/control.spec.ts:25:5

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  locator('[data-resilience-target="target-94e76973e20445c8"]')
Expected: 1
Received: 0
Timeout:  7000ms

Call log:
  - Expect "toHaveCount" with timeout 7000ms
  - waiting for locator('[data-resilience-target="target-94e76973e20445c8"]')
    18 × locator resolved to 0 elements
       - unexpected value "0"

```

# Page snapshot

```yaml
- generic [ref=e2]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - link "Tricentis Demo Web Shop" [ref=e6] [cursor=pointer]:
        - /url: /
        - img "Tricentis Demo Web Shop" [ref=e7]
      - list [ref=e10]:
        - listitem [ref=e11]:
          - link "Register" [ref=e12] [cursor=pointer]:
            - /url: /register
        - listitem [ref=e13]:
          - link "Log in" [ref=e14] [cursor=pointer]:
            - /url: /login
        - listitem [ref=e15]:
          - link "Shopping cart (0)" [ref=e16] [cursor=pointer]:
            - /url: /cart
            - generic [ref=e17]: Shopping cart
            - generic [ref=e18]: (0)
        - listitem [ref=e19]:
          - link "Wishlist (0)" [ref=e20] [cursor=pointer]:
            - /url: /wishlist
            - generic [ref=e21]: Wishlist
            - generic [ref=e22]: (0)
      - generic [ref=e24]:
        - status [ref=e25]
        - textbox [ref=e26]: Search store
        - button "Search" [ref=e27] [cursor=pointer]
    - list [ref=e29]:
      - listitem [ref=e30]:
        - link "Books" [ref=e31] [cursor=pointer]:
          - /url: /books
      - listitem [ref=e32]:
        - link "Computers" [ref=e33] [cursor=pointer]:
          - /url: /computers
      - listitem [ref=e34]:
        - link "Electronics" [ref=e35] [cursor=pointer]:
          - /url: /electronics
      - listitem [ref=e36]:
        - link "Apparel & Shoes" [ref=e37] [cursor=pointer]:
          - /url: /apparel-shoes
      - listitem [ref=e38]:
        - link "Digital downloads" [ref=e39] [cursor=pointer]:
          - /url: /digital-downloads
      - listitem [ref=e40]:
        - link "Jewelry" [ref=e41] [cursor=pointer]:
          - /url: /jewelry
      - listitem [ref=e42]:
        - link "Gift Cards" [ref=e43] [cursor=pointer]:
          - /url: /gift-cards
    - generic:
      - generic [ref=e44]:
        - generic [ref=e45]:
          - strong [ref=e47]: Categories
          - list [ref=e49]:
            - listitem [ref=e50]:
              - link "Books" [ref=e51] [cursor=pointer]:
                - /url: /books
            - listitem [ref=e52]:
              - link "Computers" [ref=e53] [cursor=pointer]:
                - /url: /computers
            - listitem [ref=e54]:
              - link "Electronics" [ref=e55] [cursor=pointer]:
                - /url: /electronics
            - listitem [ref=e56]:
              - link "Apparel & Shoes" [ref=e57] [cursor=pointer]:
                - /url: /apparel-shoes
            - listitem [ref=e58]:
              - link "Digital downloads" [ref=e59] [cursor=pointer]:
                - /url: /digital-downloads
            - listitem [ref=e60]:
              - link "Jewelry" [ref=e61] [cursor=pointer]:
                - /url: /jewelry
            - listitem [ref=e62]:
              - link "Gift Cards" [ref=e63] [cursor=pointer]:
                - /url: /gift-cards
        - generic [ref=e64]:
          - strong [ref=e66]: Manufacturers
          - list [ref=e68]:
            - listitem [ref=e69]:
              - link "Tricentis" [ref=e70] [cursor=pointer]:
                - /url: /tricentis
        - generic [ref=e71]:
          - strong [ref=e73]: Popular tags
          - generic [ref=e74]:
            - list [ref=e76]:
              - listitem [ref=e77]:
                - link "apparel" [ref=e78] [cursor=pointer]:
                  - /url: /producttag/4/apparel
              - listitem [ref=e79]:
                - link "awesome" [ref=e80] [cursor=pointer]:
                  - /url: /producttag/8/awesome
              - listitem [ref=e81]:
                - link "book" [ref=e82] [cursor=pointer]:
                  - /url: /producttag/10/book
              - listitem [ref=e83]:
                - link "camera" [ref=e84] [cursor=pointer]:
                  - /url: /producttag/13/camera
              - listitem [ref=e85]:
                - link "cell" [ref=e86] [cursor=pointer]:
                  - /url: /producttag/12/cell
              - listitem [ref=e87]:
                - link "compact" [ref=e88] [cursor=pointer]:
                  - /url: /producttag/9/compact
              - listitem [ref=e89]:
                - link "computer" [ref=e90] [cursor=pointer]:
                  - /url: /producttag/6/computer
              - listitem [ref=e91]:
                - link "cool" [ref=e92] [cursor=pointer]:
                  - /url: /producttag/3/cool
              - listitem [ref=e93]:
                - link "digital" [ref=e94] [cursor=pointer]:
                  - /url: /producttag/16/digital
              - listitem [ref=e95]:
                - link "jeans" [ref=e96] [cursor=pointer]:
                  - /url: /producttag/14/jeans
              - listitem [ref=e97]:
                - link "jewelry" [ref=e98] [cursor=pointer]:
                  - /url: /producttag/11/jewelry
              - listitem [ref=e99]:
                - link "nice" [ref=e100] [cursor=pointer]:
                  - /url: /producttag/1/nice
              - listitem [ref=e101]:
                - link "shirt" [ref=e102] [cursor=pointer]:
                  - /url: /producttag/5/shirt
              - listitem [ref=e103]:
                - link "shoes" [ref=e104] [cursor=pointer]:
                  - /url: /producttag/7/shoes
              - listitem [ref=e105]:
                - link "TCP" [ref=e106] [cursor=pointer]:
                  - /url: /producttag/19/tcp
            - link "View all" [ref=e108] [cursor=pointer]:
              - /url: /producttag/all
      - generic [ref=e109]:
        - generic [ref=e110]:
          - strong [ref=e112]: Newsletter
          - generic [ref=e114]:
            - text: "Sign up for our newsletter:"
            - textbox [ref=e116]
            - button "Subscribe" [ref=e118] [cursor=pointer]
        - generic [ref=e119]:
          - strong [ref=e121]: Community poll
          - generic [ref=e123]:
            - strong [ref=e124]: Do you like nopCommerce?
            - list [ref=e125]:
              - listitem [ref=e126]:
                - radio "Excellent" [ref=e127]
                - text: Excellent
              - listitem [ref=e128]:
                - radio "Good" [ref=e129]
                - text: Good
              - listitem [ref=e130]:
                - radio "Poor" [ref=e131]
                - text: Poor
              - listitem [ref=e132]:
                - radio "Very bad" [ref=e133]
                - text: Very bad
            - button "Vote" [ref=e135] [cursor=pointer]
      - generic [ref=e138]:
        - generic [ref=e139]:
          - generic [ref=e140]:
            - link [ref=e141] [cursor=pointer]:
              - /url: https://www.tricentis.com/speed/
            - link [ref=e142] [cursor=pointer]:
              - /url: https://academy.tricentis.com
            - img [ref=e143]
            - generic [ref=e144]: Speed | Tricentis
            - generic:
              - generic [ref=e145] [cursor=pointer]: Prev
              - generic [ref=e146] [cursor=pointer]: Next
            - img [ref=e148]
            - img [ref=e150]
            - img [ref=e152]
            - img [ref=e154]
            - img [ref=e156]
            - img [ref=e158]
            - img [ref=e160]
            - img [ref=e162]
            - img [ref=e164]
            - img [ref=e166]
            - img [ref=e168]
            - img [ref=e170]
            - img [ref=e172]
            - img [ref=e174]
            - img [ref=e176]
            - img [ref=e178]
            - img [ref=e180]
            - img [ref=e182]
            - img [ref=e184]
            - img [ref=e186]
            - img [ref=e188]
            - img [ref=e190]
            - img [ref=e192]
            - img [ref=e194]
            - img [ref=e196]
            - img [ref=e198]
            - img [ref=e200]
            - img [ref=e202]
            - img [ref=e204]
            - img [ref=e206]
            - img [ref=e208]
            - img [ref=e210]
          - generic [ref=e211]:
            - generic [ref=e212] [cursor=pointer]: "1"
            - generic [ref=e213] [cursor=pointer]: "2"
        - generic [ref=e214]:
          - heading "Welcome to our store" [level=2] [ref=e216]
          - generic [ref=e217]:
            - paragraph [ref=e218]: Welcome to the new Tricentis store!
            - paragraph [ref=e219]: Feel free to shop around and explore everything.
        - generic [ref=e220]:
          - strong [ref=e222]: Featured products
          - generic [ref=e224]:
            - link "Picture of $25 Virtual Gift Card" [ref=e226] [cursor=pointer]:
              - /url: /25-virtual-gift-card
              - img "Picture of $25 Virtual Gift Card" [ref=e227]
            - generic [ref=e228]:
              - heading "$25 Virtual Gift Card" [level=2] [ref=e229]:
                - link "$25 Virtual Gift Card" [ref=e230] [cursor=pointer]:
                  - /url: /25-virtual-gift-card
              - generic "912 review(s)" [ref=e231]
              - generic [ref=e234]:
                - generic [ref=e236]: "25.00"
                - button "Add to cart" [ref=e238] [cursor=pointer]
          - generic [ref=e240]:
            - link "Picture of 14.1-inch Laptop" [ref=e242] [cursor=pointer]:
              - /url: /141-inch-laptop
              - img "Picture of 14.1-inch Laptop" [ref=e243]
            - generic [ref=e244]:
              - heading "14.1-inch Laptop" [level=2] [ref=e245]:
                - link "14.1-inch Laptop" [ref=e246] [cursor=pointer]:
                  - /url: /141-inch-laptop
              - generic "1717 review(s)" [ref=e247]
              - generic [ref=e250]:
                - generic [ref=e252]: "1590.00"
                - button "Add to cart" [ref=e254] [cursor=pointer]
          - generic [ref=e256]:
            - link "Picture of Build your own cheap computer" [ref=e258] [cursor=pointer]:
              - /url: /build-your-cheap-own-computer
              - img "Picture of Build your own cheap computer" [ref=e259]
            - generic [ref=e260]:
              - heading "Build your own cheap computer" [level=2] [ref=e261]:
                - link "Build your own cheap computer" [ref=e262] [cursor=pointer]:
                  - /url: /build-your-cheap-own-computer
              - generic "926 review(s)" [ref=e263]
              - generic [ref=e266]:
                - generic [ref=e268]: "800.00"
                - button "Add to cart" [ref=e270] [cursor=pointer]
          - generic [ref=e272]:
            - link "Picture of Build your own computer" [ref=e274] [cursor=pointer]:
              - /url: /build-your-own-computer
              - img "Picture of Build your own computer" [ref=e275]
            - generic [ref=e276]:
              - heading "Build your own computer" [level=2] [ref=e277]:
                - link "Build your own computer" [ref=e278] [cursor=pointer]:
                  - /url: /build-your-own-computer
              - generic "434 review(s)" [ref=e279]
              - generic [ref=e282]:
                - generic [ref=e284]: "1200.00"
                - button "Add to cart" [ref=e286] [cursor=pointer]
          - generic [ref=e288]:
            - link "Picture of Build your own expensive computer" [ref=e290] [cursor=pointer]:
              - /url: /build-your-own-expensive-computer-2
              - img "Picture of Build your own expensive computer" [ref=e291]
            - generic [ref=e292]:
              - heading "Build your own expensive computer" [level=2] [ref=e293]:
                - link "Build your own expensive computer" [ref=e294] [cursor=pointer]:
                  - /url: /build-your-own-expensive-computer-2
              - generic "440 review(s)" [ref=e295]
              - generic [ref=e298]:
                - generic [ref=e300]: "1800.00"
                - button "Add to cart" [ref=e302] [cursor=pointer]
          - generic [ref=e304]:
            - link "Picture of Simple Computer" [ref=e306] [cursor=pointer]:
              - /url: /simple-computer
              - img "Picture of Simple Computer" [ref=e307]
            - generic [ref=e308]:
              - heading "Simple Computer" [level=2] [ref=e309]:
                - link "Simple Computer" [ref=e310] [cursor=pointer]:
                  - /url: /simple-computer
              - generic "399 review(s)" [ref=e311]
              - generic [ref=e314]:
                - generic [ref=e316]: "800.00"
                - button "Add to cart" [ref=e318] [cursor=pointer]
  - generic [ref=e319]:
    - generic [ref=e320]:
      - generic [ref=e321]:
        - heading "Information" [level=3] [ref=e322]
        - list [ref=e323]:
          - listitem [ref=e324]:
            - link "Sitemap" [ref=e325] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e326]:
            - link "Shipping & Returns" [ref=e327] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e328]:
            - link "Privacy Notice" [ref=e329] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e330]:
            - link "Conditions of Use" [ref=e331] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e332]:
            - link "About us" [ref=e333] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e334]:
            - link "Contact us" [ref=e335] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e336]:
        - heading "Customer service" [level=3] [ref=e337]
        - list [ref=e338]:
          - listitem [ref=e339]:
            - link "Search" [ref=e340] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e341]:
            - link "News" [ref=e342] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e343]:
            - link "Blog" [ref=e344] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e345]:
            - link "Recently viewed products" [ref=e346] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e347]:
            - link "Compare products list" [ref=e348] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e349]:
            - link "New products" [ref=e350] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e351]:
        - heading "My account" [level=3] [ref=e352]
        - list [ref=e353]:
          - listitem [ref=e354]:
            - link "My account" [ref=e355] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e356]:
            - link "Orders" [ref=e357] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e358]:
            - link "Addresses" [ref=e359] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e360]:
            - link "Shopping cart" [ref=e361] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e362]:
            - link "Wishlist" [ref=e363] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e364]:
        - heading "Follow us" [level=3] [ref=e365]
        - list [ref=e366]:
          - listitem [ref=e367]:
            - link "Facebook" [ref=e368] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e369]:
            - link "Twitter" [ref=e370] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e371]:
            - link "RSS" [ref=e372] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e373]:
            - link "YouTube" [ref=e374] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e375]:
            - link "Google+" [ref=e376] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e377]:
      - text: Powered by
      - link "nopCommerce" [ref=e378] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e379]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  1   | import fs from 'node:fs';
  2   | import { test, expect } from './fixture';
  3   | 
  4   | type Mutation = {
  5   |   mutation_id: string;
  6   |   target: {
  7   |     target_id: string;
  8   |     page_url: string;
  9   |     action: string;
  10  |     tag: string;
  11  |     attributes: Record<string, string>;
  12  |   };
  13  | };
  14  | 
  15  | function mutationFromEnvironment(): Mutation {
  16  |   const planPath = process.env.RESILIENCE_PLAN;
  17  |   const mutationId = process.env.RESILIENCE_MUTATION_ID;
  18  |   if (!planPath || !mutationId) throw new Error('RESILIENCE_PLAN and RESILIENCE_MUTATION_ID are required');
  19  |   const plan = JSON.parse(fs.readFileSync(planPath, 'utf8')) as { mutations: Mutation[] };
  20  |   const mutation = plan.mutations.find((candidate) => candidate.mutation_id === mutationId);
  21  |   if (!mutation) throw new Error(`Unknown mutation: ${mutationId}`);
  22  |   return mutation;
  23  | }
  24  | 
  25  | test('differential functional control', async ({ page }, testInfo) => {
  26  |   const mutation = mutationFromEnvironment();
  27  |   const pageErrors: string[] = [];
  28  |   const failedResponses: string[] = [];
  29  |   page.on('pageerror', (error) => pageErrors.push(error.message));
  30  |   page.on('response', (response) => {
  31  |     if (response.status() >= 500) failedResponses.push(`${response.status()} ${new URL(response.url()).pathname}`);
  32  |   });
  33  | 
  34  |   await page.goto(mutation.target.page_url);
  35  |   const target = page.locator(`[data-resilience-target="${mutation.target.target_id}"]`);
> 36  |   await expect(target).toHaveCount(1);
      |                        ^ Error: expect(locator).toHaveCount(expected) failed
  37  |   await expect(target).toBeVisible();
  38  | 
  39  |   const attributes = mutation.target.attributes;
  40  |   let supported = true;
  41  |   if (mutation.target.action === 'fill') {
  42  |     await target.fill(attributes.input_type === 'email' ? 'resilience@example.test' : 'resilience-probe');
  43  |   } else if (mutation.target.action === 'check') {
  44  |     await target.check();
  45  |   } else if (mutation.target.action === 'click') {
  46  |     if (mutation.target.tag === 'a' && attributes.href) {
  47  |       await target.click();
  48  |       await page.waitForLoadState('domcontentloaded');
  49  |     } else {
  50  |       await populateFormSafely(target);
  51  |       await target.click();
  52  |       await page.waitForTimeout(500);
  53  |     }
  54  |   } else {
  55  |     supported = false;
  56  |   }
  57  | 
  58  |   const observation = await page.evaluate(
  59  |     ({ targetId, supportedAction, errors, responses }) => {
  60  |       const normalized = (value: string | null | undefined) => (value || '').replace(/\s+/g, ' ').trim();
  61  |       const visibleText = (selector: string) =>
  62  |         Array.from(document.querySelectorAll(selector))
  63  |           .filter((element) => {
  64  |             const style = getComputedStyle(element);
  65  |             return style.visibility !== 'hidden' && style.display !== 'none';
  66  |           })
  67  |           .map((element) => normalized(element.textContent))
  68  |           .filter(Boolean)
  69  |           .sort();
  70  |       const marked = document.querySelector(`[data-resilience-target="${targetId}"]`) as HTMLInputElement | null;
  71  |       return {
  72  |         supported: supportedAction,
  73  |         pathname: location.pathname,
  74  |         search: location.search,
  75  |         heading: visibleText('h1').slice(0, 3),
  76  |         notifications: visibleText('#bar-notification, .validation-summary-errors, .result').slice(0, 5),
  77  |         targetPresent: Boolean(marked),
  78  |         targetValueChanged: marked ? Boolean(marked.value || marked.checked) : null,
  79  |         pageErrors: errors.slice().sort(),
  80  |         failedResponses: responses.slice().sort(),
  81  |       };
  82  |     },
  83  |     {
  84  |       targetId: mutation.target.target_id,
  85  |       supportedAction: supported,
  86  |       errors: pageErrors,
  87  |       responses: failedResponses,
  88  |     },
  89  |   );
  90  |   await testInfo.attach('resilience-control-observation', {
  91  |     body: JSON.stringify(observation, null, 2),
  92  |     contentType: 'application/json',
  93  |   });
  94  |   expect(observation.supported).toBe(true);
  95  |   expect(observation.pageErrors).toEqual([]);
  96  |   expect(observation.failedResponses).toEqual([]);
  97  | });
  98  | 
  99  | async function populateFormSafely(target: import('@playwright/test').Locator): Promise<void> {
  100 |   const form = target.locator('xpath=ancestor::form[1]');
  101 |   if ((await form.count()) !== 1) return;
  102 |   const seed = `${Date.now()}-${Math.floor(Math.random() * 1_000_000)}`;
  103 |   for (const input of await form.locator('input:visible:not([type=submit]):not([type=button]):not([type=hidden])').all()) {
  104 |     const type = (await input.getAttribute('type')) || 'text';
  105 |     if (['checkbox', 'radio'].includes(type)) {
  106 |       if (await input.isEnabled()) await input.check().catch(() => undefined);
  107 |       continue;
  108 |     }
  109 |     const name = ((await input.getAttribute('name')) || '').toLowerCase();
  110 |     let value = 'Resilience';
  111 |     if (type === 'email' || name.includes('email')) value = `resilience-${seed}@example.test`;
  112 |     else if (type === 'password' || name.includes('password')) value = 'Resilience123!';
  113 |     else if (name === 'q') value = 'Blue Jeans';
  114 |     else if (name.includes('zip')) value = '59000-000';
  115 |     else if (name.includes('phone')) value = '84999999999';
  116 |     if (await input.isEditable()) await input.fill(value);
  117 |   }
  118 |   for (const select of await form.locator('select:visible').all()) {
  119 |     const option = select.locator('option:not([value=""]):not([value="0"])').first();
  120 |     if ((await option.count()) === 1) await select.selectOption(await option.getAttribute('value') || undefined);
  121 |   }
  122 | }
  123 | 
  124 | 
```