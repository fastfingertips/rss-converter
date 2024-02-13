from bs4 import BeautifulSoup as TagSoup
import streamlit as st
import requests
import validators

class InputManager:
    textbox_placeholder = 'Enter a RSS **url**.'

    def __init__(self):
        self.data = {
            'input': st.text_input(label=self.textbox_placeholder),
            'query': st.query_params.to_dict()
        }

    def process_data(self):
        input_data = self.data['input']
        query_data = self.data['query']

        if input_data:
            data = input_data
        elif 'q' in query_data:
            # URL Params Found
            data = query_data['q']
        else:
            data = None

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
        #> Provides information in the log file at the beginning of the connection.
        print(f'Conection to the address [{_url}] is being established..')
        while True:
            #> https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
            try:
                urlResponseCode = requests.get(_url, timeout=30)
                urlDom = TagSoup(urlResponseCode.content.decode('utf-8'), 'html.parser')
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

if __name__ == "__main__":
    # Render
    page = Page()
    page.create_title()
    page.create_footer()

    # Input
    input_manager = InputManager()
    user_input = input_manager.process_data()

    if is_url(user_input):
      page_dom = get_dom_from_url(user_input)
      print(page_dom.find('rss'))