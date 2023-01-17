from .navigator.navigation_guide import NavigationGuide


class TwitterDotCom(NavigationGuide):

    def login(self): # TODO: Implement login to sometimes mimic more a user behavior, by login in diferent forms
        """
        Randomized paths to login: Bottom banner, right side buttons, ....
        """
        pass

    def search(self, search_term: str):
        # Click on input field
        self.append({
            'human_label': 'input_search_terms',
            'actions': ['move_to_element', 'click',],
            'many': False,
            'XPATH': r'//form[@role="search"]/div[1]/div/div/div/label/div[2]/div/input'
        })
        
        # Click on input field, slow type [input] value, and send ENTER key.
        self.append({
            'human_label': 'input_search_terms',
            # TODO 2: implement pipe action|paramter
            'actions': ['move_to_element', 'click', f'slow_typing|{search_term}', 'send_special_key|RETURN', 'perform_actions'],
            'many': False,
            'XPATH': r'//form[@role="search"]/div[1]/div/div/div/label/div[2]/div/input'
        })

    def go_to_people(self):
        # Click on People Tab
        self.append({
            'human_label': 'button_People',
            'actions': ['move_to_element', 'click', 'perform_actions'],
            'many': False,
            'XPATH': r'//div[@data-testid="ScrollSnap-List"]/div[2]'
        })

        # Get User's data from HoverCard
        # self.append({
        #     'human_label': 'hover_UserAvatar',
        #     'actions': ['move_to_element'], # Show modal on hover
        #     'next': {'actions': ['scroll_page']}, # TODO 2: implement next action - on each element apply scroll_page
        #     'many': True,
        #     'XPATH': r'//img[contains(@src,"https://pbs.twimg.com/profile_images/")]',
        #     'subcommands': [
        #         # User HoverCard
        #         {'human_label': 'HoverCard',
        #          'actions': [''], # Just wait for presence
        #          'many': False,
        #          'XPATH': r'//div[@data-testid="HoverCard"]'},

        #         {'human_label': 'screen_name',  # TODO: be sure that it's ending on .eth
        #          'actions': ['create_entry'],
        #          'many': False,
        #          'XPATH': r'//div[@data-testid="HoverCard"]/div/div/div[2]/div/div/a/div/div[1]/span/span'},

        #         {'human_label': 'username',
        #          'actions': ['create_entry'],
        #          'many': False,
        #          'XPATH': r'//div[@data-testid="HoverCard"]/div/div/div[2]/div/div/div/a/div/div/span'},

        #          # TODO: do a transform function to extract text and links from bio, because bio is a html rich field
        #         {'human_label': 'bio',
        #          'actions': ['create_entry'],
        #          'many': False,
        #          'XPATH': r'//div[@data-testid="HoverCard"]/div/div/div[3]/div'},

        #         {'human_label': 'following_count',
        #          'actions': ['create_entry'],
        #          'many': False,
        #          'XPATH': r'//div[@data-testid="HoverCard"]/div/div/div[4]/div/div[1]/a/span[1]/span'},

        #         {'human_label': 'followers_count',
        #          'actions': ['create_entry', 'debug_print_data'],#, 'perform_create_entry'],
        #          'many': False,
        #          'XPATH': r'//div[@data-testid="HoverCard"]/div/div/div[4]/div/div[2]/a/span[1]/span'},
        #     ]
        # })
