# filename: save_extracted_links.py
extracted_links = [
    {'text': '', 'link': '#ctl00_Menu1_SkipLink'},
    {'text': 'Services', 'link': 'Default.aspx'},
    {'text': 'Search', 'link': 'SearchForm.aspx?sc=0'},
    {'text': 'Study File', 'link': 'https://eforms.eservices.cyprus.gov.cy/MCIT/RCOR/OrganisationFileSearch'},
    {'text': 'Annual Company Fee', 'link': 'SearchForm.aspx?sc=1'},
    {'text': 'Workspace', 'link': 'Restricted/Basket.aspx'},
    {'text': 'Confirmation of Authenticity', 'link': 'CertificateValidationNew.aspx'},
    {'text': 'Results of Name Examination', 'link': 'OrganizationNameExamination.aspx'},
    {'text': 'Electronic Filing', 'link': 'https://efiling.drcor.mcit.gov.cy/drcorprivate/login/authenticate.aspx'},
    {'text': 'Login', 'link': "javascript:__doPostBack('ctl00$lnkLoginStatus','')"},
    {'text': 'Orders Basket (0)', 'link': 'javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("ctl00$ltBasketItems", "", false, "", "ManageOrders.aspx", false, true))'},
    {'text': 'New Search', 'link': "javascript:__doPostBack('ctl00$cphMyMasterCentral$lnkNewSearch','')"},
    {'text': 'Go', 'link': "javascript:__doPostBack('ctl00$cphMyMasterCentral$ucSearch$lbtnSearch','')"},
    {'text': 'Select', 'link': "javascript:__doPostBack('ctl00$cphMyMasterCentral$GridView1','Select$0')"},
    {'text': '', 'link': 'http://www.structuralfunds.org.cy/'},
    {'text': 'Home Page', 'link': 'Default.aspx'},
    {'text': 'Disclaimer', 'link': 'Disclaimer.aspx'},
    {'text': 'Webmaster', 'link': 'WebMaster.aspx'},
    {'text': 'Companies Section', 'link': 'https://www.companies.gov.cy/en/'}
]

# Save the extracted links to a text file
with open("extracted_links.txt", "w", encoding='utf-8') as file:
    for link_info in extracted_links:
        file.write(f"Text: {link_info['text']}, Link: {link_info['link']}\n")

print("Extracted links saved to 'extracted_links.txt'.")