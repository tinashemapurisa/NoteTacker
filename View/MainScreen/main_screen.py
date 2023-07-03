from View.base_screen import BaseScreenView
from kivymd.uix.card import MDCard
from libs.notetackerdatabase.data import Data
from kivy.properties import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock


class MainScreenView(BaseScreenView):
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
    def __init__(self,**kw):
        super().__init__(**kw)
        self.db = Data()
        self.no = 0 
        self.display_on_start()
        Clock.schedule_interval(self.check_if_populated,0.0001)
        Clock.schedule_interval(self.check_screen_width,0.0001)

    def check_if_populated(self,dt):
        if len(self.ids.list.children)  == 0 :
            self.ids.indicator.opacity = 1
        if len(self.ids.list.children)  != 0 :
            self.ids.indicator.opacity = 0
    


    def display_on_start(self):
        self.display_notes()
        self.ids.update_btn.bind(on_press = self.update)
        

    def save(self):
        title = self.ids.title.text
        content = self.ids.content.text
        self.db.save_note(title,content)
        self.ids.manager.current = "home"
        print("saved to file")


    def display_notes(self):

        data= self.db.get_notes()

        for i in data:
            card = ContentCard()
            card.title = i["title"]
            card.content = i['content']
            card.date = i['date']
            card.idx = i['id']

            card.bind(on_press = self.send_to_view)
            card.ids.delete_btn.bind(on_press = self.deleteItem)
            self.ids.list.add_widget(card)
        
    def deleteItem(self,instance):
        self.db.delete_note(instance.parent.parent.idx)
        self.ids.list.remove_widget(instance.parent.parent)


    
    def send_to_view(self,instance):
        self.ids.manager.current = "edit"
        self.ids.title_view.text = instance.title
        self.ids.content_view.text = instance.content
        self.no = instance.idx
        print(self.no)
        self.ids.e_toolbar.title = f"{instance.title}"

    def update(self,instance):
        self.db.update_note(self.no,{"title":self.ids.title_view.text,"content": self.ids.content_view.text})
        self.ids.manager.current = "home"
        self.no = self.no
    def check_screen_width(self,dt):
        if self.width <=370:
            self.ids.list.cols = 1
        if self.width >=370:
            self.ids.list.cols = 2




class ContentCard(MDCard,ButtonBehavior):
    title =StringProperty("")
    content = StringProperty("")
    date = StringProperty("")
    idx = 0

    pass
