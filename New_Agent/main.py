import autogen
llm_config={
    "cache_seed": 1,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json",
        filter_dict={"model": ["Your model"]},
    ),
    "temperature": 0.3,
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
    code_execution_config={"work_dir":"Output","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and I need to scrape particular details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
Query="BLACK JACK SPORTS BETTING"
task=f"""
    **Task Description**:
    You are a web scraping agent tasked with automating the extraction and interaction with data from a given website. Your responsibilities include analyzing the website's structure, identifying key elements (e.g., input fields, triggers, links), simulating user actions, and efficiently retrieving relevant information. The extracted results must strictly align with the expected content visible on the provided URL ({url}) without introducing unrelated elements such as arbitrary dates, times, or other extraneous data. Follow the steps outlined below to complete this task systematically.
    
    **Steps to Follow**
    1.Extract the HTML Structure:-
        Fetch the HTML Content: 
            Use web scraping tools to retrieve the HTML content of the provided URL ({url}).
        Analyze the DOM:
            Do this analyze for each page.
            Identify input fields, links, buttons, and other interactive elements.
            Locate containers like tables or lists for displaying results or data.
            Inspect the DOM structure to identify key elements:
                Input Fields: Locate search bars, forms, or fields for user input.
                Buttons: Identify submit buttons, clickable elements, or JavaScript triggers.
                Links: Discover navigation or action links leading to intermediate pages.
                Tables/Containers: Identify containers (e.g., tables, lists) for displaying results or data.
            Whenever a new page from web site is open you should analyze the DOM.
        Document Attributes:
            Record the attributes (e.g., id, class, name, type) of identified elements for precise interaction.
        Store the HTML:
            Save the fetched HTML of the initial page locally for future debugging and detailed structural analysis..

    2. Locate Search Input Fields:-
        Identify Search Fields:
            Locate all text input fields related to search functionality by examining:
                <input> tags with id, name, class, or placeholder attributes.
                Contextual clues from <label> tags or aria-labels.
                Fields with type="text", aria-label, or contextual hints from <label> tags or nearby elements.
        Document Attributes:
            Record attributes like id, name, class, and placeholder for correct interaction.
        Account for Dynamic Changes:
            Use flexible selectors like XPath or CSS to adapt to dynamic or changing DOM structures.
        Store Identified Fields:
            Save details about the fields for programmatically entering queries.

    3. Identify the Search Trigger:-
        Locate Trigger Elements:
            Search for elements that initiate the search, such as:
                <button> tags, <input type="submit">, or class="buttons" or "button" or "btn" anchor <a> tags styled as buttons.
                <a> tags that may have class name as "Buttons" or "button" or "btn"
                Check the text related to "Go" or "Submit" or "Search"
                Sometime Css property also called for making this as button.
                Clickable or accessable <div> or <span> elements with onclick handlers.
                JavaScript-driven functions (e.g., custom __doPostBack or keypress listeners).
        Document Trigger Attributes:
            Record relevant attributes (e.g., onclick, id, href, class) for future interactions.
        Monitor Trigger Actions: 
            Check if the trigger causes:
                Full page reloads.
                Dynamically updated content (e.g., AJAX or JavaScript).

    4. Simulate User Input:-
        Analyze the Query:
            Based on {Query}, determine the appropriate input fields to populate:
                If only a name is provided, use the relevant field for name input.
                If only an ID is provided, fill the ID-specific field.
                If both are provided, populate both fields appropriately.
        Simulate Input and Trigger Search:
            Programmatically enter the query into the identified fields and simulate user trigger the search via button or link clicks, form submission, or custom events.
    
    5. Perform Search Action:-
        Execute the Search:
            Simulate the appropriate action (e.g., clicking a button, executing JavaScript).
        Handle Dynamic Updates:
            Fetch updated HTML if results load dynamically or redirect to a new page.
            Retry if actions fail or result in unexpected states.
        Track Search State:
            Save progress to resume from interruptions.

    6.Handle Search Results:-
        Fetch Updated HTML:
            After triggering the search, retrieve the updated HTML content of the results page.
        Identify Result Links:
            Locate actionable links or elements that correspond to {Query}, such as:
                <a> tags with href attributes pointing to detail pages.
                Interactive elements leading to additional information.
            once you got the search output scrape that HTML and DOM structure then save as new file for seperated DOM as you did before.look for there is any link provided for navigate.if there is then navigate through the respected link for furthur process the link may have the same name or ID as {Query}.
        
    7.Extract Results from Search Links and Navigate to Details Page:-
        Extract HTML of Results Page: 
            Once the search results page loads, extract the HTML content and DOM structure of the page, identifying key elements such as:
                Links (e.g., <a> tags) related to the search query or ID.
                table tag , classnames and IDs associated with navigating to detailed pages.
                Other relevant elements providing details about the {Query}.
                Check for Links in Tables: Ensure you also check within <table> tags for any links that may contain relevant search results or detailed pages.
        Identify Relevant Links:
            From the list of results, locate the link(s) that hold the detailed information about {Query}.
        Navigate to the Detail Page:
            Follow the link(s) to the detail page(s) containing the full information related to {Query}.
        Extract HTML and DOM of the Detail Page:
            On the detail page, extract the HTML content and DOM structure, ensuring you capture the main details related to {Query}.
        Explore the Links on the Detail Page: 
            Identify and navigate through all links (e.g., <a>, <div>) within the main container that holds the detailed information of {Query}.
        Document New Links and Details: 
            Record the links, IDs, and other relevant information related to the {Query} for further processing.
        Verify that the results strictly match the expected output visible on the URL ({url}).
        Avoid including unrelated data such as arbitrary dates, times, or irrelevant details.
        Navigate Intermediate Links:
            Follow intermediate links leading to the expected detailed result page.
            Check for Links in Tables: Look for links within <table> tags, which may contain relevant search results or additional navigation links. Make sure to extract and track these links for further processing.
            Save the DOM structure of each intermediate page for debugging and documentation.

    8. Scrape and Save Detailed Information
        Reanalyze DOM on Detail Pages:
            Parse the results and navigated pages to extract relevant data.
            Identify and extract relevant content (e.g., text, tables, lists, images).
            Locate links to subcategories like “categories” or “directors” and navigate them recursively.
        Recursive Data Extraction:
            Follow all links within detail pages to gather additional details, repeating the DOM analysis for each subsequent page.
            Handle nested structures or multi-level data hierarchies.
        Pagination and Infinite Scroll:
            If data spans multiple pages, interact with pagination controls or simulate infinite scrolling to load more content.
        Save DOM Structures and Data:
            For every visited page, save the DOM structure locally for reference.
            Store the extracted data in a structured format (e.g., JSON, dictionary).

    9. Output the Results
        Format Data:
            Present the extracted data in a structured format, such as JSON, CSV, or a database-ready format.
            Include hierarchical or nested data where applicable.
        Verify Completeness:
            Ensure all details relevant to {Query} have been captured and stored.
        Save Outputs:
            Persist both the extracted data and the DOM structures for every page in a secure and accessible location.
        **Save the Final output in a Text File **

    Key Considerations
        1.Dynamic Content Handling:
            Use automation tools  to handle JavaScript-rendered content and dynamic DOM updates.
            Wait for elements to load completely before interacting.
        2.Error Handling and Retries:
            Implement robust error handling for missing elements, timeouts, or navigation failures.
            Retry failed requests and log issues for debugging.
        3.Efficiency and Detection Avoidance:
            Rotate user agents and IP addresses to prevent detection.
            Introduce random delays to mimic human-like behavior.
        4.State Persistence:
            Maintain a record of visited pages and extracted data to resume interrupted processes seamlessly.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)