import autogen
llm_config={
    "cache_seed": 2,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json",
        filter_dict={"model": ["model name"]},
    ),
    "temperature": 0,
    "max_tokens":2000
}

assistant=autogen.AssistantAgent(
    name="Web_Scraping_Agent",
    llm_config=llm_config
)

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x:x.get("content"," ").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir":"Scraped","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and I need to scrape particular details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
Query="BLACK JACK SPORTS BETTING"
task=f"""
    **Task Description**:  
    You are tasked with automating the extraction of data from a given website. Your role involves analyzing the website’s structure, identifying key elements like input fields, triggers, and interactive elements, simulating user actions, and efficiently retrieving relevant information. The process should be adaptable to different web structures, account for dynamic content, and manage state persistence for reliable and uninterrupted execution.
    Steps to Follow:

    1. Extract the HTML Structure
        1.Fetch the HTML Content:
        Retrieve the HTML content of the provided URL {url} using an appropriate tool like Playwright  or selenium or Pyppeteer.
        2.Analyze the DOM:
        Inspect the DOM structure to identify key elements such as:
        - Input Fields: Search bars, forms.
        - Buttons: Submit buttons, clickable elements.
        - Links: Navigation or action links.
        - Tables: For results display or data extraction.
        Capture all necessary elements that interact with the search and results process, making a note of their attributes (e.g., id, class, name, type).
        3.Store the HTML:
            - Save the fetched HTML for future reference and debugging. This allows you to analyze the page structure in detail during development.

    2. Locate Search Input Fields
        1.Identify Search Fields:
            Identify all relevant text input fields related to search functionality by examining:
                - <input> tags with attributes like id, name, class, or placeholder.
                - Fields with type="text", aria-label, or any contextual hints from adjacent <label> tags.
        2.Document Attributes:
            - Record the necessary attributes (id, name, class, placeholder) of each identified input field to ensure correct interaction.
        3.Account for Dynamic Changes:
            - Ensure selectors are flexible (e.g., XPath or CSS selectors) to handle dynamic or changing attribute values.
        4.Store Search Fields for Reuse:
            - Save the search field attributes for use in automating the entry of search queries.

    3. Identify the Search Trigger
        1.Locate Search Trigger Element:
            Search for the element that initiates the search, which could be:
            - A <button> tag, <input type="submit">, or an anchor <a> tag styled as a button.
            - A clickable element that executes a JavaScript function, such as __doPostBack.
            - Any clickable <div>, <span>, or other elements with event listeners (e.g., onclick, onkeypress).
        2.Document Trigger Attributes:
            Record the necessary attributes of the search trigger (e.g., onclick, href, id, class) for simulating user interaction.
        3.Handle Non-Standard Triggers:
            In case the search is triggered by non-traditional elements, such as pressing the Enter key or hidden buttons, detect and handle these scenarios accordingly.
        4.Monitor for Page Reloads or AJAX Updates:
            Check if the search trigger results in page reloads or dynamic content updates (e.g., AJAX). Prepare to handle these actions.

    4. Simulate User Input
        1.Analyze the Search Query:
            Based on the provided query {Query}, determine which input fields need to be populated:
            - If only a name is provided, fill the search field for name.
            - If only an ID is provided, fill the search field for ID.
            - If both are provided, fill both fields appropriately.
        2.Simulate User Input:
            Programmatically enter the query data into the identified input fields, making sure to handle any special characters or formatting requirements.
        3.Simulate Search Trigger:
            Trigger the search by clicking the search button, submitting the form, or simulating any necessary JavaScript event.

    5. Perform the Search Action
        1.Execute the Search:
            Simulate the search action by either clicking the trigger element or submitting the form.
        2.Handle Dynamic Content:
            If the page content is loaded dynamically (via JavaScript or AJAX), wait for the page to fully load or for the content to appear.
        3.Track Search State:
            Monitor for changes in the page state to ensure the search was successful. If the results aren’t displayed, retry the action or log the error for analysis.

    6. Handle Search Results
    You must do this particular 5 process given below only after you got search result and handling this page may be dynamic.
        1.Fetch Updated HTML:
            After executing the search, retrieve the updated HTML content if the results load on a new page or dynamically.
        2.Identify Search Results:
            Locate the relevant elements in the search results, such as:
                - Links, <a> tags with href attributes.
                - Text, identifiers, or other elements associated with the results.
                -Table Elements: Links or navigation triggers embedded in <tr>, <td>, <th>, or other nested structures.
                -Hidden Elements: JavaScript-driven links or elements with embedded navigation logic.
                -Nested Elements: In some cases, the link may be inside a <div> tag nested within a <tr>, <td>, or similar container. The link will trigger a JavaScript function __doPostBack.
                    -Traverse through these elements and extract any links with the __doPostBack function attached to them.
                -Flexible XPath Navigation: Use relative XPath expressions to adapt to varying structures to find the link or javascript function.
                    - For table rows containing a specific result:
                    ```xpath
                        //table//tr[td[contains(text(), 'Search Result' or 'Select')]]
                    ```
                    - For a specific class-based search result:
                    ```xpath
                    //div[contains(@class, 'result' or 'new_content')]
                    ```

            Traverse the DOM to identify the correct link based on attributes like class, id, text content, or surrounding context.
        3.Validate and Extract Links:
            Confirm the link is valid and points to a detail page.
            Handle cases where the link initiates a POST request:
                Extract hidden input fields, tokens, or other payloads required for the POST request.
                Save these for subsequent navigation.
        4. Store and Prepare for Navigation:
            Save the validated links or identifiers in a structured format (e.g., dictionary or list).
        5.Ensure Proper Navigation:
            Only proceed to the next step if valid links to the detail pages are identified.

    7. Extract and Scrape Details
        1.Navigate to Detailed Pages:
            Click on the relevant search result to navigate to the detailed page. Capture the link or URL needed for navigation.
            For traditional links, use Selenium or similar tools to navigate via href.
            For POST-based navigation:
                Programmatically execute the POST request using tools like requests.
                Include required headers, cookies, or payload data extracted earlier.
        2.Scrape Detailed Information:
            On the detail page, extract all available information, such as:
                - Text content (e.g., descriptions, addresses, etc.).
                - Structured data (e.g., tables, lists).
                - Links to further pages or media content (images, videos).
        3.Handle Pagination:
            If the details span multiple pages:
                - Identify and interact with pagination controls (e.g., "Next", page numbers).
                - If content is loaded via infinite scrolling, simulate scrolling actions to load more data.
        4.Track Navigation:
            Record the navigation path and scrape state, so that if interrupted, the process can resume from the last point.

    8. Output the Results
        1.Structured Data Output:
            -Present the extracted information in a structured, readable text format.
        2.Ensure Accuracy:
            Double-check that the output data is clean, concise, and matches the query. Avoid unnecessary information, ensuring relevance to the search query.
        3.Store Data for Future Use:
            Save the extracted results in a persistent format(JSON,CSV or Text), such as a database or local files, for later use or analysis.

    Key Considerations:
    - Dynamic Content Handling:
        Use automation tools like Selenium, Puppeteer, or Playwright to handle JavaScript-rendered content, AJAX-rendered content or dynamically updated elements.
        Use robust DOM traversal to identify valid links, even when nested in <tr>, <td>, <th>, or other non-standard containers.
        Verify the relevance of links using contextual information.
    -Dynamic XPath/CSS Selectors: 
        Use relative XPath or CSS selectors that depend on content, class names, or dynamic identifiers rather than static positions. This ensures flexibility if the page layout or URL changes.
    -Text-Based and Content Matching: 
        XPath allows you to match elements based on the text they contain or other attributes, making it adaptable even when the page structure changes.
    - Page Interaction and Waiting: 
        For dynamic pages (e.g., with AJAX), use waiting mechanisms in automation tools to ensure that the page has fully loaded before extracting or interacting with elements.
    -Post request Navigation:
        Extract and include necessary form data or tokens for POST-based detail page navigation.
        Use tools like requests or Selenium for proper execution.
    - Handling Non-Standard Elements:
        Be prepared to work with unconventional search triggers like hidden buttons, custom icons, or JavaScript-driven links (e.g., <a> tags with embedded onclick functions).
    - Error Handling and Retry Mechanisms:
        Implement robust error handling. If elements are missing or the search fails, retry the action or log the error for analysis. Include retries for timeouts or failures.
    - Efficiency and Optimization:
        Minimize delays between interactions and optimize code to reduce the load on the server. Avoid detection by using rotating user agents and IP addresses.
    - State Persistence:
        Track the process state (e.g., page number, data scraped) so that if the process is interrupted, it can resume from the last known state without re-running the entire scraping task.
        Record the process state (e.g., scraped links, pagination) for seamless resumption.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)