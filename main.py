results = []

with sync_playwright() as p:
    print("Launching browser...")
    browser = p.chromium.launch(
        #channel="chrome",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--window-size=1920,1080"
        ]
    )
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    for idx, code in enumerate(product_codes, start=1):
        #url=code # In case you got the actual link of the product
        url = f"https://www.amazon.com.mx/dp/{code}" #In case you have an ASIN
        print(f"\n[{idx}] Scraping product: {url}")

        try:
            page.goto(url, timeout=120000, wait_until="domcontentloaded")
            print("   Page loaded")
        except:
            print("   Page load failed, skipping product")
            results.append({"Product Code": code, "URL": url})
            continue
        # ---------------- CHECK FOR BOT WARNING ----------------
        try:
            # Looking for CSS Button class 
            btn_seguir = page.locator("button.a-button-text").first
            
            btn_seguir.wait_for(timeout=3000) 
            
            print("Warning Button dected trying to continue...")
            btn_seguir.click()
            
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2) 
            
        except:
            # If there's no button
            pass
        # ---------------- SMART SCROLL ----------------
        print("  Scrolling page dynamically...")
        scroll_pause = 0.5 #original: 1.0
        max_attempts = 10  #original: 30
        prev_height = 0

        for attempt in range(max_attempts):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            curr_height = page.evaluate("document.body.scrollHeight")
            if curr_height == prev_height:
                break
            prev_height = curr_height
        print("   Scrolling completed")

        # ---------------- EXTRACTION ----------------
        # Title
        try:
            title = page.locator("#productTitle").first.inner_text().strip()
            print(f"   Title: {title[:60]}...")
        except:
            title= "Not Found"
            print(f"   Title: Not Found")

        # Price
        try:
            #symbol = page.locator("span.a-price-symbol").first.inner_text()
            price = page.locator("#centerCol span.a-price-whole").first.inner_text()
            price = re.sub(r'[^\d.]', '', price)
            price=float(price)
            #price = f"{symbol}{whole}"
            print(f"   Price: {price}")
        except:
            price = "Not Found"
            print("  Price: Not Found")

        # List price
        try:
            list_price = page.locator("#centerCol span.a-size-small.aok-offscreen").first.inner_text()
            list_price = re.sub(r'[^\d.]', '', list_price)
            list_price=float(list_price)
            print(f"List Price: {list_price}")
        except:
            list_price = price
            print("  List Price: Not Found")    
        if isinstance(price, float):
            discount=((list_price-price)/list_price)*-1
        else:
            discount="Not Found"

        # Promo Tag
        try:
            badge = page.locator(".dealBadgeTextColor span").first.inner_text().strip()
            print(f"  Badge: {badge}")
            promo_tag=True
        except:
            badge = "Not Found"
            print("   Badge: Not Found")
            promo_tag=False

        # Seller info
        #seller_raw = safe_text("#merchant-info", "Seller Info")
        #seller_info = seller_raw.split("|")[0].strip() if seller_raw != "Not Found" else "Not Found"


        # ---------------- STORE RESULT ----------------
        results.append({
            "Product Code": code,
            "URL": url,
            "Title": title,
            "List price":list_price,
            "Current Price": price,
            "Discount":discount,
            "Promo Tag":promo_tag,
            #"Seller Info": seller_info,
            "Query Date": date.today()
        })

        print(f"[{idx}] Product completed \n")
        time.sleep(1)  # short wait between products original: 2

    print("All products scraped. Closing browser...")
    browser.close()
