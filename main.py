from bs4 import BeautifulSoup as TagSoup
import streamlit as st
import requests
import validators

class InputManager:
    # Placeholder text for the text input field
    textbox_placeholder = 'Enter a RSS **url**.'

    def __init__(self):
        # Initialize the InputManager object
        # - Store the input data from the text input field and query parameters
        self.data = {
            'input': st.sidebar.text_input(label=self.textbox_placeholder),
            'query': st.query_params.to_dict()
        }

    def process_data(self):
        # Process the input data and return the cleaned URL
        input_data = self.data['input']
        query_data = self.data['query']

        if input_data:
            # If input data is provided, use it
            data = input_data
        elif 'q' in query_data:
            # If 'q' parameter is present in query parameters, use it
            data = query_data['q']
        else:
            # If no input data or query parameters are found, set data to None
            data = None

        # Return the cleaned URL data, if available
        return data.strip() if data else None

class Page:
    config = {
        'page_config':{ 
            'page_title':'RSS Converter',
            'page_icon':'🛠️',
            'menu_items':{
            'Get Help': 'https://github.com/FastFingertips/rss-converter',
            'Report a bug': 'https://github.com/FastFingertips/rss-converter/issues',
            'About': 'The developer behind it is [@FastFingertips](https://github.com/FastFingertips).'
            }
        }
    }

    st.set_page_config(**config['page_config'])

    def __init__(self):
        pass

    def create_title(self, text:str=None):
        if text is None:
            text = self.config['page_config']['page_title']
        st.title(text)

    def create_footer(self):
        st.markdown(
            """
            <style>
                .footer {
                    position: fixed;
                    left: 0;
                    bottom: 0;
                    width: 100%;
                    margin-bottom: 1em;
                    background-color: transparent;
                    color: white;
                    text-align: center;
                }
                .footer a {text-decoration: none; margin-left: 0.5em; margin-right: 0.5em;}
                .foooter img {vertical-align: middle;}
            </style>
            <div class="footer">
                <a href="https://github.com/FastFingertips/rss-converter" target="_blank" rel="noopener noreferrer">
                    <img src="https://img.shields.io/github/last-commit/fastfingertips/rss-converter?style=flat&&label=last%20update&labelColor=%2314181C&color=%2320272E">
                </a>
                <img src="https://visitor-badge.laobi.icu/badge?page_id=FastFingertips.rss-converter&left_color=%2314181C&right_color=%2320272E"/>
            </div>
            """,
            unsafe_allow_html=True
        )

def get_dom_from_url(_url) -> TagSoup:
    """
    Reads and retrieves the DOM of the specified page URL.
    """
    try:
        while True:
            #> https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
            try:
                urlResponseCode = requests.get(_url, timeout=30)
                urlDom = TagSoup(urlResponseCode.content.decode('utf-8'), 'xml')
                if urlDom is not None:
                    return urlDom # Returns the page DOM
            except requests.ConnectionError as e:
                print("OOPS!! Connection Error. Make sure you are connected to the Internet. Technical details are provided below.")
                print(str(e))
                continue
            except requests.Timeout as e:
                print("OOPS!! Timeout Error")
                print(str(e))
                continue
            except requests.RequestException as e:
                print("OOPS!! General Error")
                print(str(e))
                continue
            except KeyboardInterrupt:
                print("Someone closed the program")
            except Exception as e:
                print('Error:', e)
    except Exception as e:
        #> If an error occurs while obtaining the DOM...
        print(f'Connection to the address failed [{_url}] Error: {e}')

def is_url(url) -> bool:
      """
      this function checks if the URL is valid or not,
      and returns a boolean value as the result.
      """
      return validators.url(url)

def parse_soup_2(soup):
    if not soup.name:
        return str(soup)

    result = {}
    result['tag'] = soup.name
    if soup.attrs:
        result['attrs'] = soup.attrs
    
    if soup.string:
        result['content'] = soup.string.strip()
    else:
        children = []
        for child in soup.children:
            if child.name:
                children.append(parse_soup_2(child))
        if children:
            result['contents'] = children

    return result

def parse_soup(soup):
    if is_url(user_input):
        rss_dict = {}

        for element in soup.find_all():
            if element.name == "item":
                break

                    
            if 'atom:link' in str(element):
                continue
                rss_dict['atom_link'] = {}
                for attr in element.attrs:
                    rss_dict['atom_link'][attr] = element[attr]
                
            
            if len(element.find_all()) > 1:
                rss_dict[element.name] = {}
                for eleme in element.find_all():
                    element_text = element.get_text()
                    is_digit =  element_text.replace(".", "", 1).isdigit()
                    rss_dict[element.name] = {
                        eleme.name: float(element_text) if is_digit else element_text
                        }
                continue
            element_text = element.get_text()
            is_digit =  element_text.replace(".", "", 1).isdigit()
            rss_dict[element.name] = float(element_text) if is_digit else element_text

        items = []
        for item in soup.find_all("item"):
            item_dict = {}

            for element in item.find_all():
                element_text = element.get_text()
                is_digit =  element_text.replace(".", "", 1).isdigit()
                item_dict[element.name] = float(element_text) if is_digit else element_text
            items.append(item_dict)
        
        rss_dict["items"] = items
        st.json(rss_dict)


if __name__ == "__main__":
    # Render
    page = Page()
    page.create_title()
    page.create_footer()

    example_links = [
            "https://letterboxd.com/horrorville/rss/",
            "http://rss.cnn.com/rss/edition.rss",
            "https://www.filmjabber.com/rss/rss-news.php",
            "https://english.kyodonews.net/rss/all.xml",
        ]

    selected = st.sidebar.selectbox("Select a link", example_links)

    # Input
    input_manager = InputManager()
    user_input = input_manager.process_data() or selected

    if is_url(user_input):
        rss_dict = {}
        dom =  get_dom_from_url(user_input).find('channel')
    
        # st.caption("test1")
        # st.json(parse_soup(dom), expanded=False)
        # st.caption("test2")
        data = parse_soup_2(dom)

        st.json(data, expanded=False)
        contents = data['contents']
        
        dd = {}
        for c in contents:
            try:
                dd[c['tag']] = c['content']
            except KeyError: 
                if c['tag'] == 'item':
                    break
                pass

        main_title = dd['title']
        main_description = dd['description']
        main_link = dd['link']

        st.title(f"[{main_title}]({main_link})")
        st.write(main_description)
        for c in contents:
            if c['tag'] == 'item':
                for cc in c['contents']:
                    if cc['tag'] == 'title':
                        st.subheader(cc['content'])
                    elif cc['tag'] == 'link':
                        st.write(f"[{cc['content']}]({cc['content']})")
                    elif cc['tag'] == 'description':
                        st.write(cc['content'], unsafe_allow_html=True)
                    elif cc['tag'] == 'pubDate':
                        st.write(cc['content'])

    else:
        st.error("Please enter a valid URL")

