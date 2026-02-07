
import asyncio
from playwright.async_api import async_playwright
import csv

async def scrape_shivalik_with_playwright():
    """
    Uses Playwright to scrape Shivalik Bank branch data to bypass request blocking.
    """
    all_branches = []
    print("Launching browser...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for page_num in range(1, 11):
            url = f"https://shivalikbank.com/contact/branch?page={page_num}"
            print(f"Navigating to page {page_num}...")
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Using evaluate to run JavaScript in the page context to get the data
                branches_on_page = await page.evaluate('''( () => {
                    const data = [];
                    const containers = document.querySelectorAll('.col-md-4');
                    containers.forEach(branch => {
                        const name = branch.querySelector('h4');
                        const address = branch.querySelector('p');
                        if (name) {
                            data.push({
                                "Branch Name": name.innerText.trim(),
                                "Address": address ? address.innerText.trim() : 'NA'
                            });
                        }
                    });
                    return data;
                } )''')

                if not branches_on_page:
                    print(f"No more branches found on page {page_num}. Stopping.")
                    break
                
                all_branches.extend(branches_on_page)

            except Exception as e:
                print(f"An error occurred on page {page_num}: {e}")
                break

        await browser.close()

    # Save to CSV
    output_file = 'shivalik_branches.csv'
    if not all_branches:
        print("No branches were scraped. CSV file will not be created.")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Branch Name', 'Address'])
        writer.writeheader()
        writer.writerows(all_branches)
        
    print(f"\nSuccessfully scraped {len(all_branches)} branches.")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(scrape_shivalik_with_playwright())
