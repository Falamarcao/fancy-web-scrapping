from .navigator.navigation_guide import NavigationGuide


class IngressoDotCom(NavigationGuide):

    def go_to_theaters_list(self):
        # Close cookies popup window
        self.append({
            'human_label': 'button_cookies_OK',
            'actions': ['move_to_element', 'click',],
            'many': False,
            'XPATH': r'//*[@id="c-p-bn"]'
        })

        # Move to menu item and click
        self.append({
            'human_label': 'button_sao_paulo_continuar',
            'actions': ['move_to_element', 'click',],
            'many': False,
            'XPATH': r'//*[@id="hd-local-suggest"]/div/div/form/div/button[1]'
        })

        self.append({
            'human_label': 'menu_cinema',
            'actions': ['move_to_element', 'click', 'perform_actions'],
            'many': False,
            'XPATH': r'//*[@id="header"]/div[2]/div/div/div/nav/ul/li[2]/a'
        })

    def get_and_record_movie_theaters(self):
        # GET PLACES
        self.append({
            'human_label': 'Place',
            'subcommands': [
                {'human_label': 'name',
                 'model_name': 'Place',
                 'actions': ['create_entry'],
                 'many': True,
                 'XPATH': r'//div[contains(@class, "card-theater-text")]//strong'},
                {'human_label': 'address',
                 'model_name': 'Place',
                 'actions': ['create_entry'],
                 'many': True,
                 'XPATH': r'//div[contains(@class, "card-theater-text")]//span'},
                {'human_label': 'url',
                 'model_name': 'Place',
                 'actions': ['create_entry', 'perform_create_entry'],
                 'many': True,
                 'XPATH': r'//div[contains(@class, "card-theater-text")]//a',
                 'get_attribute': 'href'}
            ]
        })

    def get_movies(self):
        # Click on cards
        self.append({
            'human_label': 'card-theater-text',
            'actions': ['move_to_element', 'click'],
            'many': True,
            'XPATH': r'//div[contains(@class, "card-theater-text")]'
        })

        self.append({
            'human_label': 'Movie',
            'subcommands': [
                {'human_label': 'image_url',
                 'model_name': 'Movie',
                 'actions': ['create_entry'],
                 'many': True,
                 'XPATH': r'//div[contains(@class, "se-image-container")]//img',
                 'get_attribute': 'src'},
                {'human_label': 'name',
                 'model_name': 'Movie',
                 'actions': ['create_entry'],
                 'many': True,
                 'XPATH': r'//div[contains(@class, "col-md-5") and contains(@class, "se-info")]//span//a'},
                {'human_label': 'duration',
                 'model_name': 'Movie',
                 'actions': ['create_entry', 'back', 'debug_print_data'],
                 'many': False,
                 'XPATH': r'//span[contains(@class, "txt2") and contains(@class, "ng-binding")]'},
            ]
        })
