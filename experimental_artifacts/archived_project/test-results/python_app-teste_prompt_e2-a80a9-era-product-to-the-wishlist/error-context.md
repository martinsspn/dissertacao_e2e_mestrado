# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: python_app/teste_prompt_e2e_semantico/generated_tests/semantic_prompt/suite_adicionar_wishlist_sem_gerador.spec.ts >> adding a Camera product to the wishlist
- Location: python_app/teste_prompt_e2e_semantico/generated_tests/semantic_prompt/suite_adicionar_wishlist_sem_gerador.spec.ts:3:5

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.fill: Test timeout of 30000ms exceeded.
Call log:
  - waiting for getByRole('textbox', { name: 'Search store' })

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
          - link "gabrieltestee2e@gmail.com" [ref=e12] [cursor=pointer]:
            - /url: /customer/info
        - listitem [ref=e13]:
          - link "Log out" [ref=e14] [cursor=pointer]:
            - /url: /logout
        - listitem [ref=e15]:
          - link "Shopping cart (1)" [ref=e16] [cursor=pointer]:
            - /url: /cart
            - generic [ref=e17]: Shopping cart
            - generic [ref=e18]: (1)
        - listitem [ref=e19]:
          - link "Wishlist (3)" [ref=e20] [cursor=pointer]:
            - /url: /wishlist
            - generic [ref=e21]: Wishlist
            - generic [ref=e22]: (3)
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
            - img [ref=e147]
            - img [ref=e148]
            - img [ref=e149]
            - img [ref=e150]
            - img [ref=e151]
            - img [ref=e152]
            - img [ref=e153]
            - img [ref=e154]
            - img [ref=e155]
            - img [ref=e156]
            - img [ref=e157]
            - img [ref=e158]
            - img [ref=e159]
            - img [ref=e160]
            - img [ref=e161]
            - img [ref=e162]
            - img [ref=e163]
            - img [ref=e164]
            - img [ref=e165]
            - img [ref=e166]
            - img [ref=e167]
            - img [ref=e168]
            - img [ref=e169]
            - img [ref=e170]
            - img [ref=e171]
            - img [ref=e172]
            - img [ref=e173]
            - img [ref=e174]
            - img [ref=e175]
            - img [ref=e176]
            - img [ref=e177]
            - img [ref=e178]
          - generic [ref=e179]:
            - generic [ref=e180] [cursor=pointer]: "1"
            - generic [ref=e181] [cursor=pointer]: "2"
        - generic [ref=e182]:
          - heading "Welcome to our store" [level=2] [ref=e184]
          - generic [ref=e185]:
            - paragraph [ref=e186]: Welcome to the new Tricentis store!
            - paragraph [ref=e187]: Feel free to shop around and explore everything.
        - generic [ref=e188]:
          - strong [ref=e190]: Featured products
          - generic [ref=e192]:
            - link "Picture of $25 Virtual Gift Card" [ref=e194] [cursor=pointer]:
              - /url: /25-virtual-gift-card
              - img "Picture of $25 Virtual Gift Card" [ref=e195]
            - generic [ref=e196]:
              - heading "$25 Virtual Gift Card" [level=2] [ref=e197]:
                - link "$25 Virtual Gift Card" [ref=e198] [cursor=pointer]:
                  - /url: /25-virtual-gift-card
              - generic "911 review(s)" [ref=e199]
              - generic [ref=e202]:
                - generic [ref=e204]: "25.00"
                - button "Add to cart" [ref=e206] [cursor=pointer]
          - generic [ref=e208]:
            - link "Picture of 14.1-inch Laptop" [ref=e210] [cursor=pointer]:
              - /url: /141-inch-laptop
              - img "Picture of 14.1-inch Laptop" [ref=e211]
            - generic [ref=e212]:
              - heading "14.1-inch Laptop" [level=2] [ref=e213]:
                - link "14.1-inch Laptop" [ref=e214] [cursor=pointer]:
                  - /url: /141-inch-laptop
              - generic "1713 review(s)" [ref=e215]
              - generic [ref=e218]:
                - generic [ref=e220]: "1590.00"
                - button "Add to cart" [ref=e222] [cursor=pointer]
          - generic [ref=e224]:
            - link "Picture of Build your own cheap computer" [ref=e226] [cursor=pointer]:
              - /url: /build-your-cheap-own-computer
              - img "Picture of Build your own cheap computer" [ref=e227]
            - generic [ref=e228]:
              - heading "Build your own cheap computer" [level=2] [ref=e229]:
                - link "Build your own cheap computer" [ref=e230] [cursor=pointer]:
                  - /url: /build-your-cheap-own-computer
              - generic "925 review(s)" [ref=e231]
              - generic [ref=e234]:
                - generic [ref=e236]: "800.00"
                - button "Add to cart" [ref=e238] [cursor=pointer]
          - generic [ref=e240]:
            - link "Picture of Build your own computer" [ref=e242] [cursor=pointer]:
              - /url: /build-your-own-computer
              - img "Picture of Build your own computer" [ref=e243]
            - generic [ref=e244]:
              - heading "Build your own computer" [level=2] [ref=e245]:
                - link "Build your own computer" [ref=e246] [cursor=pointer]:
                  - /url: /build-your-own-computer
              - generic "433 review(s)" [ref=e247]
              - generic [ref=e250]:
                - generic [ref=e252]: "1200.00"
                - button "Add to cart" [ref=e254] [cursor=pointer]
          - generic [ref=e256]:
            - link "Picture of Build your own expensive computer" [ref=e258] [cursor=pointer]:
              - /url: /build-your-own-expensive-computer-2
              - img "Picture of Build your own expensive computer" [ref=e259]
            - generic [ref=e260]:
              - heading "Build your own expensive computer" [level=2] [ref=e261]:
                - link "Build your own expensive computer" [ref=e262] [cursor=pointer]:
                  - /url: /build-your-own-expensive-computer-2
              - generic "440 review(s)" [ref=e263]
              - generic [ref=e266]:
                - generic [ref=e268]: "1800.00"
                - button "Add to cart" [ref=e270] [cursor=pointer]
          - generic [ref=e272]:
            - link "Picture of Simple Computer" [ref=e274] [cursor=pointer]:
              - /url: /simple-computer
              - img "Picture of Simple Computer" [ref=e275]
            - generic [ref=e276]:
              - heading "Simple Computer" [level=2] [ref=e277]:
                - link "Simple Computer" [ref=e278] [cursor=pointer]:
                  - /url: /simple-computer
              - generic "399 review(s)" [ref=e279]
              - generic [ref=e282]:
                - generic [ref=e284]: "800.00"
                - button "Add to cart" [ref=e286] [cursor=pointer]
  - generic [ref=e287]:
    - generic [ref=e288]:
      - generic [ref=e289]:
        - heading "Information" [level=3] [ref=e290]
        - list [ref=e291]:
          - listitem [ref=e292]:
            - link "Sitemap" [ref=e293] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e294]:
            - link "Shipping & Returns" [ref=e295] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e296]:
            - link "Privacy Notice" [ref=e297] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e298]:
            - link "Conditions of Use" [ref=e299] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e300]:
            - link "About us" [ref=e301] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e302]:
            - link "Contact us" [ref=e303] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e304]:
        - heading "Customer service" [level=3] [ref=e305]
        - list [ref=e306]:
          - listitem [ref=e307]:
            - link "Search" [ref=e308] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e309]:
            - link "News" [ref=e310] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e311]:
            - link "Blog" [ref=e312] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e313]:
            - link "Recently viewed products" [ref=e314] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e315]:
            - link "Compare products list" [ref=e316] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e317]:
            - link "New products" [ref=e318] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e319]:
        - heading "My account" [level=3] [ref=e320]
        - list [ref=e321]:
          - listitem [ref=e322]:
            - link "My account" [ref=e323] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e324]:
            - link "Orders" [ref=e325] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e326]:
            - link "Addresses" [ref=e327] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e328]:
            - link "Shopping cart" [ref=e329] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e330]:
            - link "Wishlist" [ref=e331] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e332]:
        - heading "Follow us" [level=3] [ref=e333]
        - list [ref=e334]:
          - listitem [ref=e335]:
            - link "Facebook" [ref=e336] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e337]:
            - link "Twitter" [ref=e338] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e339]:
            - link "RSS" [ref=e340] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e341]:
            - link "YouTube" [ref=e342] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e343]:
            - link "Google+" [ref=e344] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e345]:
      - text: Powered by
      - link "nopCommerce" [ref=e346] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e347]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('adding a Camera product to the wishlist', async ({ page }) => {
  4  |   const email = process.env.DEMO_WEB_SHOP_EMAIL;
  5  |   const password = process.env.DEMO_WEB_SHOP_PASSWORD;
  6  | 
  7  |   if (!email || !password) {
  8  |     throw new Error(
  9  |       'Define DEMO_WEB_SHOP_EMAIL and DEMO_WEB_SHOP_PASSWORD in the testing environment.',
  10 |     );
  11 |   }
  12 | 
  13 |   await page.goto('https://demowebshop.tricentis.com/');
  14 | 
  15 |   await page.getByRole('link', { name: 'Log in' }).click();
  16 | 
  17 |   await page.locator('#Email').fill(email);
  18 |   await page.locator('#Password').fill(password);
  19 |   await page.getByRole('button', { name: 'Log in' }).click();
  20 | 
  21 |   await expect(page.getByRole('link', { name: email })).toBeVisible();
  22 | 
  23 |   const searchField = page.getByRole('textbox', { name: 'Search store' });
> 24 |   await searchField.fill('Camera');
     |                     ^ Error: locator.fill: Test timeout of 30000ms exceeded.
  25 |   await page.getByRole('button', { name: 'Search' }).click();
  26 | 
  27 |   const cameraProduct = page
  28 |     .locator('.product-item')
  29 |     .filter({
  30 |       has: page.locator('.product-title a', { hasText: 'Camera' }),
  31 |     })
  32 |     .first();
  33 | 
  34 |   await expect(cameraProduct).toBeVisible();
  35 | 
  36 |   const productName = (
  37 |     await cameraProduct.locator('.product-title a').innerText()
  38 |   ).trim();
  39 | 
  40 |   await cameraProduct.locator('.product-title a').click();
  41 | 
  42 |   await expect(page.getByRole('heading', { name: productName })).toBeVisible();
  43 | 
  44 |   await page.getByRole('button', { name: 'Add to wishlist' }).click();
  45 | 
  46 |   await expect(page.locator('#bar-notification')).toContainText(
  47 |     'The product has been added to your wishlist',
  48 |   );
  49 | 
  50 |   await page.getByRole('link', { name: /Wishlist/ }).click();
  51 | 
  52 |   await expect(
  53 |     page.locator('.wishlist-content .product-name', {
  54 |       hasText: productName,
  55 |     }),
  56 |   ).toBeVisible();
  57 | });
```